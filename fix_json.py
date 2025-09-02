import json
import os

# Create the data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Default commands configuration
commands = {
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
    "time": {
        "patterns": ["what time", "current time", "time now"],
        "action": "get_time"
    },
    "joke": {
        "patterns": ["tell me a joke", "joke", "funny"],
        "action": "tell_joke"
    },
    "search": {
        "patterns": ["search for *", "google *", "look up *"],
        "action": "web_search"
    },
    "weather": {
        "patterns": ["weather", "temperature", "forecast"],
        "action": "get_weather"
    }
}

# Write the commands to the JSON file
try:
    with open("data/commands.json", "w", encoding="utf-8") as f:
        json.dump(commands, f, indent=2)
    
    print("✅ Created data/commands.json successfully!")
    print("✅ JARVIS should now work properly!")
    print("\nRun: python main.py")
    
except Exception as e:
    print(f"❌ Error creating commands.json: {e}")