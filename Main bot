"""
YAGAMI UNIVERZE - Universal Telegram Bot Generator
Main Bot Entry Point
"""

import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.handlers.start_handler import handle_start
from bot.handlers.generate_handler import handle_generate
from bot.handlers.repo_scan_handler import handle_repo_scan
from bot.handlers.deploy_handler import handle_deploy
from bot.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/yagami.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize bot
app = Client(
    "yagami_univerze",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=Config.WORKERS
)


@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    await handle_start(client, message)


@app.on_message(filters.command("generate") & filters.private)
async def generate_command(client: Client, message: Message):
    """Handle /generate command"""
    await handle_generate(client, message)


@app.on_message(filters.command("scan") & filters.private)
async def scan_command(client: Client, message: Message):
    """Handle /scan command for GitHub repo scanning"""
    await handle_repo_scan(client, message)


@app.on_message(filters.command("deploy") & filters.private)
async def deploy_command(client: Client, message: Message):
    """Handle /deploy command"""
    await handle_deploy(client, message)


@app.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    """Handle /help command"""
    help_text = """
🔥 **YAGAMI UNIVERZE Commands**

/start - Start the bot
/generate <description> - Generate a bot from description
/scan <github_url> - Scan GitHub repo for env vars
/deploy <bot_id> - Deploy generated bot
/help - Show this help message

**Examples:**

`/generate Create an RSS feed bot that forwards new items to channel`

`/scan https://github.com/user/telegram-bot`

`/deploy bot_20231121_123456`
    """
    await message.reply_text(help_text)


@app.on_message(filters.text & filters.private & ~filters.command(["start", "generate", "scan", "deploy", "help"]))
async def handle_text(client: Client, message: Message):
    """Handle plain text as generation request"""
    await handle_generate(client, message, direct_prompt=True)


async def main():
    """Main entry point"""
    logger.info("🔥 Starting YAGAMI UNIVERZE...")
    
    try:
        await app.start()
        logger.info("✅ YAGAMI UNIVERZE is now running!")
        
        # Send startup notification to admin
        try:
            await app.send_message(
                Config.ADMIN_ID,
                "🔥 **YAGAMI UNIVERZE** is now online and ready to generate bots!"
            )
        except Exception as e:
            logger.error(f"Failed to send startup notification: {e}")
        
        # Keep the bot running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        await app.stop()
        logger.info("🛑 YAGAMI UNIVERZE stopped")


if __name__ == "__main__":
    asyncio.run(main())
