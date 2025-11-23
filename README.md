# NookLook - Animal Crossing: New Horizons Discord Bot

**NookLook** is a comprehensive Discord bot for Animal Crossing: New Horizons, providing instant access to items, villagers, recipes, artwork, fossils and critters with detailed information and smart search capabilities.

[Install NookLook](https://discord.com/oauth2/authorize?client_id=1439097629404561539)

## Features

- **Smart Search** - Search across all ACNH content with partial matching and category filtering
- **Item Lookup** - Complete item details with variants, customization options, and hex codes
- **Villager Info** - Detailed villager profiles including house details, preferences, and equipment
- **Recipe Database** - Both DIY crafting and cooking recipes with ingredients and sources
- **Artwork Guide** - Genuine vs fake artwork detection with visual comparisons
- **Fossil Guide** - Complete fossil catalog with museum donation info
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
| `/fossil` | Look up fossils and paleontology info |
| `/help` | Interactive help with detailed command info |
| `/info` | Bot statistics and database information |

## Technical Details

### Built With
- **Python 3.12+** with discord.py 2.6+
- **SQLite Database** with FTS5 full-text search
- **Async/Await** architecture for optimal performance
- **Comprehensive Data Models** with dataclasses and type hints

### Database Schema
- **Items & Variants** - Complete item catalog with color/pattern variants
- **Villagers** - All 400+ villagers with detailed house and preference data
- **Recipes** - DIY crafting and cooking recipes with ingredients
- **Artwork** - Paintings and statues with authenticity details
- **Fossils** - Complete paleontology collection with details
- **Critters** - Fish, bugs, sea creatures with seasonal data
- **Search Index** - FTS5 unified search across all content types

### Key Features
- **Smart Autocomplete** - Context-aware suggestions with caching
- **Prefix Matching** - "ancho" finds "anchovy" and related items
- **Category Filtering** - Narrow results by content type
- **Interactive Views** - Rich UI components for better UX
- **Variant Resolution** - Resolves internal IDs to human-readable names

## Data Source

NookLook uses comprehensive data from the [ACNH Sheets Discord](https://discord.gg/8jNFHxG) community. The bot automatically imports the latest data via Google Sheets API, ensuring you always have up-to-date information.

**Automated via Google Sheets API:**
- Real-time data synchronization
- **26,000+** records across all categories  
- Automatic image URL extraction
- TI code generation for trading
- **400+** villagers with complete details
- **600+** recipes (DIY + cooking)
- **40+** artwork pieces
- **70+** fossils for museum collection
- **240+** critters with seasonal data

**Image Sources:**
- All item, villager, and content images are served from **[ACNH Community CDN](https://acnhcdn.com/)**
- Images are not redistributed but linked directly to maintain up-to-date content

**Community Attribution**: All data courtesy of the amazing ACNH research community at [discord.gg/8jNFHxG](https://discord.gg/8jNFHxG)

## Getting Started

1. **Invite the Bot** - Add NookLook to your Discord server
2. **Try Commands** - Start with `/lookup` and type for suggestions
3. **Explore Features** - Use `/help` for detailed command information
4. **Search Everything** - Use `/search` with category filters for specific content

## Development Setup

### Quick Start with Google Sheets API

The easiest way to set up NookLook is using the Google Sheets API integration:

```bash
# Clone the repository
git clone https://github.com/yourusername/nooklook.git
cd nooklook/acnh-lookup

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API key (see .env.example for all options)

# Create database from Google Sheets (recommended)
python db_tools/run_full_import.py

# Start the bot
python start_bot.py
```

### Google Sheets API Setup

1. **Get Google Cloud API Key**:
   - Visit [Google Cloud Console](https://console.cloud.google.com)
   - Create/select a project
   - Enable "Google Sheets API" in APIs & Services
   - Create credentials → API Key
   - Restrict key to Google Sheets API (recommended)

2. **Configure Environment**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key:
   GOOGLE_SHEETS_API_KEY=your_google_cloud_api_key_here
   ```

3. **Run Import**:
   ```bash
   python run_full_import.py
   ```

This automatically imports the latest data from the [ACNH Sheets Discord](https://discord.gg/8jNFHxG) community spreadsheet.

> **Note**: See [GOOGLE_SHEETS_API.md](GOOGLE_SHEETS_API.md) for detailed setup instructions and troubleshooting.


## Requirements

- Python 3.12 or higher
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
Copyright (c) 2025 doodlebunnyhops
Licensed under MIT License - see LICENSE file for details
Attribution required for all derivative works
```

**Third-party attributions:**
- Game data: Animal Crossing: New Horizons (©Nintendo Co., Ltd.)
- Community data: [ACNH Community Discord](https://discord.gg/kWMMYrN) spreadsheet
- Images: [ACNH Community CDN](https://acnhcdn.com/)

---

*Animal Crossing: New Horizons is a trademark of Nintendo. This bot is not affiliated with or endorsed by Nintendo.*