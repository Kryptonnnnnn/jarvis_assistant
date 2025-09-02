def test_wake_word_detection():
    test_phrases = [
        "hello with jokes",  # Your problematic phrase
        "hello jarvis",
        "hey jarvis", 
        "jar vis",
        "jokes",
        "job is"
    ]
    
    wake_words = ["jarvis", "hey jarvis", "ok jarvis", "hello jarvis"]
    
    from difflib import SequenceMatcher
    
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def is_wake_word(text):
        text = text.lower().strip()
        
        # Direct match
        for wake_word in wake_words:
            if wake_word in text:
                return True, f"Direct match: {wake_word}"
        
        # Fuzzy match for "jarvis"
        words = text.split()
        for word in words:
            if similarity(word, "jarvis") > 0.6:
                return True, f"Fuzzy match: {word} ≈ jarvis ({similarity(word, 'jarvis'):.2f})"
        
        return False, "No match"
    
    print("Testing wake word detection:")
    for phrase in test_phrases:
        result, reason = is_wake_word(phrase)
        status = "✅ DETECTED" if result else "❌ MISSED"
        print(f"{status}: '{phrase}' - {reason}")

if __name__ == "__main__":
    test_wake_word_detection()