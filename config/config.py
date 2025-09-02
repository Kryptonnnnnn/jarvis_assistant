import os
from pathlib import Path

class Config:
    # Base directories
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Speech recognition settings
    SPEECH_RECOGNITION_TIMEOUT = 5
    SPEECH_RECOGNITION_PHRASE_TIMEOUT = 0.3
    
    # Text-to-speech settings
    TTS_RATE = 180
    TTS_VOLUME = 0.9
    
    # OpenAI settings (optional)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Weather API (optional)
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    
    # Default location
    DEFAULT_LOCATION = "New York"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = LOGS_DIR / "jarvis.log"
    
    # Conversation settings
    MAX_CONVERSATION_HISTORY = 10
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)

# Initialize directories when imported
Config.ensure_directories()