"""
Image fallback utilities for handling Cloudflare and other CDN outages
"""
import aiohttp
import logging
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
import discord
from discord.ext import tasks
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def is_valid_url(url: str) -> bool:
    """Check if a URL is properly formatted for Discord"""
    if not url:
        return False
    
    try:
        parsed = urlparse(url)
        # Must have scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return False
        # Must be http or https
        if parsed.scheme not in ['http', 'https']:
            return False
        return True
    except Exception:
        return False

class ImageServiceStatus:
    """Track the status of various image services"""
    
    def __init__(self):
        self.service_status: Dict[str, dict] = {}
        self.last_check: Dict[str, datetime] = {}
        self.check_interval = timedelta(minutes=15)  # Check every 15 minutes
        self.manual_overrides: Dict[str, dict] = {}  # For testing/mocking service states
        
        # Sample URLs from different CDNs to monitor
        self.monitor_urls = [
            "https://dodo.ac/np/images/thumb/4/49/99k_Bells_NH_Inv_Icon_cropped.png/15px-99k_Bells_NH_Inv_Icon_cropped.png",  # Nookipedia
            "https://cdn.discordapp.com/embed/avatars/0.png",  # Discord CDN
            "https://acnhcdn.com/latest/MenuIcon/MoneyBag010.png",  # ACNH CDN (if exists)
        ]
        
    async def check_service_health(self, service_domain: str) -> bool:
        """Check if a service is responding properly"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Try a simple HEAD request to the domain first
                test_url = f"https://{service_domain}"
                logger.debug(f"Testing service health for: {test_url}")
                
                try:
                    async with session.head(test_url) as response:
                        logger.debug(f"HEAD request to {service_domain} returned status: {response.status}")
                        is_healthy = response.status < 500
                        if not is_healthy:
                            logger.warning(f"Service {service_domain} returned status {response.status} (considered unhealthy)")
                        else:
                            logger.debug(f"✅ HEAD request successful for {service_domain}")
                        return is_healthy
                except Exception as head_error:
                    logger.debug(f"HEAD request failed for {service_domain}: {head_error}, trying GET request...")
                    
                    # Some services don't support HEAD, try GET with range request to minimize data
                    headers = {'Range': 'bytes=0-1023'}  # Only get first 1KB
                    try:
                        async with session.get(test_url, headers=headers) as response:
                            logger.debug(f"GET request to {service_domain} returned status: {response.status}")
                            is_healthy = response.status < 500
                            if not is_healthy:
                                logger.warning(f"Service {service_domain} returned status {response.status} on GET (considered unhealthy)")
                            else:
                                logger.debug(f"✅ GET request successful for {service_domain}")
                            return is_healthy
                    except Exception as get_error:
                        logger.warning(f"Both HEAD and GET requests failed for {service_domain}: HEAD={head_error}, GET={get_error}")
                        return False
                        
        except Exception as e:
            logger.warning(f"Service health check failed for {service_domain}: {type(e).__name__}: {e}")
            return False
    
    async def is_service_available(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a service is available, with caching to avoid spam
        Returns (is_available, reason_if_not)
        """
        if not url:
            return True, None
            
        # Extract domain from URL
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
        except Exception:
            return True, None  # If we can't parse, assume it's fine
            
        # Check if we need to test this domain
        now = datetime.now()
        if domain in self.last_check:
            if now - self.last_check[domain] < self.check_interval:
                # Use cached result
                cached_status = self.service_status.get(domain, {})
                is_available = cached_status.get('available', True)
                reason = cached_status.get('reason')
                return is_available, reason
        
        # Perform health check
        logger.debug(f"Checking service health for domain: {domain}")
        is_available = await self.check_service_health(domain)
        
        # Cache the result
        self.last_check[domain] = now
        if is_available:
            self.service_status[domain] = {'available': True, 'reason': None}
            return True, None
        else:
            # Determine likely reason based on domain
            if 'cloudflare' in domain.lower() or any(cf in domain for cf in ['cdn', 'img']):
                reason = "CDN service may be experiencing issues"
            else:
                reason = "Image service temporarily unavailable"
                
            self.service_status[domain] = {'available': False, 'reason': reason}
            logger.info(f"Service {domain} appears to be down: {reason}")
            return False, reason
    
    def is_service_healthy(self, domain: str, bypass_cache: bool = False) -> bool:
        """
        Check if a service is healthy (synchronous version for use with get_safe_image_url)
        
        Args:
            domain: Domain to check
            bypass_cache: If True, force fresh check
            
        Returns:
            bool: True if service appears healthy
        """
        if not domain:
            return True
            
        # Check manual overrides first (for testing)
        if domain in self.manual_overrides:
            override = self.manual_overrides[domain]
            logger.debug(f"Using manual override for {domain}: {override['available']} ({override.get('reason', 'Manual override')})")
            return override['available']
            
        # Check cache first unless bypassing
        if not bypass_cache and domain in self.service_status:
            now = datetime.now()
            if domain in self.last_check and (now - self.last_check[domain]) < self.check_interval:
                # Use cached result
                return self.service_status[domain].get('available', True)
        
        # For synchronous calls, we can't do actual HTTP checks
        # Just return the cached status or assume healthy
        cached_status = self.service_status.get(domain, {})
        return cached_status.get('available', True)
    
    def set_manual_override(self, domain: str, is_available: bool, reason: str = None):
        """Manually override service status for testing purposes"""
        if reason is None:
            reason = "Manual override for testing" if not is_available else "Manual override - service restored"
            
        self.manual_overrides[domain] = {
            'available': is_available,
            'reason': reason,
            'timestamp': datetime.now()
        }
        
        # Also update the main service status to show in /service-status
        self.service_status[domain] = {
            'available': is_available,
            'reason': f"🔧 {reason}"
        }
        self.last_check[domain] = datetime.now()
        
        logger.info(f"Manual override set: {domain} = {'Available' if is_available else 'Down'} ({reason})")
    
    def clear_manual_override(self, domain: str):
        """Clear manual override for a domain"""
        if domain in self.manual_overrides:
            del self.manual_overrides[domain]
            logger.info(f"Cleared manual override for {domain}")
            
            # Remove from service status too if it was a manual override
            if domain in self.service_status and self.service_status[domain].get('reason', '').startswith('🔧'):
                del self.service_status[domain]
                if domain in self.last_check:
                    del self.last_check[domain]
    
    def clear_all_overrides(self):
        """Clear all manual overrides"""
        cleared_domains = list(self.manual_overrides.keys())
        self.manual_overrides.clear()
        
        # Clean up service status entries that were manual overrides
        for domain in cleared_domains:
            if domain in self.service_status and self.service_status[domain].get('reason', '').startswith('🔧'):
                del self.service_status[domain]
                if domain in self.last_check:
                    del self.last_check[domain]
        
        if cleared_domains:
            logger.info(f"Cleared all manual overrides for domains: {cleared_domains}")
    
    async def check_all_monitored_services(self):
        """Check all monitored services - called by Discord task loop"""
        logger.info("Running periodic service health checks...")
        
        for url in self.monitor_urls:
            try:
                parsed = urlparse(url)
                domain = parsed.netloc
                logger.debug(f"Processing monitor URL: {url} -> domain: {domain}")
                
                if domain and domain not in self.manual_overrides:  # Skip manually overridden services
                    logger.info(f"Checking health for domain: {domain} (from URL: {url})")
                    is_healthy = await self.check_service_health(domain)
                    now = datetime.now()
                    
                    self.last_check[domain] = now
                    if is_healthy:
                        self.service_status[domain] = {'available': True, 'reason': None}
                        logger.info(f"✅ Service {domain} is healthy")
                    else:
                        reason = "CDN service may be experiencing issues" if any(x in domain for x in ['cdn', 'img', 'cloudflare']) else "Service temporarily unavailable"
                        self.service_status[domain] = {'available': False, 'reason': reason}
                        logger.warning(f"❌ Service {domain} appears down: {reason}")
                elif domain in self.manual_overrides:
                    logger.debug(f"Skipping {domain} - has manual override")
                else:
                    logger.warning(f"Could not extract domain from URL: {url}")
            
            except Exception as e:
                logger.error(f"Error checking monitor URL {url}: {type(e).__name__}: {e}", exc_info=True)

# Global instance
_image_service_status = ImageServiceStatus()

# No fallback images - just service checking with notifications

def get_safe_image_url(original_url: str, bypass_cache: bool = False) -> tuple[str, str]:
    """
    Get safe image URL with service monitoring
    
    Args:
        original_url: Original image URL to check
        bypass_cache: If True, force fresh service check
    
    Returns:
        tuple: (url_to_use, warning_message or empty string)
    """
    if not original_url or not original_url.strip():
        return "", ""
    
    try:
        import urllib.parse
        parsed_url = urllib.parse.urlparse(original_url.strip())
        domain = parsed_url.netloc.lower()
        
        if not domain:
            return original_url, ""
        
        status = _image_service_status.is_service_healthy(domain, bypass_cache)
        
        if not status:
            warning = "⚠️ CDN service may be experiencing issues. Image may not load properly."
            logger.warning(f"Service {domain} appears unhealthy, showing warning to users")
            return original_url, warning
        
        return original_url, ""
        
    except Exception as e:
        logger.error(f"Error checking image service for {original_url}: {e}")
        return original_url, ""

def add_service_notice_to_embed(embed: discord.Embed, service_notice: Optional[str]) -> discord.Embed:
    """Add a service notice to an embed if there are image service issues"""
    if service_notice:
        # Add the notice to the footer
        current_footer = embed.footer.text if embed.footer else ""
        if current_footer:
            embed.set_footer(text=f"{current_footer} | {service_notice}")
        else:
            embed.set_footer(text=service_notice)
            
        # Optionally change embed color to indicate issues
        if embed.color == discord.Color.default():
            embed.color = discord.Color.orange()
            
    return embed

# async def safe_set_image(embed: discord.Embed, image_url: Optional[str], content_type: str = 'general') -> discord.Embed:
#     """Safely set an embed image with fallback handling"""
#     safe_url, notice = get_safe_image_url(image_url, bypass_cache=False)
    
#     if safe_url and is_valid_url(safe_url):
#         embed.set_image(url=safe_url)
#     elif safe_url:
#         logger.warning(f"Invalid URL format for image: {safe_url}")
        
#     if notice:
#         embed = add_service_notice_to_embed(embed, notice)
        
#     return embed

# async def safe_set_thumbnail(embed: discord.Embed, image_url: Optional[str], content_type: str = 'general') -> discord.Embed:
#     """Safely set an embed thumbnail with fallback handling"""
#     safe_url, notice = get_safe_image_url(image_url, bypass_cache=False)
    
#     if safe_url and is_valid_url(safe_url):
#         embed.set_thumbnail(url=safe_url)
#     elif safe_url:
#         logger.warning(f"Invalid URL format for thumbnail: {safe_url}")
        
#     if notice:
#         embed = add_service_notice_to_embed(embed, notice)
        
#     return embed

def get_service_status_summary() -> Dict[str, dict]:
    """Get current status of all monitored services"""
    return dict(_image_service_status.service_status)







def get_service_monitoring_config() -> Dict[str, any]:
    """Get current service monitoring configuration"""
    return {
        'check_interval_minutes': 15,
        'monitored_services': list(_image_service_status.service_status.keys()) if _image_service_status.service_status else [],
        'monitor_urls': _image_service_status.monitor_urls,
        'background_task_running': 'Managed by bot',  # Task is now managed by the bot class
        'manual_overrides': dict(_image_service_status.manual_overrides),
        'status_message': '⚠️ CDN service may be experiencing issues. Image may not load properly.'
    }

# Manual override functions for testing
def mock_service_down(domain: str, reason: str = None):
    """Mock a service as down for testing purposes"""
    if reason is None:
        reason = f"Simulated outage for {domain}"
    _image_service_status.set_manual_override(domain, False, reason)

def mock_service_up(domain: str, reason: str = None):
    """Mock a service as up for testing purposes"""    
    if reason is None:
        reason = f"Simulated recovery for {domain}"
    _image_service_status.set_manual_override(domain, True, reason)

def clear_service_mock(domain: str):
    """Clear mock status for a domain"""
    _image_service_status.clear_manual_override(domain)

def clear_all_service_mocks():
    """Clear all service mocks"""
    _image_service_status.clear_all_overrides()

def get_active_mocks() -> Dict[str, dict]:
    """Get all currently active manual overrides"""
    return dict(_image_service_status.manual_overrides)