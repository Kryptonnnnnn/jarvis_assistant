import random
import webbrowser
from utils.logger import get_logger

class Entertainment:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        
    def tell_joke(self):
        """Tell a random joke"""
        try:
            joke = random.choice(self.jokes)
            return joke
        except Exception as e:
            self.logger.error(f"Error telling joke: {e}")
            return "Sorry, I can't think of any good jokes right now!"
    
    def play_music(self, song_name=None):
        """Play music (opens in browser)"""
        try:
            if song_name:
                search_query = f"play {song_name}"
                music_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            else:
                music_url = "https://www.youtube.com"
            
            webbrowser.open(music_url)
            return f"Opening music in your browser."
            
        except Exception as e:
            self.logger.error(f"Error playing music: {e}")
            return "Sorry, I couldn't open music for you."
    
    def get_quote(self):
        """Get an inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle"
        ]
        try:
            quote = random.choice(quotes)
            return quote
        except Exception as e:
            self.logger.error(f"Error getting quote: {e}")
            return "Believe in yourself and great things will happen!"

# config/api_keys.py (Create this file)
# Add your API keys here (optional)
OPENAI_API_KEY = "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"  # Add your OpenAI API key if you have one
WEATHER_API_KEY = ""  # Add your weather API key if you have one

# Keep this file private and don't commit to version control!

# data/commands.json (This will be created automatically by the app)
# The NLPProcessor will create this file with default commands

# data/responses.json (Optional - for custom responses)
{
    "greetings": [
        "Hello! How can I assist you today?",
        "Hi there! What can I do for you?",
        "Good to see you! How may I help?"
    ],
    "farewells": [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Until next time!"
    ],
    "errors": [
        "I'm sorry, I didn't understand that.",
        "Could you please repeat that?",
        "I'm having trouble processing that request."
    ]
}