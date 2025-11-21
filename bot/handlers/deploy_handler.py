"""
bot/handlers/deploy_handler.py
"""

import logging
import asyncio
import subprocess
from pathlib import Path
from pyrogram import Client
from pyrogram.types import Message
from bot.config import Config

logger = logging.getLogger(__name__)


async def handle_deploy(client: Client, message: Message):
    """Handle bot deployment"""

    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) < 2:
        await message.reply_text(
            "❌ Please provide a bot ID.\n\n"
            "**Example:**\n"
            "`/deploy bot_20231121_123456`\n\n"
            "You can find bot IDs in your generated bot messages."
        )
        return

    bot_id = command_parts[1].strip()
    bot_dir = Config.GENERATED_BOTS_DIR / bot_id

    if not bot_dir.exists():
        await message.reply_text(
            f"❌ **Bot not found**\n\n"
            f"Bot ID: `{bot_id}`\n\n"
            f"Make sure you've generated this bot first using `/generate`"
        )
        return

    status_msg = await message.reply_text(
        "🚀 **Deploying bot...**\n\n"
        "⏳ Checking environment..."
    )

    try:
        # Check if .env exists
        env_file = bot_dir / ".env"
        if not env_file.exists():
            await status_msg.edit_text(
                "❌ **Missing .env file**\n\n"
                "Please create a .env file with your configuration first.\n\n"
                "You can find the .env.example in your bot archive."
            )
            return

        # Update status
        await status_msg.edit_text(
            "🚀 **Deploying bot...**\n\n"
            "🐳 Building Docker image..."
        )

        # Build Docker image
        build_process = await asyncio.create_subprocess_exec(
            'docker-compose', 'build',
            cwd=str(bot_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await build_process.communicate()

        if build_process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            await status_msg.edit_text(
                f"❌ **Build failed**\n\n"
                f"```\n{error_msg[:500]}\n```"
            )
            return

        # Update status
        await status_msg.edit_text(
            "🚀 **Deploying bot...**\n\n"
            "🐳 Starting containers..."
        )

        # Start containers
        start_process = await asyncio.create_subprocess_exec(
            'docker-compose', 'up', '-d',
            cwd=str(bot_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await start_process.communicate()

        if start_process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            await status_msg.edit_text(
                f"❌ **Deployment failed**\n\n"
                f"```\n{error_msg[:500]}\n```"
            )
            return

        # Success
        await status_msg.edit_text(
            f"✅ **Bot deployed successfully!**\n\n"
            f"🆔 **Bot ID:** `{bot_id}`\n"
            f"🐳 **Status:** Running\n\n"
            f"**Useful commands:**\n"
            f"• View logs: `docker-compose logs -f`\n"
            f"• Stop bot: `docker-compose down`\n"
            f"• Restart: `docker-compose restart`\n\n"
            f"📁 Bot directory: `{bot_dir}`"
        )

        logger.info(f"Successfully deployed bot {bot_id}")

    except Exception as e:
        logger.error(f"Error deploying bot: {e}")
        await status_msg.edit_text(
            f"❌ **Deployment error**\n\n"
            f"Error: {str(e)}\n\n"
            f"Make sure Docker is installed and running."
        )
