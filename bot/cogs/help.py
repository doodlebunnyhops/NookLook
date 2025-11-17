import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

def is_dm(interaction: discord.Interaction) -> bool:
    """Check if interaction is in a DM or Group DM (both have guild=None)"""
    return interaction.guild is None

class HelpDropdown(discord.ui.Select):
    """Dropdown selector for detailed command help"""
    
    def __init__(self):
        options = [
            discord.SelectOption(
                label="🔍 Search Command",
                description="Search across all ACNH content with filters",
                value="search"
            ),
            discord.SelectOption(
                label="🏠 Lookup Command", 
                description="Look up specific items with variants",
                value="lookup"
            ),
            discord.SelectOption(
                label="👥 Villager Command",
                description="Find villager details and preferences", 
                value="villager"
            ),
            discord.SelectOption(
                label="🍳 Recipe Command",
                description="Look up DIY and food recipes",
                value="recipe"
            ),
            discord.SelectOption(
                label="🎨 Artwork Command", 
                description="Find genuine and fake artwork",
                value="artwork"
            ),
            discord.SelectOption(
                label="🐛 Critter Command",
                description="Fish, bugs, and sea creature info",
                value="critter"
            )
        ]
        
        super().__init__(
            placeholder="Select a command for detailed help...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle dropdown selection"""
        command = self.values[0]
        ephemeral = not is_dm(interaction)
        
        embed = discord.Embed(color=discord.Color.green())
        
        if command == "search":
            embed.title = "🔍 Search Command"
            embed.description = "**Usage:** `/search <query> [category]`\n\nSearch across all ACNH content using advanced text search. Supports partial matching and category filtering."
            embed.add_field(
                name="Categories",
                value="• **Items** - Furniture, clothing, tools\n• **Critters** - Fish, bugs, sea creatures\n• **Food Recipes** - Cooking recipes only\n• **DIY Recipes** - Crafting recipes only\n• **Villagers** - All villager residents",
                inline=False
            )
            embed.add_field(
                name="Examples",
                value="`/search apple` - Returns items, recipes, and villagers!\n`/search apple category:Items` - Just the apple chair and apple TV\n`/search apple category:Food Recipes` - Just the apple pie recipe\n`/search bass category:Critters` - Find bass fish only",
                inline=False
            )
            
        elif command == "lookup":
            embed.title = "🏠 Lookup Command"
            embed.description = "**Usage:** `/lookup <item>`\n\nLook up specific items with autocomplete suggestions. Shows variants, prices, and customization options."
            embed.add_field(
                name="Discoverable Item Types",
                value="• **Furniture:** Housewares, wall-mounted, ceiling-decor, interior-structures\n• **Clothing:** Tops, bottoms, dress-up, headwear, accessories, bags, shoes, socks, umbrellas\n• **Decor:** Wallpaper, floors, rugs, fencing, photos, posters, music\n• **Other:** Tools-goods, gyroids, miscellaneous, clothing-other",
                inline=False
            )
            embed.add_field(
                name="Features",
                value="• Smart autocomplete with random suggestions\n• Variant selector for colors/patterns\n• Price and source information\n• Customization details\n• Item hex codes for Treasure Island use",
                inline=False
            )
            embed.add_field(
                name="Examples",
                value="`/lookup apple chair` - Look up the apple chair\n`/lookup` (then type) - See autocomplete suggestions",
                inline=False
            )
            
        elif command == "villager":
            embed.title = "👥 Villager Command" 
            embed.description = "**Usage:** `/villager <name>`\n\nFind detailed information about any ACNH villager including personality, preferences, and house details."
            embed.add_field(
                name="What You'll See",
                value="• Basic info (species, personality, birthday)\n• Style and color preferences\n• House interior (wallpaper, flooring, furniture)\n• Clothing preferences\n• Favorite song and sayings",
                inline=False
            )
            embed.add_field(
                name="Examples",
                value="`/villager marshal` - Look up Marshal\n`/villager` (then type) - See autocomplete suggestions",
                inline=False
            )
            
        elif command == "recipe":
            embed.title = "🍳 Recipe Command"
            embed.description = "**Usage:** `/recipe <name>`\n\nLook up DIY crafting recipes and cooking recipes with ingredients, sources, and categories."
            embed.add_field(
                name="Recipe Types", 
                value="• **Food Recipes** 🍳 - Savory dishes and sweet treats\n• **DIY Recipes** 🛠️ - Furniture, tools, decorations\n• Ingredients list and quantities\n• Source information (where to get)",
                inline=False
            )
            embed.add_field(
                name="Examples",
                value="`/recipe apple pie` - Look up apple pie recipe\n`/recipe wooden chair` - Look up DIY furniture recipe",
                inline=False
            )
            
        elif command == "artwork":
            embed.title = "🎨 Artwork Command"
            embed.description = "**Usage:** `/artwork <name>`\n\nLook up artwork pieces available from Redd, including both genuine and fake versions with authentication details." 
            embed.add_field(
                name="What You'll See",
                value="• Authenticity (genuine/fake)\n• Real artwork title and artist\n• Buy and sell prices\n• Description and source\n• Redd availability",
                inline=False
            )
            embed.add_field(
                name="Examples", 
                value="`/artwork mona lisa` - Look up famous painting\n`/artwork` (then type) - See all available artwork",
                inline=False
            )
            
        elif command == "critter":
            embed.title = "🐛 Critter Command"
            embed.description = "**Usage:** `/critter <name>`\n\nLook up fish, bugs, and sea creatures with seasonal availability, locations, and catching information."
            embed.add_field(
                name="What You'll See",
                value="• Location and time availability\n• Seasonal calendar (Northern/Southern hemisphere)\n• Shadow size and rarity\n• Sell price and museum info\n• Interactive availability viewer",
                inline=False
            )
            embed.add_field(
                name="Examples",
                value="`/critter anchovy` - Look up anchovy fish\n`/critter monarch butterfly` - Look up butterfly info",
                inline=False
            )
        
        # Create new view with the dropdown for continued navigation
        view = HelpDetailView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=ephemeral)

class HelpView(discord.ui.View):
    """View containing the help dropdown"""
    
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(HelpDropdown())

class HelpDetailView(discord.ui.View):
    """View for detailed command help with navigation options"""
    
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(HelpDropdown())
    
    @discord.ui.button(label="📋 Back to Main Help", style=discord.ButtonStyle.secondary, row=1)
    async def back_to_main(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Return to the main help menu"""
        ephemeral = not is_dm(interaction)
        
        embed = discord.Embed(
            title="🏝️ NookLook - Help",
            description="Animal Crossing: New Horizons database bot with items, villagers, recipes, artwork, and critters.",
            color=discord.Color.green()
        )
        
        # Main Commands
        embed.add_field(
            name="Commands",
            value=(
                "`/search` • `/lookup` • `/villager` • `/recipe`\n"
                "`/artwork` • `/critter` • `/help` • `/info`"
            ),
            inline=False
        )
        
        # Quick Start
        embed.add_field(
            name="Get Started",
            value="Try `/lookup` and start typing for suggestions!\nUse the dropdown below for detailed help on any command.",
            inline=False
        )
        
        embed.set_footer(text="💡 Select a command below for examples and details")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        # Create view with dropdown for detailed help
        view = HelpView()
        
        await interaction.response.edit_message(embed=embed, view=view)

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help cog ready")

    @app_commands.command(name="help", description="Show information about available commands")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    async def help(self, interaction: discord.Interaction):
        """Display help information about all available commands"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        embed = discord.Embed(
            title="🏝️ NookLook - Help",
            description="Animal Crossing: New Horizons database bot with items, villagers, recipes, artwork, and critters.",
            color=discord.Color.green()
        )
        
        # Main Commands
        embed.add_field(
            name="📋 Commands",
            value=(
                "`/search` • `/lookup` • `/villager` • `/recipe`\n"
                "`/artwork` • `/critter` • `/help` • `/info`"
            ),
            inline=False
        )
        
        # Quick Start
        embed.add_field(
            name="🚀 Get Started",
            value="Try `/lookup` and start typing for suggestions!\nUse the dropdown below for detailed help on any command.",
            inline=False
        )
        
        embed.set_footer(text="💡 Select a command below for examples and details")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        # Create view with dropdown for detailed help
        view = HelpView()
        
        await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)

    @app_commands.command(name="info", description="Show bot information and statistics")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
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
            name="Database Statistics",
            value=(
                f"**Items**: {total_items:,}\n"
                f"**Critters**: {total_critters:,}\n"
                f"**Recipes**: {total_recipes:,}\n"
                f"**Villagers**: {total_villagers:,}\n"
                f"**Total Content**: {total_content:,}"
            ),
            inline=True
        )
        

        
        # Features
        embed.add_field(
            name="Features",
            value=(
                "Smart search & autocomplete • Color variants & hex codes\n"
                "Seasonal availability • Prices & sources • Villager details"
            ),
            inline=False
        )
        
        # Attribution and Support
        embed.add_field(
            name="Credits & Support",
            value=(
                "**Data Source:** [ACNH Spreadsheet](https://discord.gg/kWMMYrN) community\n"
                "**Support Server:** [BloominWatch](https://discord.gg/fxhXWgxcHV)"
            ),
            inline=False
        )
        
        embed.set_footer(text="Made with 💖 for the ACNH community | Use /help for command details")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        await interaction.followup.send(embed=embed, ephemeral=ephemeral)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))