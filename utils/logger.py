import logging
import os
from config.config import Config

def setup_logger():
    """Setup main logger for the application"""
    # Ensure log directory exists
    os.makedirs(Config.LOGS_DIR, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('JARVIS')

def get_logger(name):
    """Get logger for specific module"""
    return logging.getLogger(name)