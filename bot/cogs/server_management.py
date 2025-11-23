"""Server management commands for guild administrators and owners"""

import discord
from discord.ext import commands
from discord import app_commands
import logging

from bot.repos.server_repo import ServerRepository

logger = logging.getLogger(__name__)

class ServerManagement(commands.Cog):
    """Server configuration and management commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.server_repo = ServerRepository()

    server = app_commands.Group(name="server", description="Server management commands", guild_only=True)

    def is_type_guild():
        async def predicate(interaction: discord.Interaction) -> bool:
            # Check if the interaction occurred in a guild
            try:
                if interaction.guild:
                    return True
                return False
            except Exception as e:
                logger.error(f"Exception in is_type_guild predicate: {e}")
                return False

        return app_commands.check(predicate)

    def is_admin_or_owner():
        async def predicate(interaction: discord.Interaction) -> bool:
            """Check if user is guild administrator or owner"""
            if interaction.user.id == interaction.guild.owner_id or interaction.user.guild_permissions.administrator:
                return True
            await interaction.response.send_message("You must be a server administrator or the server owner to use this command.", ephemeral=True)
            return False

        return app_commands.check(predicate)
    
    @server.command(name="settings", description="View current server settings")
    @is_admin_or_owner()
    @is_type_guild()
    @app_commands.allowed_contexts(private_channels=False,guilds=True,dms=False)
    async def show_settings_command(self, interaction: discord.Interaction):
        """Show current server settings"""
        await self._show_settings(interaction)
    
    @server.command(name="hide_responses", description="Configure response visibility")
    @app_commands.describe(
        hide="Whether to hide bot responses or show to everyone"
    )
    @is_admin_or_owner()
    @is_type_guild()
    @app_commands.allowed_contexts(private_channels=False,guilds=True,dms=False)
    async def server_command(
        self, 
        interaction: discord.Interaction, 
        hide: bool
    ):
        """Configure whether bot responses are hidden (ephemeral) or visible to everyone"""
        
        # Check if bot is properly installed in this guild
        try:
            existing_settings = await self.server_repo.get_guild_settings_if_exists(interaction.guild.id)
            if existing_settings is None:
                embed = discord.Embed(
                    title="❌ Bot Not Installed",
                    description="This server doesn't have the bot installed yet.\n\n"
                            "**Current Behavior:**\n"
                            "• Bot responses are currently **hidden** (ephemeral) for safety\n"
                            "• Only command users can see bot responses\n\n"
                            "**To configure settings:**\n"
                            "• The bot needs to be installed to the server for settings to be available\n",
                    color=0xe74c3c
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        except Exception as e:
            await interaction.response.send_message(
                "❌ An error occurred while checking server installation. Please try again later.",
                ephemeral=True
            )
            raise e
        
        # Update the ephemeral setting (hide = True means ephemeral = True)
        success = await self.server_repo.update_ephemeral_setting(interaction.guild.id, hide)
        
        if not success:
            await interaction.response.send_message(
                "❌ Failed to update server settings. Please try again.",
                ephemeral=True
            )
            return
        
        # Create response embed
        status_text = "hidden, this means only the command user can see them." if hide else "visible to everyone."
        
        embed = discord.Embed(
            title="Setting Updated",
            description=f"Bot responses are now **{status_text}**",
            color=0x7FB069
        )
        
        # Use the opposite of the new setting for this announcement so everyone can see the change
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def _show_settings(self, interaction: discord.Interaction):
        """Show current server settings"""
        # Check if bot is properly installed in this guild first
        existing_settings = await self.server_repo.get_guild_settings_if_exists(interaction.guild.id)
        if existing_settings is None:
            embed = discord.Embed(
                title="❌ Bot Not Installed",
                description="This server doesn't have the bot installed yet.\n\n"
                           "**Current Behavior:**\n"
                           "• Bot responses are currently **hidden** (ephemeral) for safety\n"
                           "• Only command users can see bot responses\n\n"
                           "**To configure settings:**\n"
                           "• The bot needs to be installed to the server for settings to be available\n",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Bot is installed, get the actual settings
        settings = existing_settings
        
        embed = discord.Embed(
            title=f"Server Settings for {interaction.guild.name}",
            color=0x7FB069,
            description="Current configuration for this server"
        )
        
        ephemeral_status = "Enabled" if settings["ephemeral_responses"] else "Disabled"
        
        embed.add_field(
            name=f"Ephemeral Responses",
            value=f"**{ephemeral_status}**\n"
                  f"{'Bot responses are only visible to the command user' if settings['ephemeral_responses'] else 'Bot responses are visible to everyone in the channel'}",
            inline=False
        )
        
        # Check if user has admin permissions to show help text
        member = interaction.user
        has_admin_perms = False
        if isinstance(member, discord.Member):
            has_admin_perms = (member.guild_permissions.administrator or 
                            member.id == interaction.guild.owner_id)
        
        if has_admin_perms:
            embed.add_field(
                name="How to Change Settings",
                value="Use `/server hide_responses true` or `/server hide_responses false` to toggle response visibility",
                inline=False
            )
        
        # Get current guild setting for ephemeral response
        ephemeral = settings["ephemeral_responses"]
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # @server_command.error
    # async def server_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    #     """Handle errors for server command"""
    #     logger.error(f"Error in server command: {error}")
        
    #     if isinstance(error, app_commands.MissingPermissions):
    #         await interaction.response.send_message(
    #             "❌ You don't have permission to use this command!",
    #             ephemeral=True
    #         )
    #     else:
    #         await interaction.response.send_message(
    #             "❌ An error occurred while processing the command. Please try again.",
    #             ephemeral=True
    #         )

async def setup(bot: commands.Bot):
    """Setup function to add cog to bot"""
    await bot.add_cog(ServerManagement(bot))