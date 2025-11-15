import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help cog ready")

    @app_commands.command(name="help", description="Show information about available commands")
    async def help(self, interaction: discord.Interaction):
        """Display help information about all available commands"""
        await interaction.response.defer(thinking=True)
        
        embed = discord.Embed(
            title="🏝️ NookLook - Help",
            description="Look up Animal Crossing: New Horizons items with hex codes, prices, and images!",
            color=discord.Color.green()
        )
        
        # Commands
        embed.add_field(
            name="� Commands",
            value=(
                "**`/lookup furniture <name>`** - Furniture & housewares\n"
                "**`/lookup clothing <name>`** - Clothing & accessories\n"  
                "**`/lookup tools <name>`** - Tools & gadgets\n"
                "**`/lookup collectables <name>`** - DIY materials & plants\n"
                "**`/search <name> [category]`** - Search across categories\n"
                "**`/info`** - Bot statistics"
            ),
            inline=False
        )
        
        # Quick Tips
        embed.add_field(
            name="💡 Tips",
            value=(
                "• Use autocomplete for item names\n"
                "• Some color variants have different hex codes!\n"
                "• Try `/search` if you can't find an exact match"
            ),
            inline=False
        )
        
        embed.set_footer(text="Example: /lookup clothing pleather pants")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="info", description="Show bot information and statistics")
    async def info(self, interaction: discord.Interaction):
        """Display bot information and database statistics"""
        await interaction.response.defer(thinking=True)
        
        # Get database statistics
        try:
            total_result = await self.bot.acnh_service.repo.db.execute_query("SELECT COUNT(*) as count FROM acnh_items")
            total_items = total_result[0]['count']
            
            hex_result = await self.bot.acnh_service.repo.db.execute_query("SELECT COUNT(*) as count FROM acnh_items WHERE hex_id IS NOT NULL AND hex_id != ''")
            hex_items = hex_result[0]['count']
            
            image_result = await self.bot.acnh_service.repo.db.execute_query("SELECT COUNT(*) as count FROM acnh_items WHERE image_url IS NOT NULL AND image_url != ''")
            image_items = image_result[0]['count']
            
            # Get category breakdown
            category_result = await self.bot.acnh_service.repo.db.execute_query("""
                SELECT category, COUNT(*) as count 
                FROM acnh_items 
                GROUP BY category 
                ORDER BY count DESC
            """)
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            total_items = hex_items = image_items = 0
            category_result = []
        
        embed = discord.Embed(
            title="NookLook - Information",
            description="A comprehensive Animal Crossing: New Horizons item database bot",
            color=discord.Color.blue()
        )
        
        # Bot Statistics
        embed.add_field(
            name="Database Statistics",
            value=(
                f"**Total Items**: {total_items:,}\n"
                f"**Items with Hex Codes**: {hex_items:,} ({hex_items/total_items*100:.1f}%)\n"
                f"**Items with Images**: {image_items:,} ({image_items/total_items*100:.1f}%)\n"
            ),
            inline=True
        )
        
        # Category Breakdown
        if category_result:
            category_text = "\n".join([f"**{cat['category']}**: {cat['count']:,}" for cat in category_result[:8]])
            if len(category_result) > 8:
                remaining = sum(cat['count'] for cat in category_result[8:])
                category_text += f"\n**Other**: {remaining:,}"
        else:
            category_text = "Unable to load category data"
            
        embed.add_field(
            name="📦 Categories",
            value=category_text,
            inline=True
        )
        
        # Features
        embed.add_field(
            name="Features",
            value=(
                "• Color-specific hex codes\n"
                "• High-quality item images\n"
                "• Comprehensive item data\n"
                "• Smart search & autocomplete\n"
                "• Variant-aware lookups\n"
                "• Real ACNH data"
            ),
            inline=False
        )
        
        
        embed.set_footer(text="Made with 💖 for the ACNH community")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))