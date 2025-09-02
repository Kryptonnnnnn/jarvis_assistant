import pyttsx3
import threading
from config.config import Config
from utils.logger import get_logger

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.logger = get_logger(__name__)
        self.lock = threading.Lock()
        
        # Configure voice settings
        self.setup_voice()
        
    def setup_voice(self):
        """Configure TTS voice properties"""
        try:
            voices = self.engine.getProperty('voices')
            
            # Try to set a male voice (for JARVIS feel)
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
                    
            # Set rate and volume
            self.engine.setProperty('rate', Config.TTS_RATE)
            self.engine.setProperty('volume', Config.TTS_VOLUME)
        except Exception as e:
            self.logger.error(f"Error setting up voice: {e}")
        
    def speak(self, text):
        """Convert text to speech"""
        if not text:
            return
            
        with self.lock:
            try:
                self.logger.debug(f"Speaking: {text}")
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self.logger.error(f"Error in text-to-speech: {e}")