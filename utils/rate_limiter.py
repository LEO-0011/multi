"""
utils/rate_limiter.py
"""

import time
from collections import defaultdict
from typing import Dict


class RateLimiter:
    """Rate limiting for bot generations"""

    def __init__(self):
        self.user_requests: Dict[int, list] = defaultdict(list)

    def can_generate(self, user_id: int, max_requests: int = 10, window: int = 3600) -> bool:
        """
        Check if user can generate a bot

        Args:
            user_id: Telegram user ID
            max_requests: Maximum requests allowed
            window: Time window in seconds

        Returns:
            True if allowed, False if rate limited
        """
        now = time.time()

        # Clean old requests
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id]
            if now - req_time < window
        ]

        # Check limit
        if len(self.user_requests[user_id]) >= max_requests:
            return False

        # Add new request
        self.user_requests[user_id].append(now)
        return True

    def get_wait_time(self, user_id: int, window: int = 3600) -> int:
        """Get seconds until user can generate again"""
        if not self.user_requests[user_id]:
            return 0

        oldest_request = min(self.user_requests[user_id])
        wait_time = window - (time.time() - oldest_request)
        return max(0, int(wait_time))
