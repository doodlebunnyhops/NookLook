import discord
from discord.ext import commands
from discord import app_commands

def is_dm(interaction: discord.Interaction) -> bool:
    """Check if interaction is in a DM or Group DM (both have guild=None)"""
    return interaction.guild is None

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help cog ready")

    @app_commands.command(name="help", description="Show information about available commands")
    async def help(self, interaction: discord.Interaction):
        """Display help information about all available commands"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        embed = discord.Embed(
            title="🏝️ NookLook - Help",
            description="Look up Animal Crossing: New Horizons items with hex codes, prices, and images!",
            color=discord.Color.green()
        )
        
        # Commands
        embed.add_field(
            name="📋 Commands",
            value=(
                "**`/lookup <item>`** - Look up any ACNH item with autocomplete\n"
                "**`/search <query> [category]`** - Search across all ACNH content\n"
                "**`/browse items [filters]`** - Browse items with category/color/price filters\n"
                "**`/help`** - Show this help message"
            ),
            inline=False
        ),
        
        # Quick Tips
        embed.add_field(
            name="💡 Tips",
            value=(
                "• `/lookup` shows random items when you start typing\n"
                "• Use variant selectors to see different color options\n"
                "• All responses are private in servers, normal in DMs\n"
                "• Search supports exact phrase matching for precise results"
            ),
            inline=False
        ),
        
        embed.set_footer(text="Example: /lookup apple chair")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        await interaction.followup.send(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="info", description="Show bot information and statistics")
    async def info(self, interaction: discord.Interaction):
        """Display bot information and database statistics"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        # Get database statistics using the service method
        try:
            # Access the service through the nooklook commands cog
            nooklook_cog = self.bot.get_cog('ACNHCommands')
            if nooklook_cog:
                stats = await nooklook_cog.service.get_database_stats()
                total_items = stats.get('items', 0)
                total_critters = stats.get('critters', 0)
                total_recipes = stats.get('recipes', 0)
                total_villagers = stats.get('villagers', 0)
                total_content = stats.get('total_content', 0)
            else:
                total_items = total_critters = total_recipes = total_villagers = total_content = 0
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            total_items = total_critters = total_recipes = total_villagers = total_content = 0
        
        embed = discord.Embed(
            title="NookLook - Information",
            description="A comprehensive Animal Crossing: New Horizons item database bot",
            color=discord.Color.blue()
        )
        
        # Bot Statistics
        embed.add_field(
            name="📊 Database Statistics",
            value=(
                f"**🏠 Items**: {total_items:,}\n"
                f"**🐛 Critters**: {total_critters:,}\n"
                f"**🛠️ Recipes**: {total_recipes:,}\n"
                f"**👥 Villagers**: {total_villagers:,}\n"
                f"**📦 Total Content**: {total_content:,}"
            ),
            inline=True
        ),
        
        # Features
        embed.add_field(
            name="✨ Features",
            value=(
                "• Smart autocomplete with random suggestions\n"
                "• Variant selection for color/pattern options\n"
                "• Full-text search across all content\n"
                "• Item filtering by category, color, price\n"
                "• TI customize codes and hex values\n"
                "• Private responses in servers\n"
                "• Real ACNH database with 5,850+ items"
            ),
            inline=False
        )
        
        embed.set_footer(text="Made with 💖 for the ACNH community | Use /help for command details")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        await interaction.followup.send(embed=embed, ephemeral=ephemeral)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))