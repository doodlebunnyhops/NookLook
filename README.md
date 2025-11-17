# NookLook - Animal Crossing: New Horizons Discord Bot

**NookLook** is a comprehensive Discord bot for Animal Crossing: New Horizons, providing instant access to items, villagers, recipes, artwork, and critters with detailed information and smart search capabilities.

## Features

- **Smart Search** - Search across all ACNH content with partial matching and category filtering
- **Item Lookup** - Complete item details with variants, customization options, and hex codes
- **Villager Info** - Detailed villager profiles including house details, preferences, and equipment
- **Recipe Database** - Both DIY crafting and cooking recipes with ingredients and sources
- **Artwork Guide** - Genuine vs fake artwork detection with visual comparisons
- **Critter Tracker** - Fish, bugs, and sea creatures with seasonal availability
- **Interactive UI** - Dropdowns, buttons, and navigation for enhanced user experience
- **Fast Performance** - Optimized database queries with intelligent caching

## Bot Commands

| Command | Description |
|---------|-------------|
| `/search` | Search all content with category filters |
| `/lookup` | Look up items with variants & customization |
| `/villager` | Find villager info & preferences |
| `/recipe` | Look up DIY and food recipes |
| `/artwork` | Find genuine/fake artwork details |
| `/critter` | Fish, bugs & sea creature info |
| `/help` | Interactive help with detailed command info |
| `/info` | Bot statistics and database information |

## Technical Details

### Built With
- **Python 3.11+** with discord.py 2.3+
- **SQLite Database** with FTS5 full-text search
- **Async/Await** architecture for optimal performance
- **Comprehensive Data Models** with dataclasses and type hints

### Database Schema
- **Items & Variants** - Complete item catalog with color/pattern variants
- **Villagers** - All 400+ villagers with detailed house and preference data
- **Recipes** - DIY crafting and cooking recipes with ingredients
- **Artwork** - Paintings and statues with authenticity details
- **Critters** - Fish, bugs, sea creatures with seasonal data
- **Search Index** - FTS5 unified search across all content types

### Key Features
- **Smart Autocomplete** - Context-aware suggestions with caching
- **Prefix Matching** - "ancho" finds "anchovy" and related items
- **Category Filtering** - Narrow results by content type
- **Interactive Views** - Rich UI components for better UX
- **Variant Resolution** - Resolves internal IDs to human-readable names

## Data Source

All data is sourced from the **[ACNH Community Discord](https://discord.gg/kWMMYrN)** spreadsheet, converted from Google Sheets to CSV datasets and imported via `import_all_datasets.py`. This ensures accuracy and completeness with:
- **13,000+** items across 25+ categories
- **400+** villagers with complete details
- **600+** recipes (DIY + cooking)
- **40+** artwork pieces
- **240+** critters with seasonal data

**Image Sources:**
- All item, villager, and content images are served from **[ACNH Community CDN](https://acnhcdn.com/)**
- Images are not redistributed but linked directly to maintain up-to-date content

## Getting Started

1. **Invite the Bot** - Add NookLook to your Discord server
2. **Try Commands** - Start with `/lookup` and type for suggestions
3. **Explore Features** - Use `/help` for detailed command information
4. **Search Everything** - Use `/search` with category filters for specific content

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/nooklook.git
cd nooklook/acnh-lookup

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your bot token

# Initialize database
python import_all_datasets.py

# Start the bot
python start_bot.py
```

## Requirements

- Python 3.11 or higher
- Discord Bot Token
- SQLite (included with Python)
- See `requirements.txt` for Python dependencies

## Contributing

Contributions are welcome! Please feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## Support

- **Support Server**: [BloominWatch Discord](https://discord.gg/bloominwatch)
- **Issues**: GitHub Issues for bug reports and feature requests
- **Documentation**: Use `/help` in Discord for command details

## Legal & Open Source

- **License**: [MIT License](LICENSE) - Free to use, modify, and distribute with attribution
- **Terms of Service**: [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md)
- **Privacy Policy**: [PRIVACY_POLICY.md](PRIVACY_POLICY.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md) - Guidelines for contributors
- **Self-Hosting**: [DEPLOYMENT.md](DEPLOYMENT.md) - Host your own instance
- **Data Attribution**: ACNH Spreadsheet community

## Contributing

NookLook is open source! We welcome contributions from the community:

- **Bug Reports** - Help us find and fix issues
- **Feature Requests** - Suggest new functionality  
- **Code Contributions** - Submit pull requests
- **Data Improvements** - Help verify and improve game data
- **Documentation** - Improve guides and examples

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the **MIT License** with attribution requirements:

```
Copyright (c) 2024 doodlebunnyhops
Licensed under MIT License - see LICENSE file for details
Attribution required for all derivative works
```

**Third-party attributions:**
- Game data: Animal Crossing: New Horizons (©Nintendo Co., Ltd.)
- Community data: [ACNH Community Discord](https://discord.gg/kWMMYrN) spreadsheet
- Images: [ACNH Community CDN](https://acnhcdn.com/)

---

*Animal Crossing: New Horizons is a trademark of Nintendo. This bot is not affiliated with or endorsed by Nintendo.*