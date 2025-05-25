import time
from collections import deque
from typing import Deque
from src.utils.logger import setup_rps_logger

rps_logger = setup_rps_logger()

class RequestTracker:
    def __init__(self, window_size: int = 60):
        """
        Initialize the request tracker with a sliding window.
        
        Args:
            window_size: Size of the sliding window in seconds (default: 60)
        """
        self.window_size = window_size
        self.requests: Deque[float] = deque()  # Only store timestamps
    
    def add_request(self) -> None:
        """Add a new request to the tracker and log the current RPS."""
        current_time = time.time()
        self.requests.append(current_time)
        self._cleanup_old_requests(current_time)
        self._log_rps(current_time)
    
    def _cleanup_old_requests(self, current_time: float) -> None:
        """Remove requests older than the window size."""
        while self.requests and current_time - self.requests[0] > self.window_size:
            self.requests.popleft()
    
    def _log_rps(self, current_time: float) -> None:
        """Calculate and log the current RPS."""
        if not self.requests:
            return
        
        window_start = current_time - self.window_size
        recent_requests = [req for req in self.requests if req >= window_start]
        
        if recent_requests:
            rps = len(recent_requests) / self.window_size
            rps_logger.info("RPS: %.2f", rps) 