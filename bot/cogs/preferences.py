"""User preferences cog for language and hemisphere settings"""

import discord
from discord import app_commands
from discord.ext import commands
import logging

from ..repos.user_repo import UserRepository, SUPPORTED_LANGUAGES
from ..utils.localization import get_ui

logger = logging.getLogger("bot.cogs.preferences")


class PreferencesCog(commands.Cog):
    """Commands for managing user preferences like language and hemisphere"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_repo = UserRepository()
    
    # Language choices for autocomplete
    def get_language_choices(self):
        return [
            app_commands.Choice(
                name=f"{info['native']} ({info['name']})", 
                value=code
            )
            for code, info in SUPPORTED_LANGUAGES.items()
        ]
    
    @app_commands.command(
        name="language",
        description="Set your preferred language for item names and searches"
    )
    @app_commands.describe(language="Choose your preferred language")
    @app_commands.choices(language=[
        app_commands.Choice(name="English", value="en"),
        app_commands.Choice(name="日本語 (Japanese)", value="ja"),
        app_commands.Choice(name="简体中文 (Chinese)", value="zh"),
        app_commands.Choice(name="한국어 (Korean)", value="ko"),
        app_commands.Choice(name="Français (French)", value="fr"),
        app_commands.Choice(name="Deutsch (German)", value="de"),
        app_commands.Choice(name="Español (Spanish)", value="es"),
        app_commands.Choice(name="Italiano (Italian)", value="it"),
        app_commands.Choice(name="Nederlands (Dutch)", value="nl"),
        app_commands.Choice(name="Русский (Russian)", value="ru"),
    ])
    async def set_language(
        self, 
        interaction: discord.Interaction, 
        language: str
    ):
        """Set user's preferred language"""
        success = await self.user_repo.set_preferred_language(
            interaction.user.id, 
            language
        )
        
        if success:
            lang_info = SUPPORTED_LANGUAGES[language]
            # Use the newly selected language for the confirmation message
            ui = get_ui(language)
            embed = discord.Embed(
                title=f"{ui.language_updated}",
                description=f"{ui.language_set_to} **{lang_info['native']}** ({lang_info['name']}).",
                color=discord.Color.green()
            )
            embed.add_field(
                name=ui.what_this_means,
                value=ui.language_benefits,
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            # Use English for error since we don't know the user's preference
            await interaction.response.send_message(
                f"❌ {get_ui('en').language_update_failed}",
                ephemeral=True
            )
    
    @app_commands.command(
        name="hemisphere",
        description="Set your hemisphere for seasonal availability info"
    )
    @app_commands.describe(hemisphere="Your in-game hemisphere")
    @app_commands.choices(hemisphere=[
        app_commands.Choice(name="Northern Hemisphere", value="north"),
        app_commands.Choice(name="Southern Hemisphere", value="south"),
    ])
    async def set_hemisphere(
        self, 
        interaction: discord.Interaction, 
        hemisphere: str
    ):
        """Set user's hemisphere preference"""
        success = await self.user_repo.set_hemisphere(
            interaction.user.id, 
            hemisphere
        )
        
        if success:
            name = "Northern" if hemisphere == "north" else "Southern"
            embed = discord.Embed(
                title=f"Hemisphere Updated",
                description=f"Your hemisphere is now **{name}**.",
                color=discord.Color.green()
            )
            embed.add_field(
                name="What this means",
                value="• Fish and bug availability will show for your hemisphere\n"
                      "• Seasonal events will match your in-game seasons",
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(
                "❌ Failed to update hemisphere preference. Please try again.",
                ephemeral=True
            )
    
    @app_commands.command(
        name="preferences",
        description="View your current NookLook preferences"
    )
    async def view_preferences(self, interaction: discord.Interaction):
        """Show current user preferences"""
        settings = await self.user_repo.get_user_settings(interaction.user.id)
        
        # Get display info
        lang_code = settings['preferred_language']
        lang_info = SUPPORTED_LANGUAGES.get(lang_code, SUPPORTED_LANGUAGES['en'])
        hemisphere = settings['hemisphere']
        hem_name = "Northern" if hemisphere == "north" else "Southern"
        
        embed = discord.Embed(
            title="Your NookLook Preferences",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="Language",
            value=f"{lang_info['native']} ({lang_info['name']})",
            inline=True
        )
        embed.add_field(
            name="Hemisphere",
            value=hem_name,
            inline=True
        )
        
        if settings['updated_at']:
            embed.set_footer(text=f"Last updated: {settings['updated_at']}")
        else:
            embed.set_footer(text="Using default settings")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(
        name="reset-preferences",
        description="Reset all your preferences to defaults"
    )
    async def reset_preferences(self, interaction: discord.Interaction):
        """Reset user preferences to defaults"""
        await self.user_repo.delete_user_settings(interaction.user.id)
        
        embed = discord.Embed(
            title="🔄 Preferences Reset",
            description="Your preferences have been reset to defaults:\n"
                        "• Language: English\n"
                        "• Hemisphere: Northern",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    """Setup function for loading the cog"""
    await bot.add_cog(PreferencesCog(bot))
