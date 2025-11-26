import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.item_views import VariantSelectView
from bot.ui.search_views import SearchResultsView
from bot.ui.common import get_combined_view
from bot.cogs.acnh.base import check_guild_ephemeral

logger = logging.getLogger(__name__)


class SearchCommands(commands.Cog):
    """ACNH search commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @property
    def service(self) -> NooklookService:
        """Get the shared NooklookService from the bot instance"""
        return self.bot.nooklook_service
    

    @app_commands.command(name="search", description="Search across all ACNH content")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(
        query="What to search for (exact phrase matching)",
        category="Limit search to specific content type"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="Items", value="items"),
        app_commands.Choice(name="Critters", value="critters"),
        app_commands.Choice(name="Fossils", value="fossils"),
        app_commands.Choice(name="Food Recipes", value="food_recipes"),
        app_commands.Choice(name="DIY Recipes", value="diy_recipes"),
        app_commands.Choice(name="Ceiling Decor", value="ceiling-decor"),
        app_commands.Choice(name="Wall Mounted", value="wall-mounted"),
        app_commands.Choice(name="Villagers", value="villagers")
    ])
    async def search(self, interaction: discord.Interaction, 
                    query: str, category: Optional[str] = None):
        """Search across all ACNH content using FTS5"""
        ephemeral = await check_guild_ephemeral(interaction)
        await interaction.response.defer(ephemeral=ephemeral)

        user_id = interaction.user.id
        guild_name = getattr(interaction.guild, 'name', 'DM') if interaction.guild else 'DM'
        category_str = f" in {category}" if category else ""
        logger.info(f"search command used by:\n\t{interaction.user.display_name} ({user_id})\n\tin {guild_name or 'Unknown Guild'}\n\tquery: '{query}'{category_str}")
        
        try:
            # Map Discord choice values to database category values
            category_mapping = {
                "items": "item",           # Discord "items" -> DB "item"
                "critters": "critter",     # Discord "critters" -> DB "critter"  
                "food_recipes": "recipe",  # Discord "food_recipes" -> DB "recipe"
                "diy_recipes": "recipe",   # Discord "diy_recipes" -> DB "recipe"
                "villagers": "villager",   # Discord "villagers" -> DB "villager"
                "artwork": "artwork",      # Discord "artwork" -> DB "artwork"
                "fossils": "fossil",       # Discord "fossils" -> DB "fossil"
                "ceiling-decor": "item",   # Discord "ceiling-decor" -> DB "item" (subcategory)
                "wall-mounted": "item"     # Discord "wall-mounted" -> DB "item" (subcategory)
            }
            
            # Convert category to database format
            db_category = category_mapping.get(category) if category else None
            
            # Handle subcategories for different content types
            recipe_subtype = None
            item_subcategory = None
            
            # Recipe subcategories
            if category == "food_recipes":
                recipe_subtype = "food"
            elif category == "diy_recipes":
                recipe_subtype = "diy"
            
            # Item subcategories
            elif category == "ceiling-decor":
                item_subcategory = "ceiling-decor"
            elif category == "wall-mounted":
                item_subcategory = "wall-mounted"
            
            logger.debug(f"Search: executing search_all with query='{query}', category_filter='{db_category}', recipe_subtype='{recipe_subtype}', item_subcategory='{item_subcategory}' (Discord: '{category}')")
            
            results = await self.service.search_all(query, category_filter=db_category, recipe_subtype=recipe_subtype, item_subcategory=item_subcategory)
            logger.debug(f"Search: found {len(results) if results else 0} results with category filter")
            
            if not results:
                embed = discord.Embed(
                    title="🔍 No Results Found",
                    description=f"No results found for '{query}'",
                    color=0xe74c3c
                )
                if category:
                    embed.description += f" in {category}"
                    logger.info(f"Search: no results for '{query}' in category '{category}'")
                
                embed.add_field(
                    name="💡 Search Tips",
                    value="• Use exact phrases for better results\n" +
                          "• Try different keywords\n" +
                          "• Check your spelling",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Single result - show detailed view
            if len(results) == 1:
                result = results[0]
                
                # If it's an item with variants, show variant selector
                if hasattr(result, 'variants') and len(result.variants) > 1:
                    view = VariantSelectView(result, interaction.user)
                    embed = view.create_embed()
                    get_combined_view(view, result.nookipedia_url)  # Adds Nookipedia button in-place
                    
                    # Send and store message reference for timeout handling
                    view.message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                else:
                    # Show regular embed
                    embed = result.to_embed() if hasattr(result, 'to_embed') else discord.Embed(
                        title=getattr(result, 'name', 'Unknown'),
                        color=0x95a5a6
                    )
                    embed.title = f"🔍 {embed.title}"
                    embed.set_footer(text=f"Search result for '{query}'")
                    category_info = f" in {category}" if category else ""
                    logger.info(f"Search found 1 result for '{query}'{category_info}: {getattr(result, 'name', 'Unknown')}")
                    
                    # Add Nookipedia button if available
                    view = get_combined_view(None, result.nookipedia_url)
                    await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
            # Multiple results - show navigation view
            else:
                view = SearchResultsView(results, query, interaction.user)
                embed = view.create_embed()
                category_info = f" in {category}" if category else ""
                logger.info(f"Search found {len(results)} results for '{query}'{category_info}")
                
                # Send the message and store it in the view for timeout handling
                message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                
                # Store the message in the search view for timeout handling
                view.message = message
            
        except Exception as e:
            logger.error(f"Error in search: {e}")
            embed = discord.Embed(
                title="❌ Search Error",
                description="An error occurred while searching.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(SearchCommands(bot))