# utils/helpers.py
import re
import string

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove punctuation from the end
    text = text.strip(string.punctuation)
    
    return text.lower()

def extract_parameters(command, pattern):
    """Extract parameters from command using pattern"""
    pattern_regex = pattern.replace("*", "(.+?)")
    match = re.search(pattern_regex, command, re.IGNORECASE)
    if match:
        return [group.strip() for group in match.groups()]
    return []