# 🔥 YAGAMI UNIVERZE

**The Ultimate Universal Telegram Bot Generator**

Generate ANY Telegram bot automatically from a simple text description. YAGAMI UNIVERZE uses AI to create complete, production-ready bots with full Docker deployment, monitoring, and GitHub integration.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 Features

### Core Capabilities
- 🤖 **AI-Powered Generation**: Describe your bot, get complete working code
- 🐳 **Docker Ready**: Auto-generated Dockerfile + docker-compose for every bot
- 🔍 **GitHub Scanner**: Scan repos to extract env variables automatically
- 🚀 **Auto-Deployment**: One-command deployment of generated bots
- 🌐 **Multi-Language**: Python, Node.js, Go, PHP support
- 📦 **Complete Packages**: Get full source code, dependencies, docs, and deployment files

### Supported Frameworks
- **Python**: Pyrogram, Aiogram, Telebot, Python-Telegram-Bot
- **Node.js**: Telegraf, node-telegram-bot-api, Grammy
- **Go**: Telebot, tgbotapi
- **PHP**: telegram-bot-sdk

### What You Get
For every generated bot:
- ✅ Complete source code
- ✅ Dockerfile + docker-compose.yml
- ✅ Environment variable templates
- ✅ README with setup instructions
- ✅ Deployment guide
- ✅ Logging and error handling
- ✅ Production-ready structure
- ✅ Downloadable ZIP archive

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- API credentials from [my.telegram.org](https://my.telegram.org)
- API key from [Anthropic](https://console.anthropic.com/) or [OpenAI](https://platform.openai.com/)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/yagami-univerze.git
cd yagami-univerze
```

2. **Configure environment**
```bash
cp .env.example .env
nano .env
```

Fill in your credentials:
```env
API_ID=12345678
API_HASH=your_api_hash
BOT_TOKEN=123456789:ABCdef...
ANTHROPIC_API_KEY=sk-ant-api03-...
ADMIN_ID=your_user_id
```

3. **Create Docker network**
```bash
docker network create yagami_network
```

4. **Deploy**
```bash
docker-compose up -d
```

5. **Check logs**
```bash
docker-compose logs -f
```

---

## 📖 Usage Guide

### Basic Usage

Start a chat with your bot and use these commands:

#### Generate a Bot
```
/generate Create an RSS feed bot that posts new articles to a channel
```

or simply describe what you want:
```
I need a bot that forwards messages from one group to another
```

#### Scan a GitHub Repository
```
/scan https://github.com/username/telegram-bot
```

This will:
- Clone and analyze the repository
- Extract all environment variables
- Generate a complete .env template
- Detect the language and framework
- Show project structure

#### Deploy a Generated Bot
```
/deploy bot_20231121_123456
```

### Example Use Cases

**1. RSS Feed Bot**
```
/generate Create a bot that monitors RSS feeds and sends new items to a channel. Support multiple feeds and custom filters.
```

**2. File Converter Bot**
```
/generate Build a file converter bot that can convert documents between PDF, DOCX, and TXT formats
```

**3. Auto-Forward Bot**
```
/generate Create a bot that automatically forwards messages from one channel to another with filtering options
```

**4. Inline Search Bot**
```
/generate Make an inline bot for searching Wikipedia articles directly from any chat
```

**5. Admin Bot**
```
/generate Create a group admin bot with ban, kick, mute features and welcome messages
```

---

## 🏗️ Architecture

### Project Structure
```
yagami_univerze/
├── bot/
│   ├── main.py                 # Main bot entry point
│   ├── config.py               # Configuration management
│   └── handlers/               # Command handlers
│       ├── start_handler.py
│       ├── generate_handler.py
│       ├── repo_scan_handler.py
│       └── deploy_handler.py
├── generator_engine/
│   ├── ai_generator.py         # AI code generation engine
│   ├── repo_scanner.py         # GitHub repo analyzer
│   └── code_writer.py          # File system writer
├── deployment/
│   ├── Dockerfile              # Bot container
│   ├── docker-compose.yml      # Orchestration
│   └── supervisor.conf         # Process manager
├── utils/
│   └── monitor.py              # Health monitoring
├── generated_bots/             # Generated bots storage
├── logs/                       # Log files
├── temp/                       # Temporary files
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── README.md                   # This file
└── LICENSE                     # MIT License
```

### How It Works

1. **User Input**: User describes the bot they want
2. **AI Analysis**: AI analyzes the requirements and determines architecture
3. **Code Generation**: Complete bot code is generated using AI
4. **File Creation**: All files written to a new directory
5. **Deployment Prep**: Dockerfile, docker-compose, and docs generated
6. **Archive Creation**: Everything packaged into a downloadable ZIP
7. **Optional Deploy**: One-command deployment to Docker

### Generated Bot Structure
```
generated_bot_example/
├── main.py                     # Bot entry point
├── requirements.txt            # Dependencies
├── Dockerfile                  # Container config
├── docker-compose.yml          # Deployment config
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── README.md                   # Bot documentation
├── DEPLOYMENT.md               # Deployment guide
├── handlers/                   # Command handlers
├── services/                   # Business logic
├── utils/                      # Helper functions
├── logs/                       # Log directory
└── data/                       # Data storage
```

---

## 🔧 Configuration

### Required Settings

| Variable | Description | Example |
|----------|-------------|---------|
| `API_ID` | Telegram API ID | `12345678` |
| `API_HASH` | Telegram API Hash | `abc123def456...` |
| `BOT_TOKEN` | Bot token from @BotFather | `123456789:ABC...` |
| `ADMIN_ID` | Your Telegram user ID | `123456789` |
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-api03-...` |

### Optional Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKERS` | `8` | Number of worker threads |
| `MAX_CONCURRENT_GENERATIONS` | `3` | Max parallel generations |
| `MAX_GENERATIONS_PER_USER` | `10` | Rate limit per user |
| `GITHUB_TOKEN` | - | For private repo scanning |
| `AI_MODEL` | `claude-sonnet-4-20250514` | AI model to use |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## 🐳 Docker Deployment

### Deploy YAGAMI UNIVERZE

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Rebuild
docker-compose up --build -d
```

### Deploy Generated Bots

After generating a bot:

```bash
cd generated_bots/your_bot_name_timestamp/

# Fill in .env
cp .env.example .env
nano .env

# Deploy
docker-compose up -d

# Monitor
docker-compose logs -f
```

### Docker Commands Cheat Sheet

```bash
# List all containers
docker ps -a

# View bot logs
docker logs -f yagami_univerze

# Execute command in container
docker exec -it yagami_univerze bash

# Clean up
docker system prune -a

# Monitor resources
docker stats
```

---

## 📊 Monitoring & Maintenance

### Log Files
- `logs/yagami.log` - Main bot logs
- `logs/yagami_err.log` - Error logs
- `logs/yagami_out.log` - Output logs
- `generated_bots/*/logs/` - Individual bot logs

### Health Checks
```bash
# Check bot status
docker-compose ps

# View bot health
docker inspect yagami_univerze | grep Health

# Resource usage
docker stats yagami_univerze
```

### Backup
```bash
# Backup generated bots
tar -czf backup_$(date +%Y%m%d).tar.gz generated_bots/

# Backup configuration
cp .env .env.backup
```

### Cleanup
```bash
# Remove old generated bots (older than 7 days)
find generated_bots/ -type d -mtime +7 -exec rm -rf {} +

# Clean Docker
docker system prune -af
```

---

## 🔐 Security Best Practices

- ✅ Never commit `.env` files to Git
- ✅ Use strong, unique bot tokens
- ✅ Restrict bot access with `ALLOWED_USERS`
- ✅ Enable rate limiting
- ✅ Keep dependencies updated
- ✅ Use HTTPS for webhooks
- ✅ Enable firewall on VPS
- ✅ Regular security audits
- ✅ Monitor logs for suspicious activity

---

## 🐛 Troubleshooting

### Bot Not Starting

**Problem**: Bot doesn't start or crashes immediately

**Solutions**:
```bash
# Check logs
docker-compose logs yagami_univerze

# Verify environment
cat .env

# Rebuild container
docker-compose down
docker-compose up --build -d

# Check permissions
ls -la generated_bots/
```

### Generation Fails

**Problem**: Bot generation fails with errors

**Solutions**:
- Check AI API key is valid
- Verify API rate limits not exceeded
- Check internet connectivity
- Review logs for specific errors

### Deployment Issues

**Problem**: Generated bot won't deploy

**Solutions**:
- Ensure `.env` file exists in bot directory
- Verify Docker is running
- Check Docker network exists: `docker network ls`
- Review bot logs: `cd generated_bots/bot_name && docker-compose logs`

### GitHub Scanning Fails

**Problem**: Repository scanning doesn't work

**Solutions**:
- Verify repo URL is correct and public
- Add `GITHUB_TOKEN` for private repos
- Check internet connectivity
- Ensure Git is installed in container

---

## 🎯 Advanced Usage

### Custom AI Models

Use GPT-4 instead of Claude:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
AI_MODEL=gpt-4
```

### Multiple Bot Instances

Run multiple YAGAMI instances:
```bash
# Create new compose file
cp docker-compose.yml docker-compose.instance2.yml

# Edit ports and container name
nano docker-compose.instance2.yml

# Deploy
docker-compose -f docker-compose.instance2.yml up -d
```

### Custom Network Configuration

```bash
# Create custom network
docker network create --subnet=172.20.0.0/16 custom_network

# Update docker-compose.yml network settings
```

### Database Integration

Enable PostgreSQL for bot metadata:
```env
DATABASE_URL=postgresql://user:pass@localhost/yagami
```

---

## 📝 Development

### Local Development

```bash
# Clone repo
git clone https://github.com/yourusername/yagami-univerze.git
cd yagami-univerze

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py
```

### Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=bot tests/

# Specific test
pytest tests/test_generator.py
```

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

---

## 🌐 Production Deployment

### VPS Deployment (Ubuntu/Debian)

```bash
# Connect to VPS
ssh user@your-vps-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/yourusername/yagami-univerze.git
cd yagami-univerze

# Configure
cp .env.example .env
nano .env

# Deploy
docker network create yagami_network
docker-compose up -d

# Enable auto-start
sudo systemctl enable docker
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/yagami
server {
    listen 443 ssl http2;
    server_name bot.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/bot.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bot.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Systemd Service

```ini
# /etc/systemd/system/yagami.service
[Unit]
Description=YAGAMI UNIVERZE Bot
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/yagami-univerze
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable yagami
sudo systemctl start yagami
```

---

## 📚 API Documentation

### AIGenerator API

```python
from generator_engine.ai_generator import AIGenerator

# Initialize
generator = AIGenerator()

# Generate bot
bot_data = await generator.generate_bot(
    user_prompt="Create a welcome bot",
    user_id=123456789
)

# Returns:
# {
#     'language': 'python',
#     'framework': 'pyrogram',
#     'files': {...},
#     'env_vars': [...],
#     'description': '...',
#     'name': 'welcome_bot'
# }
```

### RepoScanner API

```python
from generator_engine.repo_scanner import RepoScanner

# Initialize
scanner = RepoScanner()

# Scan repository
results = await scanner.scan_repository(
    repo_url="https://github.com/user/repo"
)

# Returns:
# {
#     'env_vars': [...],
#     'language': 'python',
#     'framework': 'pyrogram',
#     'structure': {...},
#     'dependencies': [...]
# }
```

---

## 🤝 Support & Community

- **Issues**: [GitHub Issues](https://github.com/yourusername/yagami-univerze/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/yagami-univerze/discussions)
- **Telegram**: [@YagamiUniverze](https://t.me/yagamiuniverze)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- Pyrogram for the excellent Telegram framework
- Anthropic for Claude API
- Docker for containerization
- All contributors and users

---

## 🔮 Roadmap

- [ ] Web interface for bot generation
- [ ] Support for more languages (Rust, C#)
- [ ] Built-in CI/CD pipelines
- [ ] Bot marketplace
- [ ] Template library
- [ ] Kubernetes deployment support
- [ ] Multi-bot orchestration
- [ ] Analytics dashboard
- [ ] Auto-updates for generated bots

---

**Made with 🔥 by YAGAMI UNIVERZE**

*Generate bots. Deploy anywhere. Code the future.*
