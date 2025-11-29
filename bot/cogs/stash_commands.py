"""Stash commands for managing user item collections"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
from typing import Optional

from bot.services.stash_service import StashService
from bot.ui.stash_views import StashListView, StashContentsView, ConfirmDeleteView, RemoveItemsView
from bot.cogs.acnh.base import check_guild_ephemeral

logger = logging.getLogger(__name__)


class StashCommands(commands.Cog):
    """Commands for managing personal item stashes"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.stash_service = StashService()
    
    stash = app_commands.Group(
        name="stash", 
        description="Manage your personal item stashes",
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True)
    )
    
    async def stash_name_autocomplete(
        self, 
        interaction: discord.Interaction, 
        current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete for stash names"""
        stashes = await self.stash_service.get_user_stashes(interaction.user.id)
        
        choices = []
        for stash in stashes:
            if current.lower() in stash['name'].lower():
                choices.append(app_commands.Choice(
                    name=f"📦 {stash['name']} ({stash['item_count']} items)",
                    value=str(stash['id'])
                ))
        
        return choices[:25]
    
    @stash.command(name="create", description="Create a new stash")
    @app_commands.describe(name="Name for your new stash (e.g., 'Kitchen Ideas', 'Cozy Theme')")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def stash_create(self, interaction: discord.Interaction, name: str):
        """Create a new stash"""
        await interaction.response.defer(ephemeral=True)
        
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"stash create command used by:\n\t{interaction.user.display_name} ({interaction.user.id}) in {guild_name or 'Unknown Guild'}")
        
        
        success, message, stash_id = await self.stash_service.create_stash(
            interaction.user.id, 
            name
        )
        
        if success:
            embed = discord.Embed(
                title="✅ Stash Created",
                description=f"Created stash **{name}**\n\n"
                           f"Use `/lookup`, `/search`, or other commands and click **Add to Stash** to save items!",
                color=discord.Color.green()
            )
            
            # Show current stash count
            stashes = await self.stash_service.get_user_stashes(interaction.user.id)
            embed.set_footer(text=f"{len(stashes)}/{self.stash_service.max_stashes} stashes")
        else:
            embed = discord.Embed(
                title="❌ Couldn't Create Stash",
                description=message,
                color=discord.Color.red()
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @stash.command(name="view", description="View contents of a stash")
    @app_commands.describe(stash="The stash to view")
    @app_commands.autocomplete(stash=stash_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def stash_view(self, interaction: discord.Interaction, stash: str):
        """View a specific stash's contents"""
        # Use guild ephemeral settings (public in DMs, honor guild settings, ephemeral if bot not installed)
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"stash view command used by:\n\t{interaction.user.display_name} ({interaction.user.id}) in {guild_name or 'Unknown Guild'}")
        
        # stash is the stash ID from autocomplete
        try:
            stash_id = int(stash)
        except ValueError:
            # User typed a name instead of using autocomplete
            stash_data = await self.stash_service.get_stash_by_name(interaction.user.id, stash)
            if not stash_data:
                await interaction.followup.send(
                    f"❌ Stash '{stash}' not found. Use `/stash list` to see your stashes.",
                    ephemeral=True
                )
                return
            stash_id = stash_data['id']
        
        stash_data = await self.stash_service.get_stash(stash_id, interaction.user.id)
        if not stash_data:
            await interaction.followup.send("❌ Stash not found", ephemeral=True)
            return
        
        items = await self.stash_service.get_stash_items(stash_id, interaction.user.id)
        
        view = StashContentsView(
            interaction_user=interaction.user,
            stash=stash_data,
            items=items,
            stash_service=self.stash_service
        )
        
        # Initialize the view (loads first item, sets up Nookipedia button)
        embed = await view.initialize()
        message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
        view.message = message
    
    @stash.command(name="rename", description="Rename a stash")
    @app_commands.describe(
        stash="The stash to rename",
        new_name="New name for the stash"
    )
    @app_commands.autocomplete(stash=stash_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def stash_rename(
        self, 
        interaction: discord.Interaction, 
        stash: str,
        new_name: str
    ):
        """Rename a stash"""
        await interaction.response.defer(ephemeral=True)
        
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"stash rename command used by:\n\t{interaction.user.display_name} ({interaction.user.id}) in {guild_name or 'Unknown Guild'}")
        
        try:
            stash_id = int(stash)
        except ValueError:
            stash_data = await self.stash_service.get_stash_by_name(interaction.user.id, stash)
            if not stash_data:
                await interaction.followup.send(f"❌ Stash '{stash}' not found", ephemeral=True)
                return
            stash_id = stash_data['id']
        
        success, message = await self.stash_service.rename_stash(
            stash_id, 
            interaction.user.id, 
            new_name
        )
        
        if success:
            embed = discord.Embed(
                title="✅ Stash Renamed",
                description=message,
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Couldn't Rename",
                description=message,
                color=discord.Color.red()
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @stash.command(name="delete", description="Delete a stash and all its items")
    @app_commands.describe(stash="The stash to delete")
    @app_commands.autocomplete(stash=stash_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def stash_delete(self, interaction: discord.Interaction, stash: str):
        """Delete a stash"""
        await interaction.response.defer(ephemeral=True)
        
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"stash delete command used by:\n\t{interaction.user.display_name} ({interaction.user.id}) in {guild_name or 'Unknown Guild'}")
        
        try:
            stash_id = int(stash)
        except ValueError:
            stash_data = await self.stash_service.get_stash_by_name(interaction.user.id, stash)
            if not stash_data:
                await interaction.followup.send(f"❌ Stash '{stash}' not found", ephemeral=True)
                return
            stash_id = stash_data['id']
        
        stash_data = await self.stash_service.get_stash(stash_id, interaction.user.id)
        if not stash_data:
            await interaction.followup.send("❌ Stash not found", ephemeral=True)
            return
        
        # Show confirmation
        embed = discord.Embed(
            title="⚠️ Delete Stash?",
            description=f"Are you sure you want to delete **{stash_data['name']}**?\n\n"
                       f"This will remove the stash and all **{stash_data['item_count']} items** in it.\n"
                       f"This action cannot be undone.",
            color=discord.Color.orange()
        )
        
        view = ConfirmDeleteView(
            interaction_user=interaction.user,
            stash=stash_data,
            stash_service=self.stash_service
        )
        
        message = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        view.message = message
    
    @stash.command(name="remove", description="Remove multiple items from a stash")
    @app_commands.describe(stash="The stash to remove items from")
    @app_commands.autocomplete(stash=stash_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def stash_remove(self, interaction: discord.Interaction, stash: str):
        """Remove multiple items from a stash"""
        await interaction.response.defer(ephemeral=True)
        
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"stash remove command used by:\n\t{interaction.user.display_name} ({interaction.user.id}) in {guild_name or 'Unknown Guild'}")
        
        try:
            stash_id = int(stash)
        except ValueError:
            stash_data = await self.stash_service.get_stash_by_name(interaction.user.id, stash)
            if not stash_data:
                await interaction.followup.send(f"❌ Stash '{stash}' not found", ephemeral=True)
                return
            stash_id = stash_data['id']
        
        stash_data = await self.stash_service.get_stash(stash_id, interaction.user.id)
        if not stash_data:
            await interaction.followup.send("❌ Stash not found", ephemeral=True)
            return
        
        items = await self.stash_service.get_stash_items(stash_id, interaction.user.id)
        
        if not items:
            embed = discord.Embed(
                title="📦 Empty Stash",
                description=f"**{stash_data['name']}** is empty - nothing to remove!",
                color=discord.Color.blue()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        view = RemoveItemsView(
            interaction_user=interaction.user,
            stash=stash_data,
            items=items,
            stash_service=self.stash_service
        )
        
        embed = view.create_embed()
        message = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        view.message = message


async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(StashCommands(bot))
