import json
import os
from config.config import Config
from utils.logger import get_logger

class ConversationMemory:
    def __init__(self, max_history=10):
        self.conversation_history = []
        self.max_history = max_history
        self.logger = get_logger(__name__)
        self.memory_file = Config.DATA_DIR / "conversation_log.txt"
        
    def add_user_message(self, message):
        """Add user message to conversation history"""
        self.conversation_history.append({"role": "user", "content": message})
        self._trim_history()
        self._save_to_file(f"USER: {message}")
    
    def add_assistant_message(self, message):
        """Add assistant message to conversation history"""
        self.conversation_history.append({"role": "assistant", "content": message})
        self._trim_history()
        self._save_to_file(f"ASSISTANT: {message}")
    
    def _trim_history(self):
        """Keep only recent conversation history"""
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def _save_to_file(self, message):
        """Save conversation to file"""
        try:
            with open(self.memory_file, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")
        except Exception as e:
            self.logger.error(f"Error saving conversation: {e}")
    
    def get_context(self):
        """Get conversation context"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []