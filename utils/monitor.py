"""
YAGAMI UNIVERZE - Utility Modules
utils/monitor.py
"""

import asyncio
import logging
import psutil
import time
from datetime import datetime
from pathlib import Path
from bot.config import Config

logger = logging.getLogger(__name__)


class SystemMonitor:
    """Monitor system resources and bot health"""

    def __init__(self):
        self.start_time = time.time()

    async def run(self):
        """Run monitoring loop"""
        logger.info("Starting system monitor...")

        while True:
            try:
                await self.check_health()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(60)

    async def check_health(self):
        """Check system health"""

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent

        # Log if high usage
        if cpu_percent > 80:
            logger.warning(f"High CPU usage: {cpu_percent}%")

        if memory_percent > 80:
            logger.warning(f"High memory usage: {memory_percent}%")

        if disk_percent > 90:
            logger.warning(f"High disk usage: {disk_percent}%")

        # Log health info
        uptime = time.time() - self.start_time
        logger.info(
            f"Health: CPU={cpu_percent}% MEM={memory_percent}% "
            f"DISK={disk_percent}% UPTIME={uptime:.0f}s"
        )
