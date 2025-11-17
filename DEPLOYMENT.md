# Self-Hosting NookLook

This guide provides instructions for hosting your own instance of NookLook, including legal requirements and technical setup.

## ⚖️ Legal Requirements

### Before You Host
**YOU MUST:**
- ✅ Comply with Discord's Terms of Service and Community Guidelines
- ✅ Provide your own Terms of Service and Privacy Policy for your instance
- ✅ Respect Nintendo's intellectual property rights
- ✅ Maintain attribution to original creators (doodlebunnyhops)
- ✅ Credit the ACNH Spreadsheet community for data
- ✅ Comply with local data protection laws (GDPR, CCPA, etc.)

**YOU CANNOT:**
- ❌ Remove attribution requirements from the bot or documentation
- ❌ Claim ownership of Nintendo's Animal Crossing content
- ❌ Use the bot for commercial purposes without proper licensing
- ❌ Redistribute Nintendo's copyrighted assets beyond fair use

### Required Disclaimers
Your bot instance **MUST** include these disclaimers:
```
- This bot is not affiliated with or endorsed by Nintendo
- Animal Crossing: New Horizons is a trademark of Nintendo Co., Ltd.
- Original bot created by doodlebunnyhops (https://github.com/doodlebunnyhops)
- Data sourced from the ACNH Spreadsheet community
```

## 🛠️ Technical Setup

### Prerequisites
- **Python 3.11+** (required for modern async features)
- **Git** for cloning the repository
- **Discord Application** with bot token
- **Hosting Environment** (VPS, cloud service, or local machine)

### Step 1: Clone and Setup
```bash
# Clone the repository
git clone https://github.com/doodlebunnyhops/nooklook.git
cd nooklook/acnh-lookup

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
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Required variables:
DISCORD_TOKEN=your_bot_token_here
DATABASE_PATH=./bot/db/nooklook.db
LOG_LEVEL=INFO

# Optional variables:
ENVIRONMENT=production
SENTRY_DSN=your_sentry_dsn_here
```

### Step 4: Database Setup
```bash
# Initialize the database with ACNH data
python import_all_datasets.py

# Verify database setup
python -c "
import sqlite3
conn = sqlite3.connect('./bot/db/nooklook.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM items')
print(f'Items loaded: {cursor.fetchone()[0]}')
conn.close()
"
```

### Step 5: Test and Deploy
```bash
# Test the bot locally
python start_bot.py

# Check for any errors in the console
# Test basic commands like /info and /lookup
```

## 🚀 Deployment Options

### Option 1: VPS/Cloud Server
**Recommended for:** Persistent uptime, community use

```bash
# Using systemd service (Linux)
sudo nano /etc/systemd/system/nooklook.service

[Unit]
Description=NookLook Discord Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/nooklook/acnh-lookup
Environment=PATH=/path/to/nooklook/acnh-lookup/bot_env/bin
ExecStart=/path/to/nooklook/acnh-lookup/bot_env/bin/python start_bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable nooklook
sudo systemctl start nooklook
```

### Option 2: Docker Deployment
```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python import_all_datasets.py

CMD ["python", "start_bot.py"]
```

```bash
# Build and run
docker build -t nooklook .
docker run -d --name nooklook-bot --env-file .env nooklook
```

### Option 3: Heroku Deployment
```bash
# Create Procfile
echo "worker: python start_bot.py" > Procfile

# Deploy to Heroku
heroku create your-bot-name
heroku config:set DISCORD_TOKEN=your_token
git push heroku main
heroku ps:scale worker=1
```

## 🔒 Security Best Practices

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

## 📊 Monitoring and Maintenance

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

## 🆘 Troubleshooting

### Common Issues

#### Bot Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip check

# Check token format
echo $DISCORD_TOKEN | wc -c  # Should be ~70 characters
```

#### Database Issues
```bash
# Rebuild database
rm ./bot/db/nooklook.db
python import_all_datasets.py

# Check database integrity
sqlite3 ./bot/db/nooklook.db "PRAGMA integrity_check;"
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

## 📋 Compliance Checklist

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
- [ ] Permissions set correctly
- [ ] Monitoring/logging configured
- [ ] Backup procedures established

**Security Measures:**
- [ ] Environment variables secured
- [ ] Dependencies updated
- [ ] Access controls implemented
- [ ] Network security configured
- [ ] Regular maintenance plan created

## 📚 Additional Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs/)
- [Python Deployment Best Practices](https://docs.python.org/3/tutorial/venv.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [GDPR Compliance Guide](https://gdpr.eu/compliance/)

---

**Important:** Running your own bot instance makes you responsible for compliance with all applicable laws and Discord's Terms of Service. This guide provides general guidance but you should consult legal professionals for specific compliance questions.

*Thank you for supporting the NookLook project by hosting your own instance! 🦝*