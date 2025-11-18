# Self-Hosting NookLook

This guide provides instructions for hosting your own instance of NookLook, including legal requirements and technical setup.

## Legal Requirements

### Before You Host
**YOU MUST:**
- Comply with Discord's Terms of Service and Community Guidelines
- Provide your own Terms of Service and Privacy Policy for your instance
- Respect Nintendo's intellectual property rights
- Maintain attribution to original creators (doodlebunnyhops)
- Credit the ACNH Spreadsheet community for data
- Comply with local data protection laws (GDPR, CCPA, etc.)

**YOU CANNOT:**
- Remove attribution requirements from the bot or documentation
- Claim ownership of Nintendo's Animal Crossing content
- Use the bot for commercial purposes without proper licensing
- Redistribute Nintendo's copyrighted assets beyond fair use

### Required Disclaimers
Your bot instance **MUST** include these disclaimers:
```
- This bot is not affiliated with or endorsed by Nintendo
- Animal Crossing: New Horizons is a trademark of Nintendo Co., Ltd.
- Original bot created by doodlebunnyhops (https://github.com/doodlebunnyhops) aka bloomindaisy on discord
- Data sourced from the ACNH Spreadsheet community
```

## Technical Setup

### Prerequisites
- **Python 3.12+** (required for modern async features)
- **Git** for cloning the repository
- **Discord Application** with bot token
- **Hosting Environment** (VPS, cloud service, or local machine)
- **Optional: Nookipedia API key** for enhanced data quality

### Important Files
The repository includes example configuration files:
- `.env.example` - Environment variable template
- `bot.service.example` - Systemd service template for Linux

Copy and customize these for your deployment.

### Step 1: Clone and Setup
```bash
# Clone the repository
git clone https://github.com/doodlebunnyhops/nooklook.git
cd nooklook

# Create virtual environment (recommended)
python -m venv bot_env
# On Windows:
bot_env\Scripts\activate
# On Linux/Mac:
source bot_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Discord Bot Setup
1. **Create Discord Application:**
   - Go to https://discord.com/developers/applications
   - Click "New Application" and name your bot
   - Navigate to "Bot" section and create a bot
   - Copy the bot token (keep this secret!)

2. **Set Bot Permissions:**
   - In Discord Developer Portal → Bot → Privileged Gateway Intents
   - Enable "Message Content Intent" if needed
   - Calculate permissions: `137439346752` (recommended permissions)

3. **Invite Bot to Server:**
   - Use Discord's OAuth2 URL Generator
   - Select "bot" and "applications.commands" scopes
   - Choose appropriate permissions
   - Generate and use the invite link

### Step 3: Configuration

**Do not edit the .env.example! You don't accidently want to commit your secrets ...**

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings (see .env.example for all available options)
# Required variables:
DISCORD_API_TOKEN=your_bot_token_here

# Google Sheets API Configuration
# Get your API key from Google Cloud Console (see GOOGLE_SHEETS_API.md)
GOOGLE_SHEETS_API_KEY=your_google_cloud_api_key_here
GOOGLE_SHEET=https://sheets.googleapis.com/v4/spreadsheets/13d_LAJPlxMa_DubPTuirkIV4DERBMXbrWQsmSh8ReK4


# Optional but recommended - Nookipedia API for enhanced data:
NOOKIPEDIA_API=your_nookipedia_api_key_here

# Other optional variables (see .env.example for complete list):
GUILD=your_guild_id_here  # For faster command syncing
FEEDBACK_CH=your_feedback_channel_id_here
```

### Step 4: Database Setup
```bash
# STEP 1: Initialize the database with ACNH data (REQUIRED FIRST)
python db_tools/run_full_import.py

# STEP 2: Add Nookipedia data for enhanced experience (optional)
# (requires NOOKIPEDIA_API in .env - configured above)
python nookipedia/update_db.py

# Verify database setup
python -c "
import sqlite3
conn = sqlite3.connect('./data/nooklook.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM items')
print(f'Items loaded: {cursor.fetchone()[0]}')
conn.close()
"
```
Should see `Items loaded: 9863`

#### Nookipedia API Setup (Optional but Recommended)
For enhanced villager images and data quality:

1. **Get API Key:**
   - Apply at https://api.nookipedia.com/
   - Add your key to `.env` as `NOOKIPEDIA_API=your_key_here`

2. **Database Update Process:**
   *(This happens in Step 4 after the base database is created)*


**What Nookipedia Update Adds:**
- High-quality villager photos and icons
- House interior/exterior images  
- Nookipedia URLs for all content

### Step 5: Test and Deploy
```bash
# Test the bot locally from root of project
python start_bot.py

# Check for any errors in the console
# Test basic commands like /info and /lookup
```

## Security Best Practices

### Environment Security
- **Never commit `.env` files** to version control
- **Use strong, unique bot tokens** - regenerate if compromised
- **Limit bot permissions** to only what's necessary
- **Regular updates** - keep dependencies up to date
- **Monitor logs** for suspicious activity

### Database Security
- **Backup regularly** - automate database backups
- **File permissions** - restrict database file access
- **SQLite security** - use WAL mode for better concurrency
- **Data validation** - sanitize all user inputs

### Network Security
```bash
# Use firewall rules (example for UFW)
sudo ufw allow 22/tcp      # SSH only if needed
sudo ufw deny incoming
sudo ufw allow outgoing
sudo ufw enable
```

## Monitoring and Maintenance

### Essential Monitoring
```python
# Add to your bot for health checks
@bot.command(name='health')
async def health_check(ctx):
    """Simple health check endpoint"""
    db_status = "✅" if check_database_connection() else "❌"
    await ctx.send(f"Bot Status: ✅\nDatabase: {db_status}")
```

### Log Management
- **Rotate logs** to prevent disk space issues
- **Monitor error rates** - set up alerts for high error rates
- **Performance tracking** - monitor command response times
- **Usage analytics** - track popular commands and features

### Update Procedure
```bash
# Regular update workflow
git fetch origin
git pull origin main
pip install -r requirements.txt --upgrade
# Test in development environment first
# Deploy to production
systemctl restart nooklook  # or your deployment method
```

## Troubleshooting

### Common Issues

#### Bot Won't Start
```bash
# Check Python version
python --version  # Should be 3.12+

# Check dependencies
pip check

# Check token format
echo $DISCORD_TOKEN | wc -c  # Should be ~70 characters
```

#### Database Issues
```bash
# Rebuild database if corrupted
rm ./data/nooklook.db
python db_tools/run_full_import.py

# Re-add Nookipedia data if configured
if [ -n "$NOOKIPEDIA_API" ]; then
    python nookipedia/fetch_urls.py
    python nookipedia/update_db.py
fi

# Check database integrity
sqlite3 ./data/nooklook.db "PRAGMA integrity_check;"
```

#### Permission Errors
- Verify bot has necessary Discord permissions
- Check file system permissions for database and logs
- Ensure bot is properly invited to server with correct scopes

#### Performance Issues
```python
# Enable SQLite performance optimizations
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 1000000;
PRAGMA temp_store = memory;
```

### Getting Help
- **GitHub Issues** - For bugs and technical problems
- **Discord Community** - [BloominWatch server](https://discord.gg/bloominwatch) for community support
- **Documentation** - Check README and other docs first
- **Logs** - Always include relevant log output when asking for help

## Compliance Checklist

Before deploying your instance:

**Legal Compliance:**
- [ ] Created your own Terms of Service
- [ ] Created your own Privacy Policy  
- [ ] Included required Nintendo disclaimers
- [ ] Maintained attribution to original creators
- [ ] Reviewed local data protection laws

**Technical Setup:**
- [ ] Bot token configured securely
- [ ] Database initialized and tested
- [ ] Nookipedia API configured (optional but recommended)
- [ ] Enhanced data imported via `nookipedia/update_db.py`
- [ ] Permissions set correctly
- [ ] Monitoring/logging configured
- [ ] Backup procedures established

**Security Measures:**
- [ ] Environment variables secured
- [ ] Dependencies updated
- [ ] Access controls implemented
- [ ] Network security configured
- [ ] Regular maintenance plan created

## Additional Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs/)
- [Python Deployment Best Practices](https://docs.python.org/3/tutorial/venv.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [GDPR Compliance Guide](https://gdpr.eu/compliance/)

---

**Important:** Running your own bot instance makes you responsible for compliance with all applicable laws and Discord's Terms of Service. This guide provides general guidance but you should consult legal professionals for specific compliance questions.

*Thank you for supporting the NookLook project by hosting your own instance!*