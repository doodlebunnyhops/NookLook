"""Modern ACNH Discord commands using the new nooklook database"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, List
import logging

from bot.services.acnh_service import NooklookService
from bot.ui.pagination import (
    ItemsPaginationView, 
    CrittersPaginationView, 
    VariantSelectView,
    SearchResultsView,
    PaginatedResultView
)

logger = logging.getLogger(__name__)

def is_dm(interaction: discord.Interaction) -> bool:
    """Check if interaction is in a DM or Group DM (both have guild=None)"""
    return interaction.guild is None

async def villager_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for villager names"""
    try:
        # Get the cog to access the service
        cog = interaction.client.get_cog('ACNHCommands')
        if not cog or not hasattr(cog, 'service'):
            return []
        
        # Get villager suggestions
        suggestions = await cog.service.get_villager_suggestions(current)
        
        # Convert to choices
        choices = []
        for name, villager_id in suggestions:
            # Use villager ID as the value for lookup
            choices.append(app_commands.Choice(name=name, value=str(villager_id)))
        
        return choices[:25]  # Discord limit
    except Exception as e:
        logger.error(f"Error in villager autocomplete: {e}")
        return []

async def recipe_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for recipe names"""
    try:
        # Get the cog to access the service
        cog = interaction.client.get_cog('ACNHCommands')
        if not cog or not hasattr(cog, 'service'):
            return []
        
        # Get recipe suggestions
        if not current or len(current) <= 2:
            # Show random recipes when query is too short
            suggestions = await cog.service.get_random_recipe_suggestions(25)
        else:
            suggestions = await cog.service.get_recipe_suggestions(current)
        
        # Convert to choices
        choices = []
        for name, recipe_id in suggestions:
            choices.append(app_commands.Choice(name=name, value=str(recipe_id)))
        
        return choices[:25]  # Discord limit
    except Exception as e:
        logger.error(f"Error in recipe autocomplete: {e}")
        return []

async def artwork_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for artwork names"""
    try:
        # Get the cog to access the service
        cog = interaction.client.get_cog('ACNHCommands')
        if not cog or not hasattr(cog, 'service'):
            return []
        
        # Get artwork suggestions
        if not current or len(current) <= 2:
            # Show random artwork when query is too short
            suggestions = await cog.service.get_random_artwork_suggestions(25)
        else:
            suggestions = await cog.service.get_artwork_suggestions(current)
        
        # Convert to choices
        choices = []
        for name, artwork_id in suggestions:
            choices.append(app_commands.Choice(name=name, value=str(artwork_id)))
        
        return choices[:25]  # Discord limit
    except Exception as e:
        logger.error(f"Error in artwork autocomplete: {e}")
        return []

async def critter_name_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete for critter names"""
    try:
        # Get the cog to access the service
        cog = interaction.client.get_cog('ACNHCommands')
        if not cog or not hasattr(cog, 'service'):
            return []
        
        # Get critter suggestions
        if not current or len(current) <= 2:
            # Show random critters when query is too short
            suggestions = await cog.service.get_random_critter_suggestions(25)
        else:
            suggestions = await cog.service.get_critter_suggestions(current)
        
        # Convert to choices
        choices = []
        for name, critter_id in suggestions:
            choices.append(app_commands.Choice(name=name, value=str(critter_id)))
        
        return choices[:25]  # Discord limit
    except Exception as e:
        logger.error(f"Error in critter autocomplete: {e}")
        return []

class BrowseGroup(app_commands.Group):
    """Command group for browsing different types of ACNH content"""
    
    def __init__(self, service: NooklookService):
        super().__init__(name="browse", description="Browse ACNH content with filters")
        self.service = service
        
        # Cache filter options for autocomplete
        self.filter_options = {}
        self._filters_loaded = False
    
    async def _ensure_filters_loaded(self):
        """Ensure filter options are loaded for autocomplete"""
        if not self._filters_loaded:
            try:
                self.filter_options = await self.service.get_filter_options()
                self._filters_loaded = True
            except Exception as e:
                logger.error(f"Failed to load filter options: {e}")
                self.filter_options = {}
    
    # Autocomplete functions for filters
    async def category_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        """Autocomplete for item categories"""
        await self._ensure_filters_loaded()
        categories = self.filter_options.get('item_categories', [])
        
        # Filter based on current input
        filtered = [cat for cat in categories if current.lower() in cat.lower()][:25]
        return [app_commands.Choice(name=cat, value=cat) for cat in filtered]
    
    @app_commands.command(name="items", description="Browse furniture and items with filters")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(
        category="Filter by item category (e.g., Housewares, Miscellaneous)",
        color="Filter by primary color",
        price_range="Filter by price range"
    )
    @app_commands.autocomplete(category=category_autocomplete)
    @app_commands.choices(color=[
        app_commands.Choice(name="Red", value="red"),
        app_commands.Choice(name="Orange", value="orange"),
        app_commands.Choice(name="Yellow", value="yellow"),
        app_commands.Choice(name="Green", value="green"),
        app_commands.Choice(name="Blue", value="blue"),
        app_commands.Choice(name="Purple", value="purple"),
        app_commands.Choice(name="Pink", value="pink"),
        app_commands.Choice(name="Brown", value="brown"),
        app_commands.Choice(name="Black", value="black"),
        app_commands.Choice(name="White", value="white"),
        app_commands.Choice(name="Gray", value="gray")
    ])
    @app_commands.choices(price_range=[
        app_commands.Choice(name="Free (0 bells)", value="free"),
        app_commands.Choice(name="Cheap (1-1000 bells)", value="cheap"),
        app_commands.Choice(name="Moderate (1001-5000 bells)", value="moderate"),
        app_commands.Choice(name="Expensive (5001-20000 bells)", value="expensive"),
        app_commands.Choice(name="Very Expensive (20000+ bells)", value="very_expensive")
    ])
    async def browse_items(self, interaction: discord.Interaction, 
                          category: Optional[str] = None,
                          color: Optional[str] = None,
                          price_range: Optional[str] = None):
        """Browse items with optional filters"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            data = await self.service.browse_items(category, color, price_range)
            
            if not data['items']:
                embed = discord.Embed(
                    title="🔍 No Items Found",
                    description="No items match your filter criteria.",
                    color=0xe74c3c
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            view = ItemsPaginationView(
                bot=interaction.client,
                interaction_user=interaction.user,
                data=data,
                service=self.service,
                category=category,
                color=color,
                price_range=price_range
            )
            
            embed = view.create_embed()
            await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in browse_items: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while browsing items.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

class ACNHCommands(commands.Cog):
    """ACNH lookup commands using nooklook database"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.service = NooklookService()
        
        # Add the browse command group
        self.browse = BrowseGroup(self.service)
        self.bot.tree.add_command(self.browse)
    
    async def cog_load(self):
        """Initialize the database when cog loads"""
        try:
            await self.service.init_database()
            logger.info("ACNH database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ACNH database: {e}")
    
    @app_commands.command(name="search", description="Search across all ACNH content")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(
        query="What to search for (exact phrase matching)",
        category="Limit search to specific content type"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="Items", value="items"),
        app_commands.Choice(name="Critters", value="critters"),
        app_commands.Choice(name="Recipes", value="recipes"),
        app_commands.Choice(name="Villagers", value="villagers")
    ])
    async def search(self, interaction: discord.Interaction, 
                    query: str, category: Optional[str] = None):
        """Search across all ACNH content using FTS5"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            results = await self.service.search_all(query, category)
            
            if not results:
                embed = discord.Embed(
                    title="🔍 No Results Found",
                    description=f"No results found for '{query}'",
                    color=0xe74c3c
                )
                if category:
                    embed.description += f" in {category}"
                
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
                    await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                else:
                    # Show regular embed
                    embed = result.to_embed() if hasattr(result, 'to_embed') else discord.Embed(
                        title=getattr(result, 'name', 'Unknown'),
                        color=0x95a5a6
                    )
                    embed.title = f"🔍 {embed.title}"
                    embed.set_footer(text=f"Search result for '{query}'")
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
            # Multiple results - show navigation view
            else:
                view = SearchResultsView(results, query, interaction.user)
                embed = view.create_embed()
                await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in search: {e}")
            embed = discord.Embed(
                title="❌ Search Error",
                description="An error occurred while searching.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
    
    # @app_commands.command(name="database-stats", description="Show database statistics")
    # async def database_stats(self, interaction: discord.Interaction):
    #     """Show comprehensive database statistics"""
    #     ephemeral = not is_dm(interaction)
    #     await interaction.response.defer(ephemeral=ephemeral)
        
    #     try:
    #         stats = await self.service.get_database_stats()
            
    #         embed = discord.Embed(
    #             title="📊 Database Statistics",
    #             color=0x3498db
    #         )
            
    #         if stats.get('database_active'):
    #             # Add individual counts
    #             stats_text = []
    #             if 'items' in stats:
    #                 stats_text.append(f"🏠 Items: {stats['items']:,}")
    #             if 'critters' in stats:
    #                 stats_text.append(f"🐛 Critters: {stats['critters']:,}")
    #             if 'recipes' in stats:
    #                 stats_text.append(f"🛠️ Recipes: {stats['recipes']:,}")
    #             if 'villagers' in stats:
    #                 stats_text.append(f"👥 Villagers: {stats['villagers']:,}")
                
    #             embed.add_field(
    #                 name="📈 Content Counts",
    #                 value="\n".join(stats_text),
    #                 inline=False
    #             )
                
    #             embed.add_field(
    #                 name="📦 Total Content",
    #                 value=f"{stats.get('total_content', 0):,} items",
    #                 inline=True
    #             )
                
    #             embed.color = 0x2ecc71
    #         else:
    #             embed.description = "Database is not available or empty."
    #             if 'error' in stats:
    #                 embed.add_field(name="Error", value=stats['error'], inline=False)
    #             embed.color = 0xe74c3c
            
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
    #     except Exception as e:
    #         logger.error(f"Error in database_stats: {e}")
    #         embed = discord.Embed(
    #             title="❌ Error",
    #             description="An error occurred while fetching database statistics.",
    #             color=0xe74c3c
    #         )
    #         await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    async def item_name_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete for item names (base items only, no variants)"""
        try:
            logger.debug(f"Autocomplete called with: '{current}'")
            if not current or len(current) <= 2:
                logger.debug("Query too short, returning random items")
                # Show 25 random items when query is too short
                base_items = await self.service.get_random_item_suggestions(25)
            else:
                # Get base item names and IDs using the service
                base_items = await self.service.get_base_item_suggestions(current)
            logger.debug(f"Found {len(base_items)} suggestions: {[name for name, _ in base_items[:5]]}")  # Show first 5
            
            # Return up to 25 choices for autocomplete using item IDs as values
            choices = [
                app_commands.Choice(name=item_name, value=str(item_id))
                for item_name, item_id in base_items[:25]
            ]
            logger.debug(f"Returning {len(choices)} choices")
            return choices
        except Exception as e:
            logger.error(f"Error in item_name_autocomplete: {e}")
            return []

    @app_commands.command(name="lookup", description="Look up a specific ACNH item")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    @app_commands.describe(item="Item name to look up")
    @app_commands.autocomplete(item=item_name_autocomplete)
    async def lookup(self, interaction: discord.Interaction, item: str):
        """Look up a specific item with autocomplete"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            # Check if item is an ID (from autocomplete) or name (typed manually)
            if item.isdigit():
                # Direct lookup by ID from autocomplete selection
                result = await self.service.get_item_by_id(int(item))
                if result:
                    results = [result]
                else:
                    results = []
            else:
                # Fallback to search by name for manually typed entries
                results = await self.service.search_all(item, category_filter="items")
            
            if not results:
                embed = discord.Embed(
                    title="🔍 No Results",
                    description=f"No items found matching '{item}'",
                    color=0xe74c3c
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # If exactly one result, show detailed view with variant selector
            if len(results) == 1:
                result = results[0]
                if hasattr(result, 'variants') and result.variants:
                    # Multiple variants - show selector
                    embed = result.to_discord_embed()
                    view = VariantSelectView(result, interaction.user)
                    await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
                else:
                    # Single item - show directly
                    embed = result.to_discord_embed()
                    await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Multiple results - show search-style list with pagination
            embed = discord.Embed(
                title=f"🔍 Lookup Results for '{item}'",
                color=0x3498db
            )
            
            # Create paginated view for multiple results
            paginated_view = PaginatedResultView(results, embed_title=f"🔍 Lookup Results for '{item}'")
            embed = paginated_view.create_page_embed()
            
            await interaction.followup.send(embed=embed, view=paginated_view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in lookup command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the item.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="villager", description="Look up a specific ACNH villager")
    @app_commands.describe(name="The villager name to look up")
    @app_commands.autocomplete(name=villager_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def villager(self, interaction: discord.Interaction, name: str):
        """Look up villager details"""
        await interaction.response.defer(thinking=True)
        
        # Check if this is a DM for ephemeral logic
        ephemeral = not is_dm(interaction)
        
        try:
            # Convert name to villager ID if it's numeric (from autocomplete)
            if name.isdigit():
                villager_id = int(name)
                villager = await self.service.get_villager_by_id(villager_id)
            else:
                # Search for villager by name
                search_results = await self.service.search(name, limit=50)
                villagers = [r for r in search_results if hasattr(r, 'species')]  # Filter for villagers
                villager = villagers[0] if villagers else None
            
            if not villager:
                embed = discord.Embed(
                    title="❌ Villager Not Found",
                    description=f"Sorry, I couldn't find a villager named **{name}** 😿\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Create the main villager embed with extra details button
            embed = villager.to_discord_embed()
            
            # Create a view with buttons for additional details
            view = VillagerDetailsView(villager, interaction.user, self.service)
            
            await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in villager command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the villager.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="recipe", description="Look up a specific ACNH recipe")
    @app_commands.describe(name="The recipe name to look up")
    @app_commands.autocomplete(name=recipe_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def recipe(self, interaction: discord.Interaction, name: str):
        """Look up recipe details"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
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
            
            # Add recipe type info in footer
            recipe_type = "🍳 Food Recipe" if recipe.is_food() else "🛠️ DIY Recipe"
            embed.set_footer(text=f"{recipe_type} • {recipe.category or 'Unknown Category'}")
            
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in recipe command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the recipe.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="artwork", description="Look up a specific ACNH artwork")
    @app_commands.describe(name="The artwork name to look up")
    @app_commands.autocomplete(name=artwork_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def artwork(self, interaction: discord.Interaction, name: str):
        """Look up artwork details"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            # Convert name to artwork ID if it's numeric (from autocomplete)
            if name.isdigit():
                artwork_id = int(name)
                artwork = await self.service.get_artwork_by_id(artwork_id)
            else:
                # Search for artwork by name
                search_results = await self.service.search_all(name, category_filter="artwork")
                artwork = search_results[0] if search_results else None
            
            if not artwork:
                embed = discord.Embed(
                    title="❌ Artwork Not Found",
                    description=f"Sorry, I couldn't find artwork named **{name}** 😿\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                
                # Add suggestion for genuine vs fake
                embed.add_field(
                    name="💡 Search Tips",
                    value="• Artwork comes in genuine and fake versions\n"
                          "• Use the artwork name without 'genuine' or 'fake'\n"
                          "• Try `/search` with partial names or artist names",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Create the artwork embed
            embed = artwork.to_discord_embed()
            
            # Add artwork category info in footer
            authenticity = "Genuine" if artwork.genuine else "Fake"
            category_text = f"🎨 {authenticity} Artwork"
            if artwork.art_category:
                category_text += f" • {artwork.art_category}"
            embed.set_footer(text=category_text)
            
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in artwork command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the artwork.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="critter", description="Look up a specific ACNH critter (fish, bug, or sea creature)")
    @app_commands.describe(name="The critter name to look up")
    @app_commands.autocomplete(name=critter_name_autocomplete)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def critter(self, interaction: discord.Interaction, name: str):
        """Look up critter details"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        try:
            # Convert name to critter ID if it's numeric (from autocomplete)
            if name.isdigit():
                critter_id = int(name)
                critter = await self.service.get_critter_by_id(critter_id)
            else:
                # Search for critter by name
                search_results = await self.service.search_all(name, category_filter="critters")
                critter = search_results[0] if search_results else None
            
            if not critter:
                embed = discord.Embed(
                    title="❌ Critter Not Found",
                    description=f"Sorry, I couldn't find a critter named **{name}** 😿\n"
                               f"Try using `/search {name}` to see if there are similar names.",
                    color=0xe74c3c
                )
                
                # Add suggestion for different critter types
                embed.add_field(
                    name="💡 Search Tips",
                    value="• 🐟 Fish: Found in rivers, ponds, and the sea\n"
                          "• 🦋 Bugs: Found around flowers, trees, and rocks\n"
                          "• 🌊 Sea Creatures: Found while diving in the ocean\n"
                          "• Try `/search` with partial names or locations",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=ephemeral)
                return
            
            # Create the critter embed
            embed = critter.to_discord_embed()
            
            # Add critter type info in footer
            critter_type = {
                'fish': '🐟 Fish',
                'insect': '🦋 Bug', 
                'sea': '🌊 Sea Creature'
            }.get(critter.kind, critter.kind.title())
            
            footer_text = f"{critter_type}"
            if critter.location:
                footer_text += f" • {critter.location}"
            embed.set_footer(text=footer_text)
            
            # Create a view with availability button
            view = CritterAvailabilityView(critter, interaction.user)
            
            await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
            
        except Exception as e:
            logger.error(f"Error in critter command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while looking up the critter.",
                color=0xe74c3c
            )
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)

class VillagerDetailsView(discord.ui.View):
    """View for showing additional villager details with navigation"""
    
    def __init__(self, villager, interaction_user: discord.Member, service, current_view: str = "main"):
        super().__init__(timeout=300)
        self.villager = villager
        self.interaction_user = interaction_user
        self.service = service
        self.current_view = current_view
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the original user to interact"""
        return interaction.user == self.interaction_user
    
    async def resolve_clothing_name(self, clothing_id_str: str) -> str:
        """Resolve clothing ID to name"""
        try:
            # If it's already a name (contains spaces or letters), return as-is
            if not clothing_id_str.isdigit():
                return clothing_id_str
            
            # Try to convert to int and resolve name by internal IDs
            clothing_id = int(clothing_id_str)
            
            # Try internal_id/internal_group_id first (more likely for villager references)
            clothing_name = await self.service.get_item_name_by_internal_id(clothing_id)
            
            # If that didn't work, try regular table ID as fallback
            if not clothing_name:
                clothing_name = await self.service.get_item_name_by_id(clothing_id)
            
            # Debug log to see what's happening
            logger.debug(f"Resolving ID {clothing_id}: found name '{clothing_name}'")
            
            return clothing_name if clothing_name else f"Unknown Item ({clothing_id})"
        except (ValueError, TypeError) as e:
            logger.error(f"Error resolving clothing ID {clothing_id_str}: {e}")
            return clothing_id_str
    
    def get_embed_for_view(self, view_type: str) -> discord.Embed:
        """Get the appropriate embed based on view type"""
        if view_type == "house":
            embed = discord.Embed(
                title=f"🏠 {self.villager.name}'s House",
                color=discord.Color.blue()
            )
            
            house_info = []
            if self.villager.wallpaper:
                house_info.append(f"**Wallpaper:** {self.villager.wallpaper}")
            if self.villager.flooring:
                house_info.append(f"**Flooring:** {self.villager.flooring}")
            if self.villager.furniture_name_list:
                house_info.append(f"**Furniture:** {self.villager.furniture_name_list}")
            
            if house_info:
                embed.description = "\n".join(house_info)
            else:
                embed.description = "No house details available."
            
            # Set house image if available
            if self.villager.house_image:
                embed.set_image(url=self.villager.house_image)
                
        elif view_type == "clothing":
            embed = discord.Embed(
                title=f"👕 {self.villager.name}'s Style",
                color=discord.Color.green()
            )
            
            clothing_info = []
            if self.villager.default_clothing:
                clothing_info.append(f"**Default Clothing:** {self.villager.default_clothing}")
            if self.villager.default_umbrella:
                clothing_info.append(f"**Default Umbrella:** {self.villager.default_umbrella}")
            
            if clothing_info:
                embed.description = "\n".join(clothing_info)
            else:
                embed.description = "No clothing details available."
                
        elif view_type == "other":
            embed = discord.Embed(
                title=f"🔧 {self.villager.name}'s Other Details",
                color=discord.Color.orange()
            )
            
            other_info = []
            if self.villager.diy_workbench:
                other_info.append(f"**DIY Workbench:** {self.villager.diy_workbench}")
            if self.villager.kitchen_equipment:
                other_info.append(f"**Kitchen Equipment:** {self.villager.kitchen_equipment}")
            if self.villager.version_added:
                other_info.append(f"**Version Added:** {self.villager.version_added}")
            if self.villager.subtype:
                other_info.append(f"**Subtype:** {self.villager.subtype}")
            
            if other_info:
                embed.description = "\n".join(other_info)
            else:
                embed.description = "No additional details available."
                
        else:  # main view
            embed = self.villager.to_discord_embed()
        
        return embed
    
    @discord.ui.button(label="🏘️ About", style=discord.ButtonStyle.primary)
    async def about_villager(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show main villager info"""
        self.current_view = "main"
        embed = self.get_embed_for_view("main")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🏠 House", style=discord.ButtonStyle.secondary)
    async def house_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show house details"""
        self.current_view = "house"
        embed = self.get_embed_for_view("house")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="👕 Clothing", style=discord.ButtonStyle.secondary)
    async def clothing_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show clothing details"""
        self.current_view = "clothing"
        
        # Create clothing embed with resolved names
        embed = discord.Embed(
            title=f"👕 {self.villager.name}'s Style",
            color=discord.Color.green()
        )
        
        clothing_info = []
        if self.villager.default_clothing:
            clothing_name = await self.resolve_clothing_name(self.villager.default_clothing)
            clothing_info.append(f"**Default Clothing:** {clothing_name}")
        if self.villager.default_umbrella:
            umbrella_name = await self.resolve_clothing_name(self.villager.default_umbrella)
            clothing_info.append(f"**Default Umbrella:** {umbrella_name}")
        
        if clothing_info:
            embed.description = "\n".join(clothing_info)
        else:
            embed.description = "No clothing details available."
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🔧 Other", style=discord.ButtonStyle.secondary)
    async def other_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show other details"""
        self.current_view = "other"
        embed = self.get_embed_for_view("other")
        await interaction.response.edit_message(embed=embed, view=self)

class CritterAvailabilityView(discord.ui.View):
    """View for showing critter availability with hemisphere and month selection"""
    
    def __init__(self, critter, interaction_user: discord.Member, show_availability: bool = False):
        super().__init__(timeout=300)
        self.critter = critter
        self.interaction_user = interaction_user
        self.current_hemisphere = "NH"  # Default to Northern Hemisphere
        self.current_month = "jan"  # Default to January
        self.show_availability = show_availability
        
        # Add appropriate buttons based on mode
        if show_availability:
            self.add_availability_controls()
            self.add_back_button()
        else:
            self.add_view_availability_button()
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the original user to interact"""
        return interaction.user == self.interaction_user
    
    def get_availability_embed(self) -> discord.Embed:
        """Create embed showing availability for selected hemisphere and month"""
        embed = discord.Embed(
            title=f"🗓️ {self.critter.name} Availability",
            color=discord.Color.green()
        )
        
        # Get hemisphere display name
        hemisphere_name = "Northern Hemisphere" if self.current_hemisphere == "NH" else "Southern Hemisphere"
        
        # Get month display name
        month_names = {
            "jan": "January", "feb": "February", "mar": "March", "apr": "April",
            "may": "May", "jun": "June", "jul": "July", "aug": "August",
            "sep": "September", "oct": "October", "nov": "November", "dec": "December"
        }
        month_name = month_names.get(self.current_month, self.current_month.title())
        
        embed.description = f"**Hemisphere:** {hemisphere_name}\n**Month:** {month_name}"
        
        # Get availability for current selection
        field_name = f"{self.current_hemisphere.lower()}_{self.current_month}"
        availability = getattr(self.critter, field_name, None)
        
        if availability and availability.lower() not in ['none', 'null', '']:
            # Available - show the time information
            embed.add_field(
                name="✅ Available", 
                value=f"{self.critter.name} is available in {month_name}!\n**Time:** {availability}", 
                inline=False
            )
            embed.color = discord.Color.green()
        elif availability and availability.lower() in ['none', 'null']:
            # Not available
            embed.add_field(
                name="❌ Not Available", 
                value=f"{self.critter.name} is not available in {month_name}.", 
                inline=False
            )
            embed.color = discord.Color.red()
        else:
            embed.add_field(name="❓ Unknown", value="Availability data not found.", inline=False)
            embed.color = discord.Color.orange()
        
        # Add full year overview
        year_data = []
        for month in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]:
            field = f"{self.current_hemisphere.lower()}_{month}"
            month_avail = getattr(self.critter, field, None)
            if month_avail and month_avail.lower() not in ['none', 'null', '']:
                year_data.append(f"✅ {month_names[month][:3]}")
            else:
                year_data.append(f"❌ {month_names[month][:3]}")
        
        # Split into quarters for better formatting
        quarters = [year_data[i:i+3] for i in range(0, 12, 3)]
        year_overview = "\n".join([" ".join(quarter) for quarter in quarters])
        
        embed.add_field(
            name=f"📅 Full Year Overview ({hemisphere_name})",
            value=f"```\n{year_overview}\n```",
            inline=False
        )
        
        # Add additional info if available
        info_lines = []
        if self.critter.time_of_day:
            info_lines.append(f"**Time:** {self.critter.time_of_day}")
        if self.critter.location:
            info_lines.append(f"**Location:** {self.critter.location}")
        if self.critter.weather:
            info_lines.append(f"**Weather:** {self.critter.weather}")
        
        if info_lines:
            embed.add_field(name="ℹ️ Additional Info", value="\n".join(info_lines), inline=False)
        
        return embed
    
    def add_availability_controls(self):
        """Add hemisphere and month selects for availability view"""
        hemisphere_select = discord.ui.Select(
            placeholder="Choose hemisphere...",
            options=[
                discord.SelectOption(label="Northern Hemisphere", value="NH", emoji="🌎"),
                discord.SelectOption(label="Southern Hemisphere", value="SH", emoji="🌏")
            ],
            row=0
        )
        hemisphere_select.callback = self.hemisphere_callback
        
        month_select = discord.ui.Select(
            placeholder="Choose month...",
            options=[
                discord.SelectOption(label="January", value="jan"),
                discord.SelectOption(label="February", value="feb"),
                discord.SelectOption(label="March", value="mar"),
                discord.SelectOption(label="April", value="apr"),
                discord.SelectOption(label="May", value="may"),
                discord.SelectOption(label="June", value="jun"),
                discord.SelectOption(label="July", value="jul"),
                discord.SelectOption(label="August", value="aug"),
                discord.SelectOption(label="September", value="sep"),
                discord.SelectOption(label="October", value="oct"),
                discord.SelectOption(label="November", value="nov"),
                discord.SelectOption(label="December", value="dec")
            ],
            row=1
        )
        month_select.callback = self.month_callback
        
        self.add_item(hemisphere_select)
        self.add_item(month_select)
    
    async def hemisphere_callback(self, interaction: discord.Interaction):
        """Handle hemisphere selection"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            
        self.current_hemisphere = interaction.data['values'][0]
        embed = self.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def month_callback(self, interaction: discord.Interaction):
        """Handle month selection"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            
        self.current_month = interaction.data['values'][0]
        embed = self.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    def add_back_button(self):
        """Add only the back to details button"""
        back_button = discord.ui.Button(label="📋 Back to Details", style=discord.ButtonStyle.secondary, row=2)
        back_button.callback = self.back_callback
        self.add_item(back_button)
    
    def add_view_availability_button(self):
        """Add only the view availability button"""
        availability_button = discord.ui.Button(label="🗓️ View Availability", style=discord.ButtonStyle.primary)
        availability_button.callback = self.availability_callback
        self.add_item(availability_button)
    
    async def back_callback(self, interaction: discord.Interaction):
        """Go back to the main critter details"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            
        embed = self.critter.to_discord_embed()
        
        # Add critter type info in footer
        critter_type = {
            'fish': '🐟 Fish',
            'insect': '🦋 Bug', 
            'sea': '🌊 Sea Creature'
        }.get(self.critter.kind, self.critter.kind.title())
        
        footer_text = f"{critter_type}"
        if self.critter.location:
            footer_text += f" • {self.critter.location}"
        embed.set_footer(text=footer_text)
        
        # Create a new view with only the availability button (no selects)
        view = CritterAvailabilityView(self.critter, self.interaction_user, show_availability=False)
        view.clear_items()
        view.add_view_availability_button()
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def availability_callback(self, interaction: discord.Interaction):
        """Show availability interface"""
        if interaction.user.id != self.interaction_user.id:
            await interaction.response.send_message("Only the user who initiated this command can use these controls.", ephemeral=True)
            return
            
        # Create new view with availability controls
        view = CritterAvailabilityView(self.critter, self.interaction_user, show_availability=True)
        
        embed = view.get_availability_embed()
        await interaction.response.edit_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    """Setup function for the cog"""
    await bot.add_cog(ACNHCommands(bot))