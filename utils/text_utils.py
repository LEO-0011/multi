"""
utils/text_utils.py
"""

import re
from typing import List


def truncate_text(text: str, max_length: int = 4000, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def split_message(text: str, max_length: int = 4000) -> List[str]:
    """Split long message into chunks"""
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""

    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + '\n'
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + '\n'

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def format_duration(seconds: float) -> str:
    """Format seconds into human readable duration"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def extract_code_blocks(text: str) -> List[str]:
    """Extract code blocks from markdown text"""
    pattern = r'```(?:\w+)?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def clean_markdown(text: str) -> str:
    """Remove markdown formatting"""
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`.*?`', '', text)
    # Remove bold
    text = re.sub(r'\*\*.*?\*\*', '', text)
    # Remove italic
    text = re.sub(r'\*.*?\*', '', text)
    # Remove links
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    return text.strip()
