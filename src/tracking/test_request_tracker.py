import time
import pytest
from src.tracking.request_tracker import RequestTracker

@pytest.fixture
def tracker():
    """Create a RequestTracker instance with a small window for testing"""
    return RequestTracker(window_size=5)  # 5 second window for faster tests

def test_add_request(tracker):
    """Test that requests are added and tracked correctly"""
    # Add a request
    tracker.add_request()
    assert len(tracker.requests) == 1
    
    # Add another request
    tracker.add_request()
    assert len(tracker.requests) == 2

def test_cleanup_old_requests(tracker):
    """Test that old requests are cleaned up correctly"""
    # Add a request
    current_time = time.time()
    tracker.requests.append(current_time - 6)  # Add request older than window
    tracker.requests.append(current_time - 3)  # Add request within window
    tracker.requests.append(current_time)      # Add current request
    
    # Cleanup old requests
    tracker._cleanup_old_requests(current_time)
    
    # Should only have 2 requests left (within window)
    assert len(tracker.requests) == 2
    assert tracker.requests[0] == current_time - 3
    assert tracker.requests[1] == current_time

def test_rps_calculation(tracker):
    """Test RPS calculation with multiple requests"""
    # Add requests at different times
    current_time = time.time()
    tracker.requests.append(current_time - 4)  # 4 seconds ago
    tracker.requests.append(current_time - 2)  # 2 seconds ago
    tracker.requests.append(current_time)      # now
    
    # Calculate RPS
    tracker._log_rps(current_time)
    
    # Should have 3 requests in 5 second window = 0.6 RPS
    window_start = current_time - tracker.window_size
    recent_requests = [req for req in tracker.requests if req >= window_start]
    assert len(recent_requests) == 3

def test_empty_requests(tracker):
    """Test behavior with no requests"""
    current_time = time.time()
    tracker._log_rps(current_time)
    assert len(tracker.requests) == 0

def test_window_size_config():
    """Test that window size is configurable"""
    custom_window = 10
    tracker = RequestTracker(window_size=custom_window)
    assert tracker.window_size == custom_window 