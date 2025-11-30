import discord
from discord.ext import commands
from discord import app_commands
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.common import get_combined_view, LanguageSelectView
from bot.cogs.acnh.base import check_guild_ephemeral
from bot.cogs.acnh.autocomplete import recipe_name_autocomplete
from bot.repos.user_repo import UserRepository

logger = logging.getLogger(__name__)


class RecipeCommands(commands.Cog):
    """ACNH recipe commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_repo = UserRepository()
    
    @property
    def service(self) -> NooklookService:
        """Get the shared NooklookService from the bot instance"""
        return self.bot.nooklook_service
    
    async def _check_new_user(self, interaction: discord.Interaction) -> bool:
        from bot.ui.common import check_new_user_language
        if await check_new_user_language(interaction, self.user_repo):
            return True
        return False

    @app_commands.command(name="recipe", description="Look up a specific ACNH recipe")
    @app_commands.describe(name="The recipe name to look up")
    @app_commands.autocomplete(name=recipe_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def recipe(self, interaction: discord.Interaction, name: str):
        """Look up recipe details"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        # Check if this is a new user - show language prompt first
        if await self._check_new_user(interaction):
            return

        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        logger.info(f"recipe command used by:\n\t{interaction.user.display_name} ({user_id})\n\tin {guild_name or 'Unknown Guild'}\n\tsearching for: '{name}'")
        
        try:
            # Convert name to recipe ID if it's numeric (from autocomplete)
            if name.isdigit():
                recipe_id = int(name)
                recipe = await self.service.get_recipe_by_id(recipe_id)
            else:
                # Search for recipe by name
                search_results = await self.service.search_all(name, category_filter="recipes")
                recipe = search_results[0] if search_results else None
            
            if not recipe:
                embed = discord.Embed(
                    title="❌ Recipe Not Found",
                    description=f"Sorry, I couldn't find a recipe named **{name}** 😿\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                
                # Add suggestion for food vs DIY search
                embed.add_field(
                    name="💡 Search Tips",
                    value="• Food recipes: savory dishes, desserts, and drinks\n"
                          "• DIY recipes: furniture, tools, and decorations\n"
                          "• Try `/search` with partial names or ingredients",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Create the recipe embed
            embed = recipe.to_discord_embed()
            # embed = await safe_embed_images(embed, 'recipe')
            
            # Add recipe type info in footer
            recipe_type = "Food Recipe" if recipe.is_food() else "DIY Recipe"
            # embed.set_footer(text=f"{recipe_type} • {recipe.category or 'Unknown Category'}")
            
            # Add Nookipedia and refresh button
            view = get_combined_view(
                None, recipe.nookipedia_url, 
                add_refresh=True, content_type="recipe",
                stash_info={'ref_table': 'recipes', 'ref_id': recipe.id, 'display_name': recipe.name}
            )
            
            logger.info(f"found recipe: {recipe.name} ({recipe_type})")
            if view:
                view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            else:
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"❌ Error in /recipe command for user {user_id}, query '{name}': {e}", exc_info=True)
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the recipe.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(RecipeCommands(bot))