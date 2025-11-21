"""
YAGAMI UNIVERZE - Code Writer
generator_engine/code_writer.py
"""

import logging
import zipfile
from pathlib import Path
from typing import Dict
import shutil

logger = logging.getLogger(__name__)


class CodeWriter:
    """Write generated code to filesystem"""
    
    async def write_bot(self, bot_dir: Path, bot_data: Dict) -> None:
        """
        Write all bot files to directory
        
        Args:
            bot_dir: Directory to write files to
            bot_data: Bot data from AIGenerator
        """
        logger.info(f"Writing bot to {bot_dir}")
        
        # Create directory
        bot_dir.mkdir(parents=True, exist_ok=True)
        
        # Write all files
        files = bot_data['files']
        
        for filename, content in files.items():
            file_path = bot_dir / filename
            
            # Create subdirectories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            try:
                if isinstance(content, bytes):
                    file_path.write_bytes(content)
                else:
                    file_path.write_text(content, encoding='utf-8')
                
                logger.debug(f"Written file: {filename}")
            except Exception as e:
                logger.error(f"Error writing {filename}: {e}")
                raise
        
        # Create additional directories
        (bot_dir / "logs").mkdir(exist_ok=True)
        (bot_dir / "data").mkdir(exist_ok=True)
        
        # Generate additional README with deployment instructions
        deployment_readme = self._generate_deployment_readme(bot_data)
        (bot_dir / "DEPLOYMENT.md").write_text(deployment_readme)
        
        logger.info(f"Successfully written {len(files)} files to {bot_dir}")
    
    async def create_archive(self, bot_dir: Path) -> Path:
        """
        Create a zip archive of the bot
        
        Args:
            bot_dir: Bot directory to archive
            
        Returns:
            Path to created archive
        """
        archive_path = bot_dir.parent / f"{bot_dir.name}.zip"
        
        logger.info(f"Creating archive: {archive_path}")
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in bot_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(bot_dir.parent)
                    zipf.write(file_path, arcname)
        
        logger.info(f"Archive created: {archive_path}")
        return archive_path
    
    def _generate_deployment_readme(self, bot_data: Dict) -> str:
        """Generate deployment instructions"""
        
        bot_name = bot_data['name']
        language = bot_data['language']
        framework = bot_data['framework']
        env_vars = bot_data['env_vars']
        
        readme = f"""# {bot_name.upper()} - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Your bot token from [@BotFather](https://t.me/BotFather)
- API credentials from [my.telegram.org](https://my.telegram.org)

### Step 1: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your credentials:

```env
# Required Variables
{chr(10).join(f'{var}=your_{var.lower()}_here' for var in env_vars[:5])}
```

### Step 2: Deploy with Docker

```bash
# Build and start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

### Step 3: Verify Deployment

Check if your bot is running:
```bash
docker-compose ps
```

View real-time logs:
```bash
docker-compose logs -f
```

## 📁 Project Structure

```
{bot_name}/
├── main.{self._get_file_extension(language)}  # Main bot entry point
├── requirements.txt / package.json            # Dependencies
├── Dockerfile                                 # Docker configuration
├── docker-compose.yml                         # Docker Compose setup
├── .env.example                               # Environment template
├── README.md                                  # Project documentation
└── logs/                                      # Log files
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
{chr(10).join(f'| {var} | ✅ | Telegram {var.replace("_", " ").lower()} |' for var in env_vars[:3])}

### Bot Features

- **Language:** {language.title()}
- **Framework:** {framework.title()}
- **Architecture:** Async/Await
- **Deployment:** Docker containerized
- **Logging:** File + Console

## 🐛 Troubleshooting

### Bot not starting?

1. Check logs:
```bash
docker-compose logs
```

2. Verify environment variables:
```bash
cat .env
```

3. Rebuild container:
```bash
docker-compose down
docker-compose up --build -d
```

### Permission errors?

```bash
# Fix permissions
sudo chown -R $USER:$USER .
```

## 📊 Monitoring

### View Logs
```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100
```

### Container Status
```bash
# Check status
docker-compose ps

# Resource usage
docker stats $(docker-compose ps -q)
```

## 🔄 Updates

### Update bot code:
```bash
# Edit your code
nano main.{self._get_file_extension(language)}

# Restart
docker-compose restart
```

### Update dependencies:
```bash
# Edit requirements
nano {self._get_requirements_file(language)}

# Rebuild
docker-compose up --build -d
```

## 🛑 Stopping the Bot

```bash
# Stop gracefully
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📦 Production Deployment

### Using VPS (Ubuntu/Debian)

1. **Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

2. **Upload bot files:**
```bash
scp -r {bot_name}/ user@your-vps:/opt/bots/
```

3. **Deploy:**
```bash
ssh user@your-vps
cd /opt/bots/{bot_name}
docker-compose up -d
```

### Nginx Reverse Proxy (for webhooks)

If your bot uses webhooks, set up Nginx:

```nginx
server {{
    listen 443 ssl;
    server_name bot.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {{
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
```

## 🔐 Security

- Never commit `.env` file
- Use strong, unique tokens
- Keep dependencies updated
- Enable firewall on your VPS
- Use HTTPS for webhooks

## 📞 Support

Generated by **YAGAMI UNIVERZE**
For issues, check logs and verify configuration.

---

**Happy Botting! 🤖**
"""
        return readme
    
    def _get_file_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            'python': 'py',
            'nodejs': 'js',
            'go': 'go',
            'php': 'php'
        }
        return extensions.get(language, 'txt')
    
    def _get_requirements_file(self, language: str) -> str:
        """Get requirements file name for language"""
        files = {
            'python': 'requirements.txt',
            'nodejs': 'package.json',
            'go': 'go.mod',
            'php': 'composer.json'
        }
        return files.get(language, 'requirements.txt')
