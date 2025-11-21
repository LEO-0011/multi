"""
bot/handlers/generate_handler.py
"""

import logging
import asyncio
from datetime import datetime
from pathlib import Path
from pyrogram import Client
from pyrogram.types import Message
from generator_engine.ai_generator import AIGenerator
from generator_engine.code_writer import CodeWriter
from bot.config import Config

logger = logging.getLogger(__name__)


async def handle_generate(client: Client, message: Message, direct_prompt: bool = False):
    """Handle bot generation request"""

    user_id = message.from_user.id

    # Extract prompt
    if direct_prompt:
        prompt = message.text
    else:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await message.reply_text(
                "❌ Please provide a bot description.\n\n"
                "**Example:**\n"
                "`/generate Create an auto-reply bot that responds to keywords`"
            )
            return
        prompt = command_parts[1]

    # Send processing message
    status_msg = await message.reply_text(
        "🔥 **YAGAMI UNIVERZE is working...**\n\n"
        "⏳ Analyzing your request..."
    )

    try:
        # Initialize generator
        generator = AIGenerator()

        # Update status
        await status_msg.edit_text(
            "🔥 **YAGAMI UNIVERZE is working...**\n\n"
            "🧠 Generating bot architecture...\n"
            "⏳ This may take 30-60 seconds..."
        )

        # Generate bot
        bot_data = await generator.generate_bot(prompt, user_id)

        # Update status
        await status_msg.edit_text(
            "🔥 **YAGAMI UNIVERZE is working...**\n\n"
            "📝 Writing files...\n"
            "⏳ Almost done..."
        )

        # Create bot directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        bot_name = bot_data['name']
        bot_id = f"{bot_name}_{timestamp}"
        bot_dir = Config.GENERATED_BOTS_DIR / bot_id

        # Write files
        writer = CodeWriter()
        await writer.write_bot(bot_dir, bot_data)

        # Create archive
        archive_path = await writer.create_archive(bot_dir)

        # Success message
        success_text = f"""
✅ **Bot Generated Successfully!**

📦 **Bot Name:** `{bot_name}`
🆔 **Bot ID:** `{bot_id}`
💻 **Language:** {bot_data['language']}
🔧 **Framework:** {bot_data['framework']}

📁 **Generated Files:**
{chr(10).join(f'  • {f}' for f in list(bot_data['files'].keys())[:10])}
{f'  ... and {len(bot_data["files"]) - 10} more' if len(bot_data['files']) > 10 else ''}

🔐 **Required Environment Variables:**
```
{chr(10).join(bot_data['env_vars'])}
```

📥 **Download your bot below!**

**Next Steps:**
1️⃣ Download the bot archive
2️⃣ Extract and fill in .env file
3️⃣ Run: `docker-compose up -d`

Or use: `/deploy {bot_id}` for auto-deployment
        """

        # Send archive
        await message.reply_document(
            document=str(archive_path),
            caption=success_text,
            file_name=f"{bot_id}.zip"
        )

        # Delete status message
        await status_msg.delete()

        logger.info(f"Successfully generated bot {bot_id} for user {user_id}")

    except Exception as e:
        logger.error(f"Error generating bot: {e}")
        await status_msg.edit_text(
            f"❌ **Error generating bot**\n\n"
            f"Error: {str(e)}\n\n"
            f"Please try again or contact admin."
        )
