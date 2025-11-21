"""
bot/handlers/repo_scan_handler.py
"""

import logging
from pyrogram import Client
from pyrogram.types import Message
from generator_engine.repo_scanner import RepoScanner

logger = logging.getLogger(__name__)


async def handle_repo_scan(client: Client, message: Message):
    """Handle GitHub repository scanning"""

    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) < 2:
        await message.reply_text(
            "❌ Please provide a GitHub repository URL.\n\n"
            "**Example:**\n"
            "`/scan https://github.com/username/telegram-bot`"
        )
        return

    repo_url = command_parts[1].strip()

    # Validate URL
    if not repo_url.startswith('https://github.com/'):
        await message.reply_text(
            "❌ Invalid GitHub URL.\n\n"
            "Please provide a valid GitHub repository URL starting with:\n"
            "`https://github.com/`"
        )
        return

    status_msg = await message.reply_text(
        "🔍 **Scanning repository...**\n\n"
        "⏳ Cloning and analyzing code..."
    )

    try:
        scanner = RepoScanner()
        scan_results = await scanner.scan_repository(repo_url)

        # Generate env template
        env_template = scanner.generate_env_template(
            scan_results['env_vars'],
            scan_results['readme_content']
        )

        # Create results message
        results_text = f"""
✅ **Repository Scan Complete!**

📦 **Repository:** {repo_url}
💻 **Language:** {scan_results['language']}
🔧 **Framework:** {scan_results['framework']}

📁 **Structure:**
  Files: {len(scan_results['structure']['files'])}
  Directories: {len(scan_results['structure']['directories'])}

📦 **Dependencies:** {len(scan_results['dependencies'])}
{chr(10).join(f'  • {dep}' for dep in scan_results['dependencies'][:5])}
{f'  ... and {len(scan_results["dependencies"]) - 5} more' if len(scan_results['dependencies']) > 5 else ''}

🔐 **Environment Variables Found:** {len(scan_results['env_vars'])}
```
{chr(10).join(scan_results['env_vars'])}
```

🔧 **Configuration:**
{chr(10).join(f'  • {k.replace("_", " ").title()}: {"✅" if v else "❌"}' for k, v in scan_results['config_patterns'].items())}

📄 **Generated .env template below ⬇️**
        """

        # Send results
        await status_msg.edit_text(results_text)

        # Send env template as file
        env_file_path = Config.TEMP_DIR / f"env_template_{message.from_user.id}.txt"
        env_file_path.write_text(env_template)

        await message.reply_document(
            document=str(env_file_path),
            caption="📄 **.env Template**\n\nFill in your values and rename to `.env`",
            file_name=".env.example"
        )

        env_file_path.unlink()

    except Exception as e:
        logger.error(f"Error scanning repository: {e}")
        await status_msg.edit_text(
            f"❌ **Error scanning repository**\n\n"
            f"Error: {str(e)}\n\n"
            f"Make sure the repository is public or you've set GITHUB_TOKEN."
        )
