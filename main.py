import os
import sys
import threading
import time
import traceback
from datetime import datetime

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

# Try to import GUI components
try:
    from gui_server import gui
    GUI_AVAILABLE = True
    print("✅ GUI components loaded")
except ImportError:
    GUI_AVAILABLE = False
    print("⚠️ GUI not available - running in console mode")

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
            self.is_active = False  # For wake word activation
            
            # GUI integration attributes
            self.gui_socket = None
            self.activity_logs = []
            self.start_time = datetime.now()
            
            # Enhanced wake words with common mishears
            self.wake_words = [
                "jarvis", "hey jarvis", "ok jarvis", "hello jarvis",
                "java", "hey java", "ok java",      # Common mishears
                "jervis", "jarrius", "jarvus"       # Phonetic variations
            ]
            
            print("JARVIS initialization complete!")
            self.logger.info("JARVIS initialized successfully")
            
        except Exception as e:
            print(f"Error initializing JARVIS: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            sys.exit(1)
    
    def log_activity(self, activity_type, message):
        """Log activity for GUI display"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'type': activity_type,
            'message': message
        }
        
        self.activity_logs.append(log_entry)
        
        # Keep only last 100 logs
        if len(self.activity_logs) > 100:
            self.activity_logs = self.activity_logs[-100:]
        
        # Update GUI if available
        if GUI_AVAILABLE and hasattr(self, 'gui_socket') and self.gui_socket:
            try:
                gui.send_update(activity_type, message)
            except:
                pass  # GUI might not be connected
        
        # Also log to console
        self.logger.info(f"[{activity_type}] {message}")
    
    def start_with_gui(self):
        """Start JARVIS with GUI - NEW METHOD"""
        if not GUI_AVAILABLE:
            print("❌ GUI not available, starting normal mode")
            self.start()
            return
        
        print("🖥️ Starting JARVIS with GUI...")
        
        # Start the GUI server
        self.gui_socket = gui.start_gui(self)
        
        # Log GUI startup
        self.log_activity('SYSTEM', 'JARVIS GUI initialized')
        
        # Start JARVIS normally
        self.start()
    
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
        self.log_activity('SYSTEM', 'JARVIS started successfully')
        
        try:
            # Start main listening loop
            self.listen_loop()
        except KeyboardInterrupt:
            print("\nShutdown requested by user...")
            self.shutdown()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.logger.error(f"Unexpected error: {e}")
            self.log_activity('ERROR', f'Unexpected error: {e}')
            self.shutdown()
    
    def listen_loop(self):
        """Enhanced main listening loop for wake words"""
        print("\nListening for wake word...")
        print("Wake words: 'Hey Jarvis', 'Jarvis', 'OK Jarvis', 'Hello Jarvis', 'Java'")
        print("Press Ctrl+C to exit\n")
        
        consecutive_failures = 0
        max_failures = 3
        last_restart = 0
        
        while self.running:
            try:
                # Listen for wake word
                print("🎤 Listening...", end=" ", flush=True)
                audio_text = self.speech_recognizer.listen(timeout=0.5)
                
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
                    current_time = time.time()
                    if current_time - last_restart > 30:  # Only restart every 30 seconds
                        print("🔄 Too many failures. Reinitializing speech recognition...")
                        try:
                            # Reinitialize speech components
                            self.speech_recognizer = SpeechRecognizer()
                            consecutive_failures = 0
                            last_restart = current_time
                            print("✅ Speech recognition reinitialized")
                            self.log_activity('SYSTEM', 'Speech recognition reinitialized')
                        except Exception as restart_error:
                            print(f"❌ Failed to restart: {restart_error}")
                            self.log_activity('ERROR', f'Failed to restart speech recognition: {restart_error}')
                            break
                    else:
                        print("⏳ Waiting before restart...")
                        time.sleep(2)
                else:
                    print("⏳ Retrying in 1 second...")
                    time.sleep(1)
    
    def is_wake_word(self, text):
        """Enhanced wake word detection with fuzzy matching"""
        if not text:
            return False
        
        text = text.strip().lower()
        
        # Direct matching first
        for wake_word in self.wake_words:
            if wake_word in text:
                print(f"✅ Direct wake word match: '{wake_word}'")
                self.logger.info(f"Wake word detected: {wake_word} in '{text}'")
                return True
        
        # Fuzzy matching for speech recognition errors
        try:
            from fuzzywuzzy import fuzz
            
            for wake_word in self.wake_words:
                ratio = fuzz.partial_ratio(wake_word, text)
                if ratio >= 65:  # Lower threshold for better detection
                    print(f"✅ Fuzzy wake word match: '{wake_word}' (confidence: {ratio}%)")
                    self.logger.info(f"Fuzzy wake word detected: {wake_word} in '{text}' (confidence: {ratio}%)")
                    return True
        except ImportError:
            pass  # Fuzzy matching not available
        
        return False
    
    def handle_wake_word(self):
        """Enhanced wake word handling with GUI updates"""
        try:
            self.is_active = True
            
            # Log wake word detection
            self.log_activity('WAKE', 'Wake word detected - JARVIS activated')
            
            # Quick acknowledgment responses
            quick_responses = [
                "Yes?", "I'm listening!", "How can I help?", 
                "Ready!", "What can I do for you?", "I'm here!"
            ]
            
            import random
            acknowledgment = random.choice(quick_responses)
            print(f"JARVIS: {acknowledgment}")
            self.tts.speak(acknowledgment)
            
            # Listen for command
            self.process_command()
            
        except Exception as e:
            error_msg = f"Error handling wake word: {e}"
            print(f"❌ {error_msg}")
            self.logger.error(error_msg)
            self.log_activity('ERROR', error_msg)
        finally:
            self.is_active = False
    
    def process_command(self):
        """Enhanced command processing with GUI updates"""
        try:
            print("🎤 Listening for command...")
            self.log_activity('LISTENING', 'Listening for command...')
            
            # Listen for command with optimized timeout
            command = self.speech_recognizer.listen(timeout=8, phrase_timeout=3)
            
            if command:
                print(f"Command received: '{command}'")
                self.logger.info(f"Command received: {command}")
                self.log_activity('COMMAND', f'Command received: {command}')
                
                # Add to conversation memory
                self.memory.add_user_message(command)
                
                # Process the command
                print("🧠 Processing command...")
                self.log_activity('PROCESSING', 'Processing command...')
                
                response = self.nlp_processor.process_command(command, self.memory)
                
                if response:
                    print(f"JARVIS: {response}")
                    self.tts.speak(response)
                    self.memory.add_assistant_message(response)
                    self.logger.info(f"Response: {response}")
                    self.log_activity('RESPONSE', f'JARVIS: {response}')
                else:
                    fallback = "I'm sorry, I couldn't process that command."
                    print(f"JARVIS: {fallback}")
                    self.tts.speak(fallback)
                    self.log_activity('RESPONSE', fallback)
                    
            else:
                timeout_msg = "I didn't hear a command. Please try again."
                print(f"JARVIS: {timeout_msg}")
                self.tts.speak(timeout_msg)
                self.log_activity('TIMEOUT', 'No command heard - timeout')
                
        except Exception as e:
            error_msg = f"Error processing command: {e}"
            print(f"❌ {error_msg}")
            self.logger.error(error_msg)
            self.log_activity('ERROR', error_msg)
            
            # Inform user of error
            error_response = "Sorry, I encountered an error processing your command."
            self.tts.speak(error_response)
        
        finally:
            print("\nReturning to wake word detection...\n")
            self.log_activity('READY', 'Ready for next wake word')
    
    def process_text_command(self, text):
        """Process text command from GUI"""
        try:
            self.log_activity('TEXT_COMMAND', f'Text command: {text}')
            
            # Add to memory
            self.memory.add_user_message(text)
            
            # Process command
            response = self.nlp_processor.process_command(text, self.memory)
            
            if response:
                self.log_activity('TEXT_RESPONSE', f'Response: {response}')
                self.memory.add_assistant_message(response)
                return response
            else:
                return "I'm not sure how to help with that."
                
        except Exception as e:
            error_msg = f"Error processing text command: {str(e)}"
            self.log_activity('ERROR', error_msg)
            return error_msg
    
    def get_system_status(self):
        """Get system status for GUI"""
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            uptime = datetime.now() - self.start_time
            uptime_str = str(uptime).split('.')[0]  # Remove microseconds
            
            status = {
                'cpu': f"{cpu:.1f}%",
                'memory': f"{memory.percent:.1f}%",
                'uptime': uptime_str,
                'status': 'ACTIVE' if self.running else 'OFFLINE',
                'listening': self.is_active
            }
            
            return status
        except Exception as e:
            self.log_activity('ERROR', f'Failed to get system status: {e}')
            return {
                'cpu': 'N/A',
                'memory': 'N/A',
                'uptime': 'N/A',
                'status': 'ERROR'
            }
    
    def shutdown(self):
        """Shutdown the assistant gracefully"""
        print("\n🔴 Shutting down JARVIS...")
        
        self.running = False
        self.is_active = False
        
        try:
            goodbye = "Goodbye! JARVIS is going offline."
            print(f"JARVIS: {goodbye}")
            self.tts.speak(goodbye)
            
            self.logger.info("JARVIS shutdown completed")
            self.log_activity('SYSTEM', 'JARVIS shutdown completed')
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

def install_gui_dependencies():
    """Install GUI dependencies if needed"""
    gui_packages = ['flask', 'flask-socketio', 'pywebview']
    
    print("📦 Checking GUI dependencies...")
    missing_gui = []
    
    for package in gui_packages:
        try:
            if package == 'flask-socketio':
                import flask_socketio
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_gui.append(package)
            print(f"❌ {package}")
    
    if missing_gui:
        print(f"\n📥 Installing GUI packages: {', '.join(missing_gui)}")
        import subprocess
        try:
            for package in missing_gui:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print("✅ GUI dependencies installed!")
            return True
        except Exception as e:
            print(f"❌ Failed to install GUI dependencies: {e}")
            return False
    
    return True

def main():
    """Enhanced main entry point with GUI support"""
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
        # Create JARVIS
        jarvis = JarvisAssistant()
        
        # Check if GUI is available and ask user
        if GUI_AVAILABLE:
            print("\n🎯 Choose startup mode:")
            print("1. GUI Mode (Beautiful interface with controls)")
            print("2. Console Mode (Text-only interface)")
            
            while True:
                try:
                    choice = input("Enter choice (1/2) [default: 1]: ").strip()
                    
                    if choice == '' or choice == '1':
                        print("🖥️ Starting JARVIS with GUI...")
                        jarvis.start_with_gui()
                        break
                    elif choice == '2':
                        print("🔧 Starting in console mode...")
                        jarvis.start()
                        break
                    else:
                        print("❌ Please enter 1 or 2")
                        continue
                        
                except KeyboardInterrupt:
                    print("\nExiting...")
                    return
        else:
            # Check if user wants to install GUI
            print("\n⚠️ GUI components not found.")
            install_choice = input("Would you like to install GUI components? (y/n) [default: n]: ").strip().lower()
            
            if install_choice in ['y', 'yes']:
                if install_gui_dependencies():
                    print("✅ GUI installed! Please restart JARVIS to use GUI mode.")
                    return
                else:
                    print("❌ GUI installation failed. Starting in console mode...")
            
            # Start in console mode
            print("🔧 Starting in console mode...")
            jarvis.start()
        
    except KeyboardInterrupt:
        print("\nExiting JARVIS...")
    except Exception as e:
        print(f"Failed to start JARVIS: {e}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()