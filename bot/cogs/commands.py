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
            furniture_items = [item for item in items if item.category in ['Housewares', 'Miscellaneous', 'Wall-mounted']]
            
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
                all_items = await self.bot.acnh_service.repo.get_random_items_by_category(['Tops', 'Bottoms', 'Dresses', 'Headwear', 'Accessories', 'Socks', 'Shoes', 'Bags'], 25)
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
                clothing_items = [item for item in items if item.category in ['Tops', 'Bottoms', 'Dresses', 'Headwear', 'Accessories', 'Socks', 'Shoes', 'Bags']]
                
                # Convert to autocomplete choices (limit to 25 as per Discord API)
                choices = []
                for item in clothing_items[:25]:
                    choices.append(app_commands.Choice(name=item.name, value=item.name))
                
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
                f"Try using `/search furniture {name}` to see similar items.",
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
                f"Try using `/search clothing {name}` to see similar items, or check the spelling.",
                ephemeral=True
            )
            return
        print("Found clothing item:", item.name, "Color variant:", item.color_variant)

        # Use the ACNHItem's built-in Discord embed generation
        embed = item.to_discord_embed()
        await interaction.followup.send(embed=embed)

    # Search command group
    search_group = app_commands.Group(name="search", description="Search for Animal Crossing: New Horizons items")

    @search_group.command(name="furniture", description="Search for furniture items by name pattern")
    @app_commands.describe(pattern="Search pattern (e.g., 'wooden', 'iron', 'chair')")
    @app_commands.autocomplete(pattern=furniture_name_autocomplete)
    async def search_furniture(self, interaction: discord.Interaction, pattern: str):
        await interaction.response.defer(thinking=True)
        
        try:
            # Search for items in the cache
            items = await self.bot.acnh_service.repo.search_items_by_name_fuzzy(pattern)
            
            if not items:
                await interaction.followup.send(
                    f"No furniture items found matching **{pattern}** 🔍\n"
                    f"Try a different search term or use `/lookup furniture <exact_name>` if you know the item name.",
                    ephemeral=True
                )
                return
            
            # Create a search results embed
            embed = discord.Embed(
                title=f"🪑 Furniture Search: '{pattern}'",
                description=f"Found {len(items)} item(s)",
                color=discord.Color.blue()
            )
            
            for i, item in enumerate(items[:10]):  # Limit to 10 results
                value_parts = []
                if item.category:
                    value_parts.append(f"**Category:** {item.category}")
                if item.item_series:
                    value_parts.append(f"**Series:** {item.item_series}")
                if item.sell_price is not None:
                    value_parts.append(f"**Sell:** {item.sell_price:,} Bells")
                
                embed.add_field(
                    name=f"{i+1}. {item.name}",
                    value="\n".join(value_parts) if value_parts else "Item information",
                    inline=False
                )
            
            if len(items) > 10:
                embed.add_field(
                    name="...",
                    value=f"And {len(items) - 10} more results. Try a more specific search.",
                    inline=False
                )
            
            embed.set_footer(text="Use /lookup furniture <name> to get detailed info about a specific item")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            await interaction.followup.send(
                f"Error searching for furniture items: {str(e)}", 
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(ACNH(bot))
