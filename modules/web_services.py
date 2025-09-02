import requests
import webbrowser
from datetime import datetime
from utils.logger import get_logger

class WebServices:
    def __init__(self):
        self.logger = get_logger(__name__)
        
    def get_weather(self, location="London"):
        """Get weather information"""
        try:
            return f"I'm unable to get weather data right now. Please check your internet connection or set up a weather API key."
        except Exception as e:
            self.logger.error(f"Error getting weather: {e}")
            return "Sorry, I couldn't retrieve weather information."
    
    def search_web(self, query):
        """Perform web search"""
        try:
            if not query:
                return "What would you like me to search for?"
            
            # Open web search in browser
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"I've opened a web search for '{query}' in your browser."
            
        except Exception as e:
            self.logger.error(f"Error performing web search: {e}")
            return "Sorry, I couldn't perform the web search."