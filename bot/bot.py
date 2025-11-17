import asyncio
import discord
from discord.ext import commands
import logging
from .settings import DISCORD_API_SECRET, GUILDS_ID
from .services.acnh_service import NooklookService


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
    
    async def setup_hook(self):
        """Called when the bot is starting up"""
        try:
            # Initialize the database
            await self.acnh_service.init_database()
            self.logger.info("ACNH database initialized")
            
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
                self.logger.warning("⚠️  Bot is not in any guilds! Invite the bot to a server to use commands.")
                self.logger.info("💡 Create an invite link at: https://discord.com/developers/applications/")
            else:
                # We're in at least one guild, sync commands to all guilds
                # Sync globally to ensure commands appear in all current and future guilds
                await self.tree.sync()
                self.logger.info(f"✅ Synced commands globally to all {len(self.guilds)} guilds")
                    
                self.logger.info("🚀 Bot is ready!")
        except Exception as e:
            self.logger.error(f"Error syncing commands: {e}")

    async def on_guild_join(self, guild):
        """Called when the bot joins a new guild"""
        self.logger.info(f"🎉 Joined new guild: {guild.name} (ID: {guild.id})")
        self.logger.info(f"Bot is now in {len(self.guilds)} guilds")
        
        # Optional: Sync commands immediately for this guild for instant availability
        # Note: This is not strictly necessary since global commands will appear automatically
        try:
            synced = await self.tree.sync(guild=guild)
            self.logger.info(f"✅ Synced {len(synced)} commands to {guild.name} immediately")
        except Exception as e:
            self.logger.error(f"Error syncing commands to {guild.name}: {e}")
            # Don't worry too much - global commands will still work

    async def close(self):
        """Enhanced close method with proper cleanup"""
        if self._shutdown_gracefully:
            return
            
        self._shutdown_gracefully = True
        self.logger.info("🛑 Starting graceful shutdown...")
        
        # The ACNH service uses context managers for DB connections, so no cleanup needed
        self.logger.info("✅ ACNH service uses auto-closing connections")
        
        # Call the parent close method
        await super().close()
        self.logger.info("✅ Bot connection closed")


async def main():
    """Main function to run the bot with proper shutdown handling"""
    bot = ACNHBot()
    
    if not DISCORD_API_SECRET:
        print("Error: DISCORD_API_TOKEN not found in environment variables")
        return
    
    try:
        print("🚀 Starting ACNH Lookup Bot...")
        await bot.start(DISCORD_API_SECRET)
    except KeyboardInterrupt:
        print("\n🛑 Received shutdown signal...")
    except asyncio.CancelledError:
        print("\n🛑 Bot operation cancelled...")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
    finally:
        print("🔄 Cleaning up...")
        if not bot.is_closed():
            try:
                await asyncio.wait_for(bot.close(), timeout=5.0)
                print("✅ Bot shutdown complete")
            except asyncio.TimeoutError:
                print("⚠️  Bot shutdown timed out")
            except Exception as e:
                print(f"⚠️  Error during shutdown: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
