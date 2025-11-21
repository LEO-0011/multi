"""
utils/docker_utils.py
"""

import asyncio
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class DockerUtils:
    """Docker utility functions"""

    @staticmethod
    async def is_docker_available() -> bool:
        """Check if Docker is available"""
        try:
            process = await asyncio.create_subprocess_exec(
                'docker', '--version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except FileNotFoundError:
            return False

    @staticmethod
    async def is_compose_available() -> bool:
        """Check if Docker Compose is available"""
        try:
            process = await asyncio.create_subprocess_exec(
                'docker-compose', '--version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except FileNotFoundError:
            return False

    @staticmethod
    async def network_exists(network_name: str) -> bool:
        """Check if Docker network exists"""
        try:
            process = await asyncio.create_subprocess_exec(
                'docker', 'network', 'ls',
                '--format', '{{.Name}}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            networks = stdout.decode().split('\n')
            return network_name in networks
        except Exception:
            return False

    @staticmethod
    async def create_network(network_name: str) -> bool:
        """Create Docker network"""
        try:
            process = await asyncio.create_subprocess_exec(
                'docker', 'network', 'create', network_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except Exception as e:
            logger.error(f"Failed to create network: {e}")
            return False

    @staticmethod
    async def get_container_status(container_name: str) -> Optional[str]:
        """Get container status"""
        try:
            process = await asyncio.create_subprocess_exec(
                'docker', 'ps', '-a',
                '--filter', f'name={container_name}',
                '--format', '{{.Status}}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            status = stdout.decode().strip()
            return status if status else None
        except Exception:
            return None
