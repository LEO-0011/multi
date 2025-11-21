"""
utils/file_utils.py
"""

import aiofiles
import hashlib
from pathlib import Path
from typing import Optional


async def read_file_async(file_path: Path) -> Optional[str]:
    """Asynchronously read file"""
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    except Exception:
        return None


async def write_file_async(file_path: Path, content: str):
    """Asynchronously write file"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(content)


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file"""
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in MB"""
    return file_path.stat().st_size / (1024 * 1024)
