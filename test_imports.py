import os
import sys

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Testing imports...")

try:
    from config.config import Config
    print("✅ Config imported successfully")
except Exception as e:
    print(f"❌ Config import failed: {e}")

try:
    from utils.logger import setup_logger
    print("✅ Logger imported successfully")
except Exception as e:
    print(f"❌ Logger import failed: {e}")

try:
    from core.text_to_speech import TextToSpeech
    print("✅ TTS imported successfully")
except Exception as e:
    print(f"❌ TTS import failed: {e}")

print("Import test completed!")