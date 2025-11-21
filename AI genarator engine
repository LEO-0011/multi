"""
YAGAMI UNIVERZE - AI Code Generation Engine
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Tuple
from anthropic import Anthropic
import openai
from bot.config import Config

logger = logging.getLogger(__name__)


class AIGenerator:
    """AI-powered code generator for Telegram bots"""
    
    def __init__(self):
        self.provider = Config.AI_PROVIDER
        if self.provider == "anthropic":
            self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            self.model = Config.AI_MODEL
        else:
            openai.api_key = Config.OPENAI_API_KEY
            self.model = "gpt-4"
    
    async def generate_bot(self, user_prompt: str, user_id: int) -> Dict:
        """
        Generate complete bot from user prompt
        
        Returns:
            Dict with structure:
            {
                'language': 'python',
                'framework': 'pyrogram',
                'files': {
                    'main.py': 'code...',
                    'requirements.txt': 'content...',
                    'Dockerfile': 'content...',
                    ...
                },
                'env_vars': ['BOT_TOKEN', 'API_ID', ...],
                'description': 'Bot description',
                'name': 'bot_name'
            }
        """
        logger.info(f"Generating bot for user {user_id}: {user_prompt}")
        
        try:
            # Step 1: Analyze prompt and determine architecture
            architecture = await self._analyze_prompt(user_prompt)
            
            # Step 2: Generate code files
            files = await self._generate_code_files(user_prompt, architecture)
            
            # Step 3: Generate deployment files
            deployment_files = await self._generate_deployment_files(architecture)
            
            # Step 4: Extract environment variables
            env_vars = await self._extract_env_vars(files)
            
            # Combine all files
            all_files = {**files, **deployment_files}
            
            return {
                'language': architecture['language'],
                'framework': architecture['framework'],
                'files': all_files,
                'env_vars': env_vars,
                'description': architecture['description'],
                'name': architecture['name'],
                'architecture': architecture
            }
            
        except Exception as e:
            logger.error(f"Error generating bot: {e}")
            raise
    
    async def _analyze_prompt(self, prompt: str) -> Dict:
        """Analyze user prompt to determine bot architecture"""
        
        system_prompt = """You are an expert Telegram bot architect. Analyze the user's request and output a JSON object with the following structure:

{
    "language": "python|nodejs|go|php",
    "framework": "pyrogram|aiogram|telegraf|etc",
    "name": "descriptive_bot_name",
    "description": "detailed description",
    "features": ["feature1", "feature2"],
    "requires_database": true|false,
    "requires_web_scraping": true|false,
    "requires_file_handling": true|false,
    "complexity": "simple|medium|complex"
}

Choose the best language and framework based on the requirements. Prefer Python with Pyrogram for most cases."""
        
        user_message = f"Analyze this bot request and determine architecture:\n\n{prompt}"
        
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\n{user_message}"}
                ]
            )
            content = response.content[0].text
        else:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            content = response.choices[0].message.content
        
        # Parse JSON from response
        try:
            # Extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            architecture = json.loads(content)
            return architecture
        except json.JSONDecodeError:
            logger.error(f"Failed to parse architecture JSON: {content}")
            # Return default architecture
            return {
                "language": "python",
                "framework": "pyrogram",
                "name": "custom_bot",
                "description": prompt,
                "features": [],
                "requires_database": False,
                "requires_web_scraping": False,
                "requires_file_handling": False,
                "complexity": "simple"
            }
    
    async def _generate_code_files(self, prompt: str, architecture: Dict) -> Dict[str, str]:
        """Generate all code files for the bot"""
        
        language = architecture['language']
        framework = architecture['framework']
        
        system_prompt = f"""You are an expert {language} developer specializing in Telegram bots using {framework}.

Generate a COMPLETE, PRODUCTION-READY Telegram bot based on the user's requirements.

IMPORTANT RULES:
1. Generate ONLY the code content, no explanations
2. Use async/await patterns
3. Include proper error handling and logging
4. Use environment variables for sensitive data
5. Follow best practices for the framework
6. Include comprehensive comments
7. Make it production-ready with proper structure

Generate these files:
- Main bot file (main.py, index.js, etc.)
- Requirements/dependencies file
- Configuration file
- Handler files (organized by feature)
- Utility/helper files
- README.md with setup instructions

Output format: Return a JSON object where keys are filenames and values are the complete file contents."""
        
        user_message = f"""Create a Telegram bot with these specifications:

DESCRIPTION: {prompt}

ARCHITECTURE:
- Language: {language}
- Framework: {framework}
- Features: {', '.join(architecture.get('features', []))}
- Requires Database: {architecture.get('requires_database', False)}
- Requires Web Scraping: {architecture.get('requires_web_scraping', False)}
- Requires File Handling: {architecture.get('requires_file_handling', False)}

Generate ALL necessary files with complete, working code."""
        
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\n{user_message}"}
                ]
            )
            content = response.content[0].text
        else:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=8000
            )
            content = response.choices[0].message.content
        
        # Parse files from response
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            files = json.loads(content)
            return files
        except json.JSONDecodeError:
            logger.error("Failed to parse files JSON, using fallback")
            return self._generate_fallback_bot(architecture)
    
    async def _generate_deployment_files(self, architecture: Dict) -> Dict[str, str]:
        """Generate Dockerfile, docker-compose.yml, and other deployment files"""
        
        language = architecture['language']
        framework = architecture['framework']
        
        files = {}
        
        # Generate Dockerfile
        if language == "python":
            files['Dockerfile'] = f"""FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Run bot
CMD ["python", "main.py"]
"""
        
        elif language == "nodejs":
            files['Dockerfile'] = f"""FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Run bot
CMD ["node", "index.js"]
"""
        
        # Generate docker-compose.yml
        bot_name = architecture['name']
        files['docker-compose.yml'] = f"""version: '3.8'

services:
  {bot_name}:
    build: .
    container_name: {bot_name}
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    networks:
      - yagami_network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  yagami_network:
    external: true
"""
        
        # Generate .env.example
        files['.env.example'] = """# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id_here
API_HASH=your_api_hash_here

# Optional: Admin user ID for notifications
ADMIN_ID=your_telegram_user_id

# Optional: Database URL (if needed)
# DATABASE_URL=sqlite:///data/bot.db

# Optional: Additional API keys (if needed)
# SOME_API_KEY=your_key_here
"""
        
        # Generate .dockerignore
        files['.dockerignore'] = """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.git
.gitignore
*.md
logs/
*.log
.DS_Store
node_modules/
"""
        
        # Generate .gitignore
        files['.gitignore'] = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Environment
.env
.venv
env/
venv/

# Logs
logs/
*.log

# Database
*.db
*.sqlite3
data/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Node
node_modules/
package-lock.json

# Docker
*.pid
"""
        
        return files
    
    async def _extract_env_vars(self, files: Dict[str, str]) -> List[str]:
        """Extract required environment variables from code"""
        
        env_vars = set()
        
        # Common environment variables for Telegram bots
        default_vars = ['BOT_TOKEN', 'API_ID', 'API_HASH']
        env_vars.update(default_vars)
        
        # Search for environment variables in code
        for filename, content in files.items():
            if isinstance(content, str):
                # Find os.getenv, process.env, etc.
                import re
                
                # Python patterns
                python_pattern = r'os\.getenv\([\'"]([A-Z_]+)[\'"]\)'
                env_vars.update(re.findall(python_pattern, content))
                
                # Node.js patterns
                node_pattern = r'process\.env\.([A-Z_]+)'
                env_vars.update(re.findall(node_pattern, content))
        
        return sorted(list(env_vars))
    
    def _generate_fallback_bot(self, architecture: Dict) -> Dict[str, str]:
        """Generate a simple fallback bot if AI generation fails"""
        
        return {
            'main.py': """import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    "generated_bot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("Hello! I'm a generated bot.")

async def main():
    await app.start()
    logger.info("Bot started!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
""",
            'requirements.txt': """pyrogram==2.0.106
tgcrypto==1.2.5
python-dotenv==1.0.0
""",
            'README.md': f"""# {architecture['name']}

{architecture['description']}

## Setup

1. Copy .env.example to .env
2. Fill in your credentials
3. Run: `docker-compose up -d`
"""
        }
