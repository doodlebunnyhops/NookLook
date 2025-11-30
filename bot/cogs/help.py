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
                label="Search Command",
                description="Search across all ACNH content with filters",
                value="search"
            ),
            discord.SelectOption(
                label="Lookup Command", 
                description="Look up specific items with variants",
                value="lookup"
            ),
            discord.SelectOption(
                label="Villager Command",
                description="Find villager details and preferences", 
                value="villager"
            ),
            discord.SelectOption(
                label="Recipe Command",
                description="Look up DIY and food recipes",
                value="recipe"
            ),
            discord.SelectOption(
                label="Artwork Command", 
                description="Find genuine and fake artwork",
                value="artwork"
            ),
            discord.SelectOption(
                label="Critter Command",
                description="Fish, bugs, and sea creature info",
                value="critter"
            ),
            discord.SelectOption(
                label="Stash Commands",
                description="Save items to personal stashes for later",
                value="stash"
            ),
            discord.SelectOption(
                label="Server Settings",
                description="Guild management and configuration",
                value="server"
            ),
            discord.SelectOption(
                label="Bot Installation Types",
                description="Guild vs User install differences",
                value="installation"
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
            embed.title = "Search Command"
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
            embed.title = "Lookup Command"
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
            embed.title = "Villager Command" 
            embed.description = "**Usage:** `/villager <name>`\n\nFind detailed information about any ACNH villager including personality, preferences, and house details."
            embed.add_field(
                name="What You'll See",
                value="• Basic info (species, personality, birthday)\n• Style and color preferences\n• House interior (wallpaper, flooring, furniture)\n• Clothing preferences and default items\n• DIY Workbench and Kitchen Equipment with variants\n• Favorite song and sayings",
                inline=False
            )
            embed.add_field(
                name="Examples",
                value="`/villager marshal` - Look up Marshal\n`/villager` (then type) - See autocomplete suggestions",
                inline=False
            )
            
        elif command == "recipe":
            embed.title = "Recipe Command"
            embed.description = "**Usage:** `/recipe <name>`\n\nLook up DIY crafting recipes and cooking recipes with ingredients, sources, and categories."
            embed.add_field(
                name="Recipe Types", 
                value="• **Food Recipes** - Savory dishes and sweet treats\n• **DIY Recipes** - Furniture, tools, decorations\n• Ingredients list and quantities\n• Source information (where to get)",
                inline=False
            )
            embed.add_field(
                name="Examples",
                value="`/recipe apple pie` - Look up apple pie recipe\n`/recipe wooden chair` - Look up DIY furniture recipe",
                inline=False
            )
            
        elif command == "artwork":
            embed.title = "Artwork Command"
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
            embed.title = "Critter Command"
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
            
        elif command == "stash":
            embed.title = "Stash Commands"
            embed.description = "Save items to personal collections for quick reference later. Stashes are private and work in servers and DMs."
            embed.add_field(
                name="Managing Stashes",
                value="• `/stash create <name>` - Create a new stash\n• `/stash rename <stash> <new_name>` - Rename a stash\n• `/stash delete <stash>` - Delete a stash and its contents\n• `/stash remove <stash>` - Remove multiple items at once",
                inline=False
            )
            embed.add_field(
                name="Viewing & Using Stashes",
                value="• `/stash view <stash>` - Browse items in a stash\n• Use the **Add to Stash** button on any lookup result\n• Choose quantity when adding (1, 5, 10, 20, 40)\n• Navigate through saved items with ◀ ▶ buttons\n• **Full List** shows all items with quantities",
                inline=False
            )
            embed.add_field(
                name="Treasure Islands Integration",
                value="• **TI Order** button generates `$order` commands for [Treasure Islands](https://discord.gg/treasureislands)\n• *Note: Treasure Islands does not endorse NookLook. This feature is for personal convenience only.*",
                inline=False
            )
            embed.add_field(
                name="Quick Add Feature",
                value="• If you only have one stash, items auto-add to it\n• With multiple stashes, you'll pick which one\n• Each item saves with its current variant\n• Duplicates allowed for Treasure Island orders",
                inline=False
            )
            
        elif command == "server":
            embed.title = "Server Settings Commands"
            embed.description = "**Usage:** `/server <subcommand>`\n\nManage server-specific bot configuration. **Admin/Owner only** and requires **Guild Installation**."
            embed.add_field(
                name="Available Commands",
                value="• `/server settings` - View current server configuration\n• `/server hide_responses <true/false>` - Configure response visibility",
                inline=False
            )
            embed.add_field(
                name="Response Visibility",
                value="• **Hidden (true)** - Only command user sees bot responses (ephemeral)\n• **Visible (false)** - Everyone in channel sees bot responses\n• **Default:** Hidden for safety when bot joins new servers",
                inline=False
            )
            embed.add_field(
                name="Requirements",
                value="• Server Administrator or Owner permissions\n• Bot must be **Guild Installed** (not User Installed)\n• Only works in server channels, not DMs",
                inline=False
            )
            
        elif command == "installation":
            embed.title = "Bot Installation Types"
            embed.description = "Understanding the difference between Guild and User installations and how they affect bot functionality."
            embed.add_field(
                name="Guild Installation (Recommended)",
                value="• Bot is installed **to the server** by admins\n• All server members can use commands\n• Server settings and configuration available\n• Admins can control response visibility\n• Bot appears in server member list",
                inline=False
            )
            embed.add_field(
                name="User Installation",
                value="• Bot is installed **to your account** personally\n• You can use the bot **anywhere** - any server, DMs, group chats\n• **In Guilds:** Only you see responses (ephemeral) unless guild has it installed with public settings\n• **In DMs/Groups:** Responses always visible to everyone in the conversation\n• No server settings or configuration available\n• Bot doesn't appear in server member lists",
                inline=False
            )
            embed.add_field(
                name="How to Check Installation Type",
                value="• Try `/server settings` - if it works, it's Guild Installed\n• If you get \"Bot Not Installed\" error, it's User Installed\n• User installations can't access server management features",
                inline=False
            )
            embed.add_field(
                name="Switching Installation Types",
                value="• Remove bot and re-add with proper permissions\n• Guild admins should install for full functionality\n• User installs are good for personal use only",
                inline=False
            )
        
        # Create new view with the dropdown for continued navigation
        view = HelpDetailView(interaction_user=interaction.user)
        await interaction.response.edit_message(embed=embed, view=view)
        # Store message reference for timeout handling
        view.message = await interaction.original_response()

class HelpView(discord.ui.View):
    """View containing the help dropdown"""
    
    def __init__(self, interaction_user: discord.Member = None):
        super().__init__(timeout=120)  # 2 minute timeout
        self.interaction_user = interaction_user
        self.add_item(HelpDropdown())
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Ensure only the original command user can interact with this view"""
        return self.interaction_user is None or interaction.user.id == self.interaction_user.id
    
    async def on_timeout(self):
        """Disable interactive items when view times out after 2 minutes, but keep link buttons enabled"""
        # Disable all buttons and selects except link buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                # Keep link buttons enabled (they don't need interaction handling)
                if item.style != discord.ButtonStyle.link:
                    item.disabled = True
            elif isinstance(item, discord.ui.Select):
                item.disabled = True
        
        # Try to update the message to show disabled state
        try:
            if hasattr(self, 'message') and self.message:
                await self.message.edit(view=self)
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            # Message was deleted or we don't have permission to edit
            pass

class HelpDetailView(discord.ui.View):
    """View for detailed command help with navigation options"""
    
    def __init__(self, interaction_user: discord.Member = None):
        super().__init__(timeout=120)  # 2 minute timeout
        self.interaction_user = interaction_user
        self.add_item(HelpDropdown())
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Ensure only the original command user can interact with this view"""
        return self.interaction_user is None or interaction.user.id == self.interaction_user.id
    
    async def on_timeout(self):
        """Disable interactive items when view times out after 2 minutes, but keep link buttons enabled"""
        # Disable all buttons and selects except link buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                # Keep link buttons enabled (they don't need interaction handling)
                if item.style != discord.ButtonStyle.link:
                    item.disabled = True
            elif isinstance(item, discord.ui.Select):
                item.disabled = True
        
        # Try to update the message to show disabled state
        try:
            if hasattr(self, 'message') and self.message:
                await self.message.edit(view=self)
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            # Message was deleted or we don't have permission to edit
            pass
    
    @discord.ui.button(label="Back to Main Help", style=discord.ButtonStyle.secondary, row=1)
    async def back_to_main(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Return to the main help menu"""
        ephemeral = not is_dm(interaction)
        
        embed = discord.Embed(
            title="NookLook - Help",
            description="Animal Crossing: New Horizons database bot with items, villagers, recipes, artwork, and critters.",
            color=discord.Color.green()
        )
        
        # Main Commands
        embed.add_field(
            name="Lookup Commands",
            value=(
                "`/search` • `/lookup` • `/villager` • `/recipe`\n"
                "`/artwork` • `/critter` • `/help` • `/info`"
            ),
            inline=False
        )
        
        embed.add_field(
            name="Server Management (Admin Only)",
            value="`/server settings` • `/server hide_responses`",
            inline=False
        )
        
        # Quick Start
        embed.add_field(
            name="Get Started",
            value="Try `/lookup` and start typing for suggestions!\n",
            inline=False
        )
        
        # Attribution and Support
        embed.add_field(
            name="Credits & Support",
            value=(
                "**Data Source:** [ACNH Spreadsheet](https://discord.gg/kWMMYrN) community\n"
                "**Sites:** [Nookipedia](https://nookipedia.com) to link back to items\n"
                "**Support Server:** [BloominWatch](https://discord.gg/fxhXWgxcHV)"
            ),
            inline=False
        )
        
        embed.set_footer(text="Select a command below for examples and details")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        # Create view with dropdown for detailed help
        view = HelpView(interaction_user=interaction.user)
        
        await interaction.response.edit_message(embed=embed, view=view)
        # Store message reference for timeout handling
        view.message = await interaction.original_response()

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
            name="Lookup Commands",
            value=(
                "`/search` • `/lookup` • `/villager` • `/recipe`\n"
                "`/artwork` • `/critter` • `/help` • `/info`"
            ),
            inline=False
        )
        
        embed.add_field(
            name="Server Management (Admin Only)",
            value="`/server settings` • `/server hide_responses`",
            inline=False
        )
        
        # Quick Start
        embed.add_field(
            name="Get Started",
            value="Try `/lookup` and start typing for suggestions!\n",
            inline=False
        ) 

        # Attribution and Support
        embed.add_field(
            name="Credits & Support",
            value=(
                "**Data Source:** [ACNH Spreadsheet](https://discord.gg/kWMMYrN) community\n"
                "**Sites:** [Nookipedia](https://nookipedia.com) to link back to items\n"
                "**Support Server:** [BloominWatch](https://discord.gg/fxhXWgxcHV)"
            ),
            inline=False
        )
        
        embed.set_footer(text="Select a command below for examples and details")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        # Create view with dropdown for detailed help
        view = HelpView(interaction_user=interaction.user)
        
        message = await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
        view.message = message

    @app_commands.command(name="info", description="Show bot information and statistics")
    @app_commands.allowed_contexts(private_channels=True,guilds=True,dms=True)
    async def info(self, interaction: discord.Interaction):
        """Display bot information and database statistics"""
        ephemeral = not is_dm(interaction)
        await interaction.response.defer(ephemeral=ephemeral)
        
        # Get database statistics using the shared service
        try:
            service = getattr(self.bot, 'nooklook_service', None)
            if service:
                stats = await service.get_database_stats()
                total_items = stats.get('items', 0)
                total_variants = stats.get('variants', 0)
                total_critters = stats.get('critters', 0)
                total_recipes = stats.get('recipes', 0)
                total_villagers = stats.get('villagers', 0)
                total_fossils = stats.get('fossils', 0)
                total_artwork = stats.get('artwork', 0)
                total_content = stats.get('total_content', 0)
            else:
                total_items = total_variants = total_critters = total_recipes = 0
                total_villagers = total_fossils = total_artwork = total_content = 0
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            total_items = total_variants = total_critters = total_recipes = 0
            total_villagers = total_fossils = total_artwork = total_content = 0
        
        embed = discord.Embed(
            title="NookLook - Information",
            description="A comprehensive Animal Crossing: New Horizons item database bot",
            color=discord.Color.blue()
        )
        
        # Bot Statistics
        embed.add_field(
            name="Database Statistics",
            value=(
                f"**Items**: {total_items:,} ({total_variants:,} variants)\n"
                f"**Critters**: {total_critters:,}\n"
                f"**Recipes**: {total_recipes:,}\n"
                f"**Villagers**: {total_villagers:,}\n"
                f"**Fossils**: {total_fossils:,}\n"
                f"**Artwork**: {total_artwork:,}\n"
                f"**Total**: {total_content:,}"
            ),
            inline=True
        )
        

        
        # Features
        embed.add_field(
            name="Features",
            value=(
                "Smart search & autocomplete • Color variants & hex codes\n"
                "Seasonal availability • Prices & sources • Villager details\n"
                "Personal stashes to save items"
            ),
            inline=False
        )
        
        # Attribution and Support
        embed.add_field(
            name="Credits & Support",
            value=(
                "**Created by:** BloominDaisy\n"
                "**Data Source:** [ACNH Spreadsheet](https://discord.gg/kWMMYrN) community\n"
                "**Sites:** [Nookipedia](https://nookipedia.com) to link back to items\n"
                "**Support Server:** [BloominWatch](https://discord.gg/fxhXWgxcHV)"
            ),
            inline=False
        )
        
        embed.set_footer(text="Made with 💖 for the ACNH community | Use /help for command details")
        embed.set_thumbnail(url="https://dodo.ac/np/images/thumb/1/13/Maple_Leaf_NH_Inv_Icon.png/60px-Maple_Leaf_NH_Inv_Icon.png")
        
        await interaction.followup.send(embed=embed, ephemeral=ephemeral)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))