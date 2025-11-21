"""
YAGAMI UNIVERZE - Bot Handlers
bot/handlers/start_handler.py
"""

import logging
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)


async def handle_start(client: Client, message: Message):
    """Handle /start command"""

    welcome_text = """
🔥 **YAGAMI UNIVERZE** - Universal Bot Generator

I can create ANY Telegram bot for you automatically!

**What I can do:**
✅ Generate complete bot code from your description
✅ Create Dockerfile and docker-compose setup
✅ Scan GitHub repos and extract env variables
✅ Deploy bots automatically
✅ Support multiple languages (Python, Node.js, Go, PHP)

**How to use:**
1️⃣ Describe the bot you want
2️⃣ I'll generate all the code
3️⃣ Deploy with one command

**Examples:**
• `/generate Create an RSS feed bot that posts to channel`
• `/generate Build a file converter bot for documents`
• `/scan https://github.com/username/bot-repo`

Just describe what you want, and I'll build it! 🚀
    """

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Examples", callback_data="examples")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
        [InlineKeyboardButton("🔧 My Bots", callback_data="my_bots")]
    ])

    await message.reply_text(welcome_text, reply_markup=keyboard)
