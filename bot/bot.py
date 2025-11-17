import asyncio
import discord
from discord.ext import commands, tasks
import logging
import shutil
import os
from datetime import datetime, timedelta
from .settings import DISCORD_API_SECRET, GUILDS_ID
from .services.acnh_service import NooklookService
from import_all_datasets import ACNHDatasetImporter


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
        self.acnh_service = NooklookService()
        self._shutdown_gracefully = False
        
        # Data update tracking  
        self.dataset_importer = None
        self.last_data_check = None
        self.data_check_interval_hours = 6  # Check every 6 hours (reasonable frequency)
        self.data_update_in_progress = False  # Prevent concurrent updates
    


    
    async def setup_hook(self):
        """Called when the bot is starting up"""
        try:
            # Initialize the database
            await self.acnh_service.init_database()
            self.logger.info("ACNH database initialized")
            
            # Initialize dataset importer for periodic updates
            try:
                self.dataset_importer = ACNHDatasetImporter()
                self.logger.info("Dataset importer initialized for periodic updates")
            except Exception as importer_error:
                self.logger.error(f"Could not initialize dataset importer: {importer_error}")
                self.logger.warning("Periodic data updates will be disabled")
            
            # Load the new nooklook commands cog
            await self.load_extension("bot.cogs.nooklook_commands")
            self.logger.info("Loaded nooklook commands cog")
            
            # Load the help cog if it exists
            try:
                await self.load_extension("bot.cogs.help")
                self.logger.info("Loaded help cog")
            except Exception as help_error:
                self.logger.warning(f"Could not load help cog (optional): {help_error}")
            
            # Note: Command syncing will happen in on_ready() after we know if we're in any guilds
            self.logger.info("Setup complete - commands will sync when bot joins a guild")
                
        except Exception as e:
            self.logger.error(f"Error in setup_hook: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        self.logger.info(f"{self.user} has connected to Discord!")
        self.logger.info(f"Bot is in {len(self.guilds)} guilds")
        
        # Sync commands now that we know our guild status
        try:
            if len(self.guilds) == 0:
                self.logger.warning("Bot is not in any guilds! Invite the bot to a server to use commands.")
                self.logger.info("Create an invite link at: https://discord.com/developers/applications/")
            else:
                # We're in at least one guild, sync commands to all guilds
                # Sync globally to ensure commands appear in all current and future guilds
                await self.tree.sync()
                self.logger.info(f"Synced commands globally to all {len(self.guilds)} guilds")
                
                # Start periodic data update checks
                if self.dataset_importer:
                    self.periodic_data_check.start()
                    self.logger.info(f"Started automatic data freshness checks (every 6 hours)")
                    self.logger.info("Bot will automatically stay up-to-date with Google Sheets data")
                    
                self.logger.info("Bot is ready!")
        except Exception as e:
            self.logger.error(f"Error syncing commands: {e}")

    async def on_guild_join(self, guild):
        """Called when the bot joins a new guild"""
        self.logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        self.logger.info(f"Bot is now in {len(self.guilds)} guilds")
        
        # Optional: Sync commands immediately for this guild for instant availability
        # Note: This is not strictly necessary since global commands will appear automatically
        try:
            synced = await self.tree.sync(guild=guild)
            self.logger.info(f"Synced {len(synced)} commands to {guild.name} immediately")
        except Exception as e:
            self.logger.error(f"Error syncing commands to {guild.name}: {e}")
            # Don't worry too much - global commands will still work



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
                    await self.acnh_service.close_connections()
                    self.logger.info("Closed existing database connections")
                    
                    # Wait a moment for any ongoing operations to complete
                    await asyncio.sleep(2)
                    
                    # Create backup of existing database before update
                    await self._create_database_backup()
                    
                    # Perform the smart import in a controlled way
                    import_performed = self.dataset_importer.import_all_datasets_smart()
                    
                    if import_performed:
                        self.logger.info("Database automatically refreshed with latest data!")
                        
                        # Reinitialize the ACNH service with fresh connections
                        await self.acnh_service.init_database()
                        self.logger.info("Bot service refreshed with new data")
                    else:
                        self.logger.info("No data changes detected during import check")
                        
                finally:
                    # Always complete the update process
                    self.logger.info("Database update complete")
            else:
                self.logger.debug(f"Data is current: {reason}")
                
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

    async def _create_database_backup(self):
        """Create a timestamped backup of the current database before updating"""
        try:
            db_path = "nooklook.db"
            if not os.path.exists(db_path):
                self.logger.warning("Database file not found, skipping backup")
                return
                
            # Create backups directory if it doesn't exist
            backup_dir = "backups"
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
                self.logger.debug(f"Removed old backup: {old_backup}")
                
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
        
        # The ACNH service uses context managers for DB connections, so no cleanup needed
        self.logger.info("ACNH service uses auto-closing connections")
        
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
