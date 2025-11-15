import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal

class ACNH(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ACNH cog ready")

    async def furniture_name_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Autocomplete for furniture names"""
        if len(current) < 2:
            return []
        
        try:
            # Get furniture items that match the current input
            items = await self.bot.acnh_service.repo.search_items_by_name_fuzzy(current)
            
            # Filter to only furniture categories
            furniture_items = [item for item in items if item.category in ['Housewares']]
            
            # Convert to autocomplete choices (limit to 25 as per Discord API)
            choices = []
            for item in furniture_items[:25]:
                choices.append(app_commands.Choice(name=item.name_normalized, value=item.name_normalized))
            
            return choices
        except Exception as e:
            # If there's an error, return empty list so autocomplete doesn't break
            print(f"Error in furniture autocomplete: {e}")
            return []

    async def clothing_name_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Autocomplete for clothing names"""
        try:
            if len(current) == 0:
                # Show 25 random clothing items when no input
                all_items = await self.bot.acnh_service.repo.get_random_items_by_category(['Tops', 'Bottoms', 'Dress-Up', 'Headwear', 'Accessories'], 25)
                
                choices = []
                for item in all_items:
                    choices.append(app_commands.Choice(name=item.name_normalized, value=item.name_normalized))
                return choices
            elif len(current) < 2:
                return []
            else:
                # Get clothing items that match the current input
                items = await self.bot.acnh_service.repo.search_items_by_name_fuzzy(current)
                
                # Filter to only clothing categories
                clothing_items = [item for item in items if item.category in ['Tops', 'Bottoms', 'Dress-Up', 'Headwear', 'Accessories']]
                
                # Convert to autocomplete choices (limit to 25 as per Discord API)
                choices = []
                for item in clothing_items[:25]:
                    choices.append(app_commands.Choice(name=item.name_normalized, value=item.name_normalized))
                
                return choices
        except Exception as e:
            # If there's an error, return empty list so autocomplete doesn't break
            print(f"Error in clothing autocomplete: {e}")
            return []

    # Main lookup command group
    lookup_group = app_commands.Group(name="lookup", description="Look up Animal Crossing: New Horizons items")

    @lookup_group.command(name="furniture", description="Look up furniture and housewares")
    @app_commands.describe(name="The furniture item name to look up")
    @app_commands.autocomplete(name=furniture_name_autocomplete)
    async def lookup_furniture(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer(thinking=True)

        # Use the service from the bot instance
        item = await self.bot.acnh_service.get_item(name)
        if not item:
            await interaction.followup.send(
                f"Sorry, I couldn't find a furniture item matching **{name}** 😿\n"
                f"Try using `/search {name} category:Housewares` to see similar items.",
                ephemeral=True
            )
            return

        # Use the ACNHItem's built-in Discord embed generation
        embed = item.to_discord_embed()
        await interaction.followup.send(embed=embed)

    @lookup_group.command(name="clothing", description="Look up clothing and apparel")
    @app_commands.describe(name="The clothing item name to look up")
    @app_commands.autocomplete(name=clothing_name_autocomplete)
    async def lookup_clothing(self, interaction: discord.Interaction, name: str):
        """Lookup clothing by name (uses same autocomplete/service as furniture)"""
        await interaction.response.defer(thinking=True)

        # Use the service from the bot instance
        item = await self.bot.acnh_service.get_item(name)
        if not item:
            await interaction.followup.send(
                f"Sorry, I couldn't find a clothing item matching **{name}** 😿\n"
                f"Try using `/search {name}` to see similar items, or check the spelling.",
                ephemeral=True
            )
            return
        print("Found clothing item:", item.name, "Color variant:", item.color_variant)

        # Use the ACNHItem's built-in Discord embed generation
        embed = item.to_discord_embed()
        await interaction.followup.send(embed=embed)



    @app_commands.command(name="search", description="Search for items across all categories")
    @app_commands.describe(
        name="Item name to search for",
        category="Optional: Filter by specific category"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="All Categories", value="All"),
        app_commands.Choice(name="Accessories", value="Accessories"),
        app_commands.Choice(name="Bottoms", value="Bottoms"),
        app_commands.Choice(name="Dress-Up", value="Dress-Up"),
        app_commands.Choice(name="Headwear", value="Headwear"),
        app_commands.Choice(name="Housewares", value="Housewares"),
        app_commands.Choice(name="Tops", value="Tops")
    ])
    async def search(self, interaction: discord.Interaction, name: str, category: str = "All"):
        """Search for items across all categories"""
        await interaction.response.defer(thinking=True)
        
        try:
            # Search for items in the cache
            items = await self.bot.acnh_service.repo.search_items_by_base_name_fuzzy(name)
            
            # Filter by category if specified
            if category != "All":
                items = [item for item in items if item.category == category]
            
            if not items:
                category_text = f" in category **{category}**" if category != "All" else ""
                await interaction.followup.send(
                    f"No items found matching **{name}**{category_text} 🔍\n"
                    f"Try a different search term or check your spelling.",
                    ephemeral=True
                )
                return
            
            # Group items by category and base name (without color variants)
            category_items = {}
            for item in items:
                # Extract base name (remove color variant part)
                base_name = item.name
                if ' (' in base_name and base_name.endswith(')'):
                    base_name = base_name.split(' (')[0]
                
                if item.category not in category_items:
                    category_items[item.category] = {}
                
                if base_name not in category_items[item.category]:
                    category_items[item.category][base_name] = []
                category_items[item.category][base_name].append(item)
            
            # Create a search results embed
            category_filter_text = f" in {category}" if category != "All" else ""
            embed = discord.Embed(
                title=f"🔍 Search Results: '{name}'{category_filter_text}",
                description=f"Found items in {len(category_items)} categor{'y' if len(category_items) == 1 else 'ies'}",
                color=discord.Color.blue()
            )
            
            total_shown = 0
            # If filtering by specific category, allow up to 15 results; otherwise 3 per category with 15 total max
            max_per_category = 15 if category != "All" else 3
            max_total = 15
            
            for cat_name, base_items in category_items.items():
                if total_shown >= max_total:
                    break
                    
                # Category emoji
                category_emoji = "👕" if cat_name in ["Bottoms", "Tops", "Dress-Up", "Accessories", "Headwear"] else "🪑" if cat_name == "Housewares" else "📦"
                
                # Show items in this category
                category_results = []
                shown_in_category = 0
                for base_name, color_variants in base_items.items():
                    if shown_in_category >= max_per_category or total_shown >= max_total:
                        break
                    
                    sample_item = color_variants[0]  # Use first variant as sample
                    
                    item_info = base_name
                    if len(color_variants) > 1:
                        item_info += f" ({len(color_variants)} variants)"
                    # if sample_item.sell_price is not None:
                    #     item_info += f" - {sample_item.sell_price:,} Bells"
                    
                    category_results.append(item_info)
                    shown_in_category += 1
                    total_shown += 1
                
                # Add remaining count if there are more items in this category
                remaining = len(base_items) - shown_in_category
                if remaining > 0:
                    category_results.append(f"...and {remaining} more")
                
                embed.add_field(
                    name=f"{category_emoji} {cat_name} ({len(base_items)} items)",
                    value="\n".join(category_results),
                    inline=False
                )
            
            embed.set_footer(text="Use /lookup clothing or /lookup furniture with the exact name to see detailed info")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            await interaction.followup.send(
                f"Error searching for items: {str(e)}", 
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(ACNH(bot))
