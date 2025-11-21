"""
utils/validator.py
"""

import re
from typing import Optional


class Validator:
    """Validate user inputs"""

    @staticmethod
    def validate_github_url(url: str) -> Optional[str]:
        """
        Validate GitHub URL

        Returns:
            Cleaned URL or None if invalid
        """
        pattern = r'https://github\.com/[\w-]+/[\w.-]+'

        if re.match(pattern, url):
            return url.rstrip('/')

        return None

    @staticmethod
    def validate_bot_name(name: str) -> bool:
        """Validate bot name"""
        # Must be alphanumeric with underscores
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]{2,30}$'
        return bool(re.match(pattern, name))

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe filesystem use"""
        # Remove or replace dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        return filename[:255]  # Max filename length
