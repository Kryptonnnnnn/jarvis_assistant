import os
import sys
import threading
import time
import traceback

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import all required modules (NO DOTS - absolute imports only)
try:
    from config.config import Config
    from core.speech_recognition import SpeechRecognizer
    from core.text_to_speech import TextToSpeech
    from core.nlp_processor import NLPProcessor
    from core.conversation_memory import ConversationMemory
    from utils.logger import setup_logger
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all modules are created and dependencies are installed.")
    print("Run: pip install speechrecognition pyttsx3 pyaudio psutil fuzzywuzzy python-levenshtein")
    sys.exit(1)

class JarvisAssistant:
    def __init__(self):
        """Initialize JARVIS Assistant"""
        print("Initializing JARVIS...")
        
        try:
            # Initialize configuration
            self.config = Config()
            
            # Setup logger
            self.logger = setup_logger()
            self.logger.info("Starting JARVIS Assistant...")
            
            # Initialize core components
            print("Setting up speech recognition...")
            self.speech_recognizer = SpeechRecognizer()
            
            print("Setting up text-to-speech...")
            self.tts = TextToSpeech()
            
            print("Setting up natural language processor...")
            self.nlp_processor = NLPProcessor()
            
            print("Setting up conversation memory...")
            self.memory = ConversationMemory()
            
            # Assistant state
            self.running = False
            self.listening = False
            
            # Wake words that activate the assistant
            self.wake_words = ["jarvis", "hey jarvis", "ok jarvis", "hello jarvis"]
            
            print("JARVIS initialization complete!")
            self.logger.info("JARVIS initialized successfully")
            
        except Exception as e:
            print(f"Error initializing JARVIS: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            sys.exit(1)
    
    def start(self):
        """Start the voice assistant"""
        print("\n" + "="*50)
        print("🤖 JARVIS Voice Assistant Starting...")
        print("="*50)
        
        self.running = True
        
        # Initial greeting
        greeting = "Hello! JARVIS is now online and ready to assist you. Say 'Hey Jarvis' to activate me."
        print(f"JARVIS: {greeting}")
        self.tts.speak(greeting)
        self.logger.info("JARVIS started successfully")
        
        try:
            # Start main listening loop
            self.listen_loop()
        except KeyboardInterrupt:
            print("\nShutdown requested by user...")
            self.shutdown()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.logger.error(f"Unexpected error: {e}")
            self.shutdown()
    
    def listen_loop(self):
        """Main listening loop for wake words"""
        print("\nListening for wake word...")
        print("Wake words: 'Hey Jarvis', 'Jarvis', 'OK Jarvis', 'Hello Jarvis'")
        print("Press Ctrl+C to exit\n")
        
        consecutive_failures = 0
        max_failures = 5
        
        while self.running:
            try:
                # Listen for wake word
                print("🎤 Listening...", end=" ", flush=True)
                audio_text = self.speech_recognizer.listen(timeout=1)
                
                if audio_text:
                    print(f"Heard: '{audio_text}'")
                    
                    if self.is_wake_word(audio_text.lower()):
                        print("✅ Wake word detected!")
                        self.handle_wake_word()
                        consecutive_failures = 0
                    else:
                        print("❌ Not a wake word, continuing to listen...")
                else:
                    print("No speech detected")
                
                consecutive_failures = 0
                
            except Exception as e:
                consecutive_failures += 1
                print(f"\n❌ Error in listen loop: {e}")
                
                if consecutive_failures >= max_failures:
                    print(f"Too many consecutive failures ({max_failures}). Shutting down...")
                    break
                
                print("Retrying in 2 seconds...")
                time.sleep(2)
    
    def is_wake_word(self, text):
        """Check if the spoken text contains a wake word"""
        if not text:
            return False
        
        text = text.strip().lower()
        
        for wake_word in self.wake_words:
            if wake_word in text:
                self.logger.info(f"Wake word detected: {wake_word} in '{text}'")
                return True
        
        return False
    
    def handle_wake_word(self):
        """Handle wake word detection"""
        try:
            # Acknowledge wake word
            acknowledgment = "Yes, how can I help you?"
            print(f"JARVIS: {acknowledgment}")
            self.tts.speak(acknowledgment)
            
            # Listen for command
            self.process_command()
            
        except Exception as e:
            error_msg = f"Error handling wake word: {e}"
            print(f"❌ {error_msg}")
            self.logger.error(error_msg)
    
    def process_command(self):
        """Process voice command after wake word"""
        try:
            print("🎤 Listening for command...")
            
            # Listen for command with longer timeout
            command = self.speech_recognizer.listen(timeout=10, phrase_timeout=2)
            
            if command:
                print(f"Command received: '{command}'")
                self.logger.info(f"Command received: {command}")
                
                # Add to conversation memory
                self.memory.add_user_message(command)
                
                # Process the command
                print("🧠 Processing command...")
                response = self.nlp_processor.process_command(command, self.memory)
                
                if response:
                    print(f"JARVIS: {response}")
                    self.tts.speak(response)
                    self.memory.add_assistant_message(response)
                    self.logger.info(f"Response: {response}")
                else:
                    fallback = "I'm sorry, I couldn't process that command."
                    print(f"JARVIS: {fallback}")
                    self.tts.speak(fallback)
                    
            else:
                timeout_msg = "I didn't hear a command. Please try again."
                print(f"JARVIS: {timeout_msg}")
                self.tts.speak(timeout_msg)
                
        except Exception as e:
            error_msg = f"Error processing command: {e}"
            print(f"❌ {error_msg}")
            self.logger.error(error_msg)
            
            # Inform user of error
            error_response = "Sorry, I encountered an error processing your command."
            self.tts.speak(error_response)
        
        finally:
            print("\nReturning to wake word detection...\n")
    
    def shutdown(self):
        """Shutdown the assistant gracefully"""
        print("\n🔴 Shutting down JARVIS...")
        
        self.running = False
        
        try:
            goodbye = "Goodbye! JARVIS is going offline."
            print(f"JARVIS: {goodbye}")
            self.tts.speak(goodbye)
            
            self.logger.info("JARVIS shutdown completed")
            print("✅ JARVIS has been shut down successfully.")
            
        except Exception as e:
            print(f"Error during shutdown: {e}")
        
        finally:
            print("Exiting...")
            sys.exit(0)

def test_dependencies():
    """Test if all required dependencies are available"""
    print("Testing dependencies...")
    
    dependencies = [
        ('speech_recognition', 'speechrecognition'),
        ('pyttsx3', 'pyttsx3'),
        ('psutil', 'psutil'),
        ('fuzzywuzzy', 'fuzzywuzzy')
    ]
    
    missing = []
    for module, package in dependencies:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} (install with: pip install {package})")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print(f"Install them with: pip install {' '.join(missing)}")
        return False
    
    print("✅ All dependencies are available!")
    return True

def test_microphone():
    """Test microphone access"""
    print("Testing microphone access...")
    try:
        import pyaudio
        import speech_recognition as sr
        
        # Test microphone
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        print("✅ Microphone access successful!")
        return True
        
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        print("Make sure your microphone is connected and working.")
        return False

def main():
    """Main entry point"""
    print("🤖 JARVIS Voice Assistant")
    print("=" * 40)
    
    # Test dependencies first
    if not test_dependencies():
        print("\nPlease install missing dependencies before running JARVIS.")
        return
    
    # Test microphone
    if not test_microphone():
        print("\nPlease check your microphone setup.")
        return
    
    try:
        # Create and start JARVIS
        jarvis = JarvisAssistant()
        jarvis.start()
        
    except KeyboardInterrupt:
        print("\nExiting JARVIS...")
    except Exception as e:
        print(f"Failed to start JARVIS: {e}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()