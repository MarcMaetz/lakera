from datetime import datetime
import time
from typing import Dict, List
import json
from pathlib import Path
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class RequestTracker:
    def __init__(self, storage_file='logs/request_data.json'):
        self.storage_file = storage_file
        self.windows = {
            '1s': [],    # Last second
            '1m': [],    # Last minute
            '1h': []     # Last hour
        }
        self.load_data()
    
    def add_request(self):
        current_time = time.time()
        for window, times in self.windows.items():
            times.append(current_time)
            # Remove old requests based on window size
            if window == '1s':
                times[:] = [t for t in times if current_time - t <= 1.0]
            elif window == '1m':
                times[:] = [t for t in times if current_time - t <= 60.0]
            elif window == '1h':
                times[:] = [t for t in times if current_time - t <= 3600.0]
        
        # Save data after each request
        self.save_data()
    
    def get_stats(self):
        return {
            '1s': len(self.windows['1s']),
            '1m': len(self.windows['1m']),
            '1h': len(self.windows['1h'])
        }
    
    def format_timestamp(self, timestamp: float) -> str:
        """Convert Unix timestamp to human-readable format"""
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    def get_formatted_stats(self) -> Dict[str, List[str]]:
        """Get stats with human-readable timestamps"""
        return {
            window: [self.format_timestamp(float(t)) for t in times]
            for window, times in self.windows.items()
        }
    
    def save_data(self):
        """Save current request data to file"""
        try:
            # Convert timestamps to strings for JSON serialization
            data = {
                window: [str(t) for t in times]
                for window, times in self.windows.items()
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=4)  # Add indentation for readability
            
            logger.debug("Request data saved successfully")
        except Exception as e:
            logger.error(f"Error saving request data: {str(e)}")
    
    def load_data(self):
        """Load request data from file"""
        try:
            if Path(self.storage_file).exists():
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                
                # Convert string timestamps back to floats
                self.windows = {
                    window: [float(t) for t in times]
                    for window, times in data.items()
                }
                
                # Clean up old data
                current_time = time.time()
                for window, times in self.windows.items():
                    if window == '1s':
                        times[:] = [t for t in times if current_time - t <= 1.0]
                    elif window == '1m':
                        times[:] = [t for t in times if current_time - t <= 60.0]
                    elif window == '1h':
                        times[:] = [t for t in times if current_time - t <= 3600.0]
                
                logger.info("Request data loaded successfully")
            else:
                logger.info("No existing request data found")
        except Exception as e:
            logger.error(f"Error loading request data: {str(e)}")
            # Initialize with empty data if loading fails
            self.windows = {
                '1s': [],
                '1m': [],
                '1h': []
            } 