"""
YAGAMI UNIVERZE Configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration"""
    
    # Telegram Bot Settings
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
    
    # Bot Settings
    WORKERS = int(os.getenv("WORKERS", "8"))
    MAX_CONCURRENT_GENERATIONS = int(os.getenv("MAX_CONCURRENT_GENERATIONS", "3"))
    
    # AI API Settings
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "anthropic")  # anthropic or openai
    AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-4-20250514")
    
    # GitHub Settings
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    GENERATED_BOTS_DIR = BASE_DIR / "generated_bots"
    LOGS_DIR = BASE_DIR / "logs"
    TEMP_DIR = BASE_DIR / "temp"
    
    # Docker Settings
    DOCKER_NETWORK = os.getenv("DOCKER_NETWORK", "yagami_network")
    DOCKER_REGISTRY = os.getenv("DOCKER_REGISTRY", "")
    
    # Database (for tracking generated bots)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///yagami.db")
    
    # Generation Settings
    SUPPORTED_LANGUAGES = ["python", "nodejs", "go", "php"]
    SUPPORTED_FRAMEWORKS = {
        "python": ["pyrogram", "aiogram", "telebot", "python-telegram-bot"],
        "nodejs": ["telegraf", "node-telegram-bot-api", "grammy"],
        "go": ["telebot", "tgbotapi"],
        "php": ["telegram-bot-sdk"]
    }
    
    # Rate Limiting
    MAX_GENERATIONS_PER_USER = int(os.getenv("MAX_GENERATIONS_PER_USER", "10"))
    GENERATION_COOLDOWN = int(os.getenv("GENERATION_COOLDOWN", "60"))  # seconds
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN is required")
        if not cls.API_ID or cls.API_ID == 0:
            errors.append("API_ID is required")
        if not cls.API_HASH:
            errors.append("API_HASH is required")
        if not cls.ANTHROPIC_API_KEY and not cls.OPENAI_API_KEY:
            errors.append("Either ANTHROPIC_API_KEY or OPENAI_API_KEY is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        cls.GENERATED_BOTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.TEMP_DIR.mkdir(parents=True, exist_ok=True)


# Validate config on import
Config.validate()
Config.setup_directories()
