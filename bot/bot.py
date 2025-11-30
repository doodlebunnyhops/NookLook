import asyncio
import discord
from discord.ext import commands, tasks
import logging
import shutil
import os
import pathlib
from datetime import datetime, timedelta
from .settings import DISCORD_API_SECRET, GUILDS_ID
from db_tools.import_all_datasets import ACNHDatasetImporter
import topgg

class ACNHBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = False
        intents.presences = False
        intents.members = False
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.logger = logging.getLogger("bot")
        self._shutdown_gracefully = False
        
        # Top.gg client (initialized in setup_hook)
        self.topgg_client = None
        
        # Data update tracking  
        self.dataset_importer = None
        self.last_data_check = None
        self.data_check_interval_hours = 6  # Check every 6 hours (reasonable frequency)
        self.data_update_in_progress = False  # Prevent concurrent updates
    

    async def setup_hook(self):
        """Called when the bot is starting up"""
        self.logger.info("Starting bot setup hook...")
        try:
            # Initialize Top.gg client for bot listing and stats
            if os.getenv("TOP_GG_TOKEN"):
                # Auto posting every 1.3 hours
                self.topgg_client = topgg.DBLClient(bot=self, token=os.getenv("TOP_GG_TOKEN"),autopost=True, post_shard_count=False,autopost_interval=4680)
                self.logger.info("Top.gg client initialized with autopost enabled")
            
            # Note: Database initialization happens in ACNHBaseCog.cog_load()
            # The shared nooklook_service will be available after loading the base cog
            
            # Initialize dataset importer for periodic updates
            try:
                self.dataset_importer = ACNHDatasetImporter()
                self.logger.info("Dataset importer initialized for periodic updates")
            except Exception as importer_error:
                self.logger.error(f"Could not initialize dataset importer: {importer_error}")
                self.logger.warning("Periodic data updates will be disabled")
            
            # Initialize server repository for guild settings
            from bot.repos.server_repo import ServerRepository
            self.server_repo = ServerRepository()
            self.logger.info("Server repository initialized successfully")
            
            # Load the new nooklook commands cog
            # await self.load_extension("bot.cogs.nooklook_commands")
            # Load base FIRST - initializes the shared NooklookService
            await self.load_extension("bot.cogs.acnh.base")

            # Then load command cogs (order doesn't matter for these)
            await self.load_extension("bot.cogs.acnh.artwork_commands")
            await self.load_extension("bot.cogs.acnh.critters_commands")
            await self.load_extension("bot.cogs.acnh.fossil_commands")
            await self.load_extension("bot.cogs.acnh.lookup_commands")
            await self.load_extension("bot.cogs.acnh.recipe_commands")
            await self.load_extension("bot.cogs.acnh.search_commands")
            await self.load_extension("bot.cogs.acnh.villager_commands")
            self.logger.info("Loaded nooklook commands cog successfully")

            await self.load_extension("bot.cogs.server_management")
            self.logger.info("Loaded server management cog successfully")
            
            await self.load_extension("bot.cogs.stash_commands")
            self.logger.info("Loaded stash commands cog successfully")
            
            # CDN monitoring task will be started in on_ready
            self.logger.info("CDN monitoring task defined (will start when bot ready)")
            
            try:
                await self.load_extension("bot.cogs.help")
                self.logger.info("Loaded help cog successfully")
            except Exception as help_error:
                self.logger.warning(f"Could not load help cog (optional): {help_error}")
            
            await self.sync()
            
            # Note: Command syncing will happen in on_ready() after we know if we're in any guilds
            self.logger.info("Setup complete - commands will sync when bot joins a guild")
                
        except Exception as e:
            self.logger.error(f"Error in setup_hook: {e}", exc_info=True)

    async def sync(self):
        """Sync the bot with Discord."""
        logging.info("Syncing bot commands with Discord...")
        try:
            #forces global update
            for guild in self.guilds:
                self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync()
            self.logger.info(f"Synced {len(synced)} commands.")
        except Exception as e:
            logging.error(f"Error during syncing: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        self.logger.info(f"{self.user} has connected to Discord!")
        self.logger.info(f"Bot is in {len(self.guilds)} guilds")
        
        # Check and onboard existing guilds that may not have settings
        await self._onboard_existing_guilds()
        
        # Sync commands now that we know our guild status
        try:
            # Start periodic data update checks
            if self.dataset_importer:
                self.periodic_data_check.start()
                self.logger.info(f"Started automatic data freshness checks (every 6 hours)")
                self.logger.info("Bot will automatically stay up-to-date with Google Sheets data")
            
            # Start CDN monitoring task
            # if not self.cdn_monitoring_task.is_running():
            #     self.cdn_monitoring_task.start()
            #     self.logger.info("Started CDN service monitoring task (15-minute intervals)")
                    
                self.logger.info("Bot is ready!")
        except Exception as e:
            self.logger.error(f"Error syncing commands: {e}")

    async def on_guild_join(self, guild: discord.Guild):
        """Called when the bot joins a new guild"""
        self.logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        self.logger.info(f"Bot is now in {len(self.guilds)} guilds")
        
        # Create default guild settings only for proper installations
        try:
            if hasattr(self, 'server_repo'):
                # Check if settings already exist first
                existing_settings = await self.server_repo.get_guild_settings_if_exists(guild.id)
                if existing_settings is None:
                    # Only create new settings if this is a fresh install
                    # Use the create method which will insert with default False (public)
                    settings = await self.server_repo.get_guild_settings(guild.id)
                    self.logger.info(f"Created guild settings for {guild.name} with public responses (default)")
                else:
                    self.logger.info(f"Guild settings already exist for {guild.name}")
            else:
                self.logger.warning("ServerRepository not available for new guild setup")
        except Exception as e:
            self.logger.error(f"Error setting up guild settings for {guild.name}: {e}")
        
        # Optional: Sync commands immediately for this guild for instant availability
        # Note: This is not strictly necessary since global commands will appear automatically
        try:
            # Add global commands to the guild
            synced = await self.tree.sync()
            self.logger.info(f"Synced {len(synced)} commands to {guild.name} immediately")
        except Exception as e:
            self.logger.error(f"Error syncing commands to {guild.name}: {e}")
            # Don't worry too much - global commands will still work

    async def on_guild_remove(self, guild: discord.Guild):
        """Called when the bot is removed from a guild"""
        self.logger.info(f"Removed from guild: {guild.name} (ID: {guild.id})")
        self.logger.info(f"Bot is now in {len(self.guilds)} guilds")
        
        # Clean up guild settings when bot leaves
        try:
            if hasattr(self, 'server_repo'):
                success = await self.server_repo.delete_guild_settings(guild.id)
                if success:
                    self.logger.info(f"Cleaned up guild settings for {guild.name}")
                else:
                    self.logger.warning(f"Failed to clean up guild settings for {guild.name}")
        except Exception as e:
            self.logger.error(f"Error cleaning up guild settings for {guild.name}: {e}")

    async def _onboard_existing_guilds(self):
        """Check and onboard existing guilds that may not have settings in the database"""
        if not hasattr(self, 'server_repo'):
            self.logger.warning("ServerRepository not available for guild onboarding")
            return
            
        self.logger.info("Checking existing guilds for missing database settings...")
        onboarded_count = 0
        
        for guild in self.guilds:
            try:
                # Check if settings already exist
                existing_settings = await self.server_repo.get_guild_settings_if_exists(guild.id)
                if existing_settings is None:
                    # This guild needs to be onboarded
                    self.logger.info(f"Onboarding existing guild: {guild.name} (ID: {guild.id})")
                    
                    # Create default settings (this will use default False for public responses)
                    settings = await self.server_repo.get_guild_settings(guild.id)
                    if settings:
                        onboarded_count += 1

                    self.logger.info(f"Created guild settings for existing guild {guild.name} with public responses (default)")
                else:
                    self.logger.debug(f"Guild {guild.name} already has settings in database")
                    
            except Exception as e:
                self.logger.error(f"Error onboarding guild {guild.name}: {e}")
                continue
        
        if onboarded_count > 0:
            self.logger.info(f"Successfully onboarded {onboarded_count} existing guild(s) to database")
        else:
            self.logger.info("All existing guilds already have database settings")

    @tasks.loop(hours=6)  # Check every 6 hours (reasonable frequency for sheet updates)
    async def periodic_data_check(self):
        """Periodically check if Google Sheet data has been updated and refresh database if needed"""
        
        # Prevent concurrent updates
        if self.data_update_in_progress:
            self.logger.info("Data update already in progress, skipping this check")
            return
            
        try:
            self.data_update_in_progress = True
            self.logger.info("Performing scheduled data freshness check...")
            
            if not self.dataset_importer:
                self.logger.warning("Dataset importer not available, skipping data check")
                return
            
            # Check if import is needed (this also logs the reason)
            needs_import, reason, sheet_info = self.dataset_importer.check_if_import_needed()
            
            if needs_import:
                self.logger.info(f"Data update detected: {reason}")
                self.logger.info("Starting automatic database refresh...")
                
                try:
                    # Close any existing database connections in the ACNH service
                    if hasattr(self, 'nooklook_service'):
                        await self.nooklook_service.close_connections()
                        self.logger.info("Closed existing database connections")
                    
                    # Wait a moment for any ongoing operations to complete
                    await asyncio.sleep(2)
                    
                    # Create backup of existing database before update
                    await self._create_database_backup()
                    
                    # Perform the smart import in a controlled way
                    import_performed = self.dataset_importer.import_all_datasets_smart()
                    
                    if import_performed:
                        self.logger.info("Database automatically refreshed with latest data!")
                        
                        # Validate the refreshed database
                        if hasattr(self, 'nooklook_service'):
                            try:
                                await self.nooklook_service.init_database()
                                self.logger.info("Database validated after refresh")
                            except Exception as e:
                                self.logger.error(f"Database validation failed after refresh: {e}")
                    else:
                        self.logger.info("No data changes detected during import check")
                        
                finally:
                    # Always complete the update process
                    self.logger.info("Database update complete")
            else:
                self.logger.info(f"Data is current: {reason}")
                
            # Update last check time
            self.last_data_check = datetime.utcnow()
            
        except Exception as e:
            self.logger.error(f"Error during automatic data check: {e}")
            self.logger.error("Bot will continue running with existing data")
        finally:
            self.data_update_in_progress = False

    @periodic_data_check.before_loop
    async def before_periodic_data_check(self):
        """Wait for the bot to be ready before starting periodic checks"""
        await self.wait_until_ready()
        self.logger.info("Bot ready, periodic data checks will begin")
    

    # @tasks.loop(minutes=15)
    # async def cdn_monitoring_task(self):
    #     """Monitor CDN service health every 15 minutes"""
    #     try:
    #         from bot.utils.image_fallback import _image_service_status
    #         await _image_service_status.check_all_monitored_services()
    #     except Exception as e:
    #         self.logger.error(f"Error in CDN monitoring: {e}")
    
    # @cdn_monitoring_task.before_loop
    # async def before_cdn_monitoring(self):
    #     """Wait for bot to be ready before starting CDN monitoring"""
    #     await self.wait_until_ready()
    #     self.logger.info("Bot ready, CDN monitoring will begin")

    async def _create_database_backup(self):
        """Create a timestamped backup of the current database before updating"""
        try:
            # Use absolute path based on this file's location
            bot_file = pathlib.Path(__file__)  # This file is bot/bot.py
            project_root = bot_file.parent.parent  # Go up to project root 
            db_path = str(project_root / "data" / "nooklook.db")
            
            if not os.path.exists(db_path):
                self.logger.warning("Database file not found, skipping backup")
                return
                
            # Create backups directory if it doesn't exist
            backup_dir = str(project_root / "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Create timestamped backup filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"nooklook_backup_{timestamp}.db"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Copy the database file
            shutil.copy2(db_path, backup_path)
            self.logger.info(f"Database backup created: {backup_path}")
            
            # Clean up old backups (keep last 10)
            await self._cleanup_old_backups(backup_dir)
            
        except Exception as e:
            self.logger.error(f"Failed to create database backup: {e}")
            self.logger.warning("Continuing with update despite backup failure")

    async def _cleanup_old_backups(self, backup_dir, keep_count=10):
        """Remove old backup files, keeping only the most recent ones"""
        try:
            # Get all backup files
            backup_files = [f for f in os.listdir(backup_dir) if f.startswith("nooklook_backup_") and f.endswith(".db")]
            
            if len(backup_files) <= keep_count:
                return
                
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)), reverse=True)
            
            # Remove old backups
            files_to_remove = backup_files[keep_count:]
            for old_backup in files_to_remove:
                old_backup_path = os.path.join(backup_dir, old_backup)
                os.remove(old_backup_path)
                self.logger.info(f"Removed old backup: {old_backup}")
                
            if files_to_remove:
                self.logger.info(f"Cleaned up {len(files_to_remove)} old backup(s), keeping {keep_count} most recent")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up old backups: {e}")

    async def close(self):
        """Enhanced close method with proper cleanup"""
        if self._shutdown_gracefully:
            return
            
        self._shutdown_gracefully = True
        self.logger.info("Starting graceful shutdown...")
        
        # Stop periodic data check task
        if hasattr(self, 'periodic_data_check') and self.periodic_data_check.is_running():
            self.periodic_data_check.cancel()
            self.logger.info("Stopped periodic data check task")
        
        # # Stop CDN monitoring task
        # if self.cdn_monitoring_task.is_running():
        #     self.cdn_monitoring_task.cancel()
        #     self.logger.info("Stopped CDN monitoring task")
        
        # Close all database connections (singleton pattern handles all instances)
        from bot.repos.database import Database
        await Database.close_all()
        self.logger.info("Closed all database connections")
        
        # Call the parent close method
        await super().close()
        self.logger.info("Bot connection closed")


async def main():
    """Main function to run the bot with proper shutdown handling"""
    bot = ACNHBot()
    
    if not DISCORD_API_SECRET:
        print("Error: DISCORD_API_TOKEN not found in environment variables")
        return
    
    try:
        print("Starting ACNH Lookup Bot...")
        await bot.start(DISCORD_API_SECRET)
    except KeyboardInterrupt:
        print("\nReceived shutdown signal...")
    except asyncio.CancelledError:
        print("\nBot operation cancelled...")
    except Exception as e:
        print(f"Error running bot: {e}")
    finally:
        print("Cleaning up...")
        if not bot.is_closed():
            try:
                await asyncio.wait_for(bot.close(), timeout=5.0)
                print("Bot shutdown complete")
            except asyncio.TimeoutError:
                print("Bot shutdown timed out")
            except Exception as e:
                print(f"Error during shutdown: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Goodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
