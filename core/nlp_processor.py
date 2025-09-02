import json
import re
from pathlib import Path
from fuzzywuzzy import fuzz
from modules.system_control import SystemController
from modules.web_services import WebServices
from modules.file_manager import FileManager
from modules.entertainment import Entertainment
from utils.logger import get_logger

class NLPProcessor:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.system_controller = SystemController()
        self.web_services = WebServices()
        self.file_manager = FileManager()
        self.entertainment = Entertainment()
        
        # Load command patterns
        self.load_commands()
        
    def load_commands(self):
        """Load command patterns from JSON file"""
        commands_file = Path("data/commands.json")
        try:
            with open(commands_file, 'r') as f:
                self.commands = json.load(f)
        except FileNotFoundError:
            self.commands = self.create_default_commands()
            self.save_commands()
            
    def create_default_commands(self):
        """Create default command patterns"""
        return {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "good morning", "good evening"],
                "responses": ["Hello! How can I assist you?", "Hi there! What can I do for you?"]
            },
            "system_info": {
                "patterns": ["system info", "computer info", "pc status", "system status"],
                "action": "get_system_info"
            },
            "open_application": {
                "patterns": ["open *", "launch *", "start *"],
                "action": "open_application"
            },
            "weather": {
                "patterns": ["weather", "temperature", "forecast"],
                "action": "get_weather"
            },
            "search": {
                "patterns": ["search for *", "google *", "look up *"],
                "action": "web_search"
            },
            "time": {
                "patterns": ["what time", "current time", "time now"],
                "action": "get_time"
            },
            "joke": {
                "patterns": ["tell me a joke", "joke", "funny"],
                "action": "tell_joke"
            },
            "shutdown": {
                "patterns": ["shutdown", "turn off", "power off"],
                "action": "shutdown_system"
            }
        }
        
    def save_commands(self):
        """Save commands to JSON file"""
        commands_file = Path("data/commands.json")
        with open(commands_file, 'w') as f:
            json.dump(self.commands, f, indent=2)
            
    def process_command(self, command, memory=None):
        """Process natural language command"""
        command = command.lower().strip()
        best_match = self.find_best_match(command)
        
        if best_match:
            return self.execute_command(best_match, command, memory)
        else:
            return self.handle_unknown_command(command, memory)
            
    def find_best_match(self, command):
        """Find best matching command pattern"""
        best_score = 0
        best_match = None
        
        for cmd_type, cmd_data in self.commands.items():
            for pattern in cmd_data["patterns"]:
                if "*" in pattern:
                    # Handle wildcard patterns
                    pattern_regex = pattern.replace("*", "(.+)")
                    if re.search(pattern_regex, command):
                        score = 90  # High score for wildcard matches
                    else:
                        score = 0
                else:
                    # Use fuzzy matching for exact patterns
                    score = fuzz.partial_ratio(pattern, command)
                
                if score > best_score and score > 70:  # Threshold for matching
                    best_score = score
                    best_match = (cmd_type, cmd_data, pattern)
                    
        return best_match
        
    def execute_command(self, match, original_command, memory):
        """Execute the matched command"""
        cmd_type, cmd_data, pattern = match
        
        try:
            if "action" in cmd_data:
                action = cmd_data["action"]
                return self.call_action(action, original_command, pattern)
            elif "responses" in cmd_data:
                import random
                return random.choice(cmd_data["responses"])
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return "Sorry, I encountered an error processing that command."
            
    def call_action(self, action, command, pattern):
        """Call the appropriate action method"""
        # Extract parameters for wildcard patterns
        params = []
        if "*" in pattern:
            pattern_regex = pattern.replace("*", "(.+)")
            match = re.search(pattern_regex, command)
            if match:
                params = [group.strip() for group in match.groups()]
        
        # Map actions to methods
        action_map = {
            "get_system_info": self.system_controller.get_system_info,
            "open_application": lambda: self.system_controller.open_application(params[0] if params else ""),
            "get_weather": self.web_services.get_weather,
            "web_search": lambda: self.web_services.search_web(params[0] if params else ""),
            "get_time": self.system_controller.get_current_time,
            "tell_joke": self.entertainment.tell_joke,
            "shutdown_system": self.system_controller.shutdown_system
        }
        
        if action in action_map:
            return action_map[action]()
        else:
            return f"Action '{action}' not implemented yet."
            
    def handle_unknown_command(self, command, memory):
        """Handle commands that don't match any pattern"""
        responses = [
            "I'm not sure how to help with that. Could you rephrase?",
            "I didn't understand that command. Can you try again?",
            "Sorry, I don't know how to do that yet."
        ]
        import random
        return random.choice(responses)