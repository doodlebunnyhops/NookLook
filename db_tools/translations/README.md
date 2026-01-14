# Translations Module

This module contains tools for fetching and managing localized item names from Nookipedia.

## Quick Start

### 1. Apply the Schema

```powershell
python -m db_tools.translations.setup_schema
```

### 2. Import Translations

```powershell
# Dry run first
python -m db_tools.translations.import_translations --dry-run

# Then import
python -m db_tools.translations.import_translations
```

### 3. Restart the Bot

The `/language`, `/hemisphere`, and `/preferences` commands will be available.

---

## Exploration Script

The `explore_translations.py` script allows you to test and explore the Nookipedia Cargo API for translations before implementing the full import.

### Usage

```bash
# Run demo (shows sample items and search examples)
python db_tools/translations/explore_translations.py

# Count all available translations
python db_tools/translations/explore_translations.py count

# Export sample translations to JSON
python db_tools/translations/explore_translations.py export

# Search for items
python db_tools/translations/explore_translations.py search "chair"
python db_tools/translations/explore_translations.py search "イス" ja

# Explore other Cargo tables
python db_tools/translations/explore_translations.py fish
python db_tools/translations/explore_translations.py art
python db_tools/translations/explore_translations.py recipe
```

---

## Available Languages

| Code | Language | Native Name |
|------|----------|-------------|
| en | English | English |
| ja | Japanese | 日本語 |
| zh | Chinese (Simplified) | 简体中文 |
| ko | Korean | 한국어 |
| fr | French | Français |
| de | German | Deutsch |
| es | Spanish | Español |
| it | Italian | Italiano |
| nl | Dutch | Nederlands |
| ru | Russian | Русский |

---

## Discord Commands

| Command | Description |
|---------|-------------|
| `/language` | Set preferred language for item lookups |
| `/hemisphere` | Set hemisphere for seasonal info |
| `/preferences` | View current settings |
| `/reset-preferences` | Reset to defaults |

---

## Database Tables

**user_settings** - Stores user preferences:
- `user_id` (TEXT PRIMARY KEY)
- `preferred_language` (TEXT, default 'en')
- `hemisphere` (TEXT, default 'north')

**item_translations** - Stores localized names:
- `ref_table` / `ref_id` - Link to source item
- `en_name`, `ja_name`, `zh_name`, `ko_name`, `fr_name`, `de_name`, `es_name`, `it_name`, `nl_name`, `ru_name`

---

## API Reference

### UserRepository

```python
from bot.repos import UserRepository

repo = UserRepository()
lang = await repo.get_user_language(user_id)  # Returns 'en' by default
await repo.set_preferred_language(user_id, 'ja')
```

### TranslationService

```python
from bot.services import TranslationService

service = TranslationService()
name = await service.get_localized_name_or_fallback('items', item_id, 'ja', item.name)
matches = await service.search_by_translation('chaise', 'fr')
```

---

## Data Source

Data is fetched from Nookipedia's Cargo tables:
- Table: `nh_language_name`
- API: `https://nookipedia.com/w/api.php?action=cargoquery`

See the [Nookipedia Cargo Tables](https://nookipedia.com/wiki/Special:CargoTables/nh_language_name) for more information.
