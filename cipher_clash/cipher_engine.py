"""
Cipher Engine for Cipher Clash game.
Handles cipher generation and checking.
"""
import random
import string
from config import (
    CAESAR_CIPHER, SUBSTITUTION_CIPHER, JUMBLE_CIPHER, MORSE_CIPHER, BINARY_CIPHER,
    DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD,
    MIN_WORD_LENGTH, MAX_WORD_LENGTH
)
from utils.helpers import load_word_bank, load_sample_ciphers

class CipherEngine:
    def __init__(self):
        """Initialize the cipher engine."""
        self.word_bank = load_word_bank()
        self.sample_ciphers = load_sample_ciphers()
        self.current_word = ""
        self.current_cipher = ""
        self.current_type = ""
        self.current_difficulty = DIFFICULTY_EASY
        self.hint_revealed = False
        self.substitution_map = {}  # Store the current substitution map
        
        # Morse code mapping
        self.morse_code = {
            'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 
            'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 
            'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 
            'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 
            'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 
            'z': '--..', '0': '-----', '1': '.----', '2': '..---', 
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', 
            '7': '--...', '8': '---..', '9': '----.'
        }
    
    def select_word(self, difficulty):
        """Select a word from the word bank based on difficulty."""
        filtered_words = []
        
        if difficulty == DIFFICULTY_EASY:
            # Easy: shorter words (3-5 letters)
            filtered_words = [word for word in self.word_bank if 3 <= len(word) <= 5]
        elif difficulty == DIFFICULTY_MEDIUM:
            # Medium: medium length words (6-8 letters)
            filtered_words = [word for word in self.word_bank if 6 <= len(word) <= 8]
        else:  # DIFFICULTY_HARD
            # Hard: longer words (9+ letters)
            filtered_words = [word for word in self.word_bank if len(word) >= 9]
        
        # If no words match the criteria, use the full word bank
        if not filtered_words:
            filtered_words = self.word_bank
        
        # Make sure we have a valid word
        if not filtered_words:
            filtered_words = ["python", "code", "cipher", "puzzle"]
        
        self.current_word = random.choice(filtered_words).lower()  # Ensure lowercase
        return self.current_word
    
    def create_caesar_cipher(self, word, difficulty):
        """Create a Caesar cipher by shifting letters."""
        if difficulty == DIFFICULTY_EASY:
            shift = 1  # Simple shift by 1
        elif difficulty == DIFFICULTY_MEDIUM:
            shift = 3  # Medium shift by 3
        else:  # DIFFICULTY_HARD
            shift = random.randint(5, 15)  # Harder random shift
        
        cipher_text = ""
        for char in word:
            if char.isalpha():
                # Apply the shift (always work with lowercase)
                shifted = chr(((ord(char.lower()) - ord('a') + shift) % 26) + ord('a'))
                cipher_text += shifted
            else:
                cipher_text += char
        
        return cipher_text, f"Caesar Shift: {shift}"
    
    def create_substitution_cipher(self, word, difficulty):
        """Create a substitution cipher by replacing letters with others."""
        # Create a substitution key
        alphabet = list(string.ascii_lowercase)
        substitution = list(string.ascii_lowercase)
        random.shuffle(substitution)
        
        # Create a mapping dictionary
        self.substitution_map = {alphabet[i]: substitution[i] for i in range(26)}
        
        # Apply the substitution
        cipher_text = ""
        for char in word.lower():
            if char in self.substitution_map:
                cipher_text += self.substitution_map[char]
            else:
                cipher_text += char
        
        # Create a hint based on difficulty
        if difficulty == DIFFICULTY_EASY:
            # Show 3 letter mappings as hint
            unique_letters = list(set(word.lower()))
            hint_letters = random.sample(unique_letters, min(3, len(unique_letters)))
            hint = "Substitution Key: "
            for letter in hint_letters:
                if letter in self.substitution_map:
                    hint += f"{letter}→{self.substitution_map[letter]}, "
            hint = hint.rstrip(", ")
        elif difficulty == DIFFICULTY_MEDIUM:
            # Show 1-2 letter mappings
            unique_letters = list(set(word.lower()))
            hint_letters = random.sample(unique_letters, min(2, len(unique_letters)))
            hint = "Substitution Key: "
            for letter in hint_letters:
                if letter in self.substitution_map:
                    hint += f"{letter}→{self.substitution_map[letter]}, "
            hint = hint.rstrip(", ")
        else:  # DIFFICULTY_HARD
            # No specific letter hints
            hint = "Substitution Cipher"
        
        return cipher_text, hint
    
    def create_jumble_cipher(self, word, difficulty):
        """Create a jumbled word cipher by rearranging letters."""
        # Convert word to list of characters
        chars = list(word.lower())
        original_chars = chars.copy()  # Keep a copy of the original
        
        # Jumble the letters based on difficulty
        if difficulty == DIFFICULTY_EASY:
            # Swap only a few adjacent pairs
            swaps = min(2, len(word) // 2)
            for _ in range(swaps):
                idx = random.randint(0, len(chars) - 2)
                chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
            
            # Make sure we actually jumbled something
            if ''.join(chars) == word.lower():
                if len(chars) >= 2:
                    chars[0], chars[1] = chars[1], chars[0]
        elif difficulty == DIFFICULTY_MEDIUM:
            # Medium jumbling
            while ''.join(chars) == word.lower():  # Ensure it's actually jumbled
                random.shuffle(chars)
                # If we can't jumble it after a few tries (e.g., "aa"), just add a letter
                if ''.join(chars) == word.lower() and len(word) < MAX_WORD_LENGTH:
                    extra_letter = random.choice(string.ascii_lowercase)
                    chars.append(extra_letter)
        else:  # DIFFICULTY_HARD
            # Hard jumbling + add a red herring letter
            random.shuffle(chars)
            if len(word) < MAX_WORD_LENGTH:
                # Add a random letter
                extra_letter = random.choice(string.ascii_lowercase)
                insert_pos = random.randint(0, len(chars))
                chars.insert(insert_pos, extra_letter)
        
        jumbled = ''.join(chars)
        
        # Create hint
        if difficulty == DIFFICULTY_EASY:
            hint = f"Jumbled Word: First letter is {word[0]}"
        elif difficulty == DIFFICULTY_MEDIUM:
            hint = "Jumbled Word: All letters rearranged"
        else:
            hint = "Jumbled Word: May contain an extra letter"
        
        # Store the original word for checking
        self.current_word = word.lower()
        
        return jumbled, hint
    
    def create_morse_cipher(self, word, difficulty):
        """Create a Morse code cipher."""
        morse_text = []
        
        for char in word.lower():
            if char in self.morse_code:
                morse_text.append(self.morse_code[char])
            else:
                # Skip characters not in Morse code
                continue
        
        # Join with different separators based on difficulty
        if difficulty == DIFFICULTY_EASY:
            # Easy: clear letter separation
            cipher_text = ' '.join(morse_text)
            hint = "Morse Code: Letters separated by spaces"
        elif difficulty == DIFFICULTY_MEDIUM:
            # Medium: letters separated by /
            cipher_text = '/'.join(morse_text)
            hint = "Morse Code: Letters separated by /"
        else:  # DIFFICULTY_HARD
            # Hard: minimal separation
            cipher_text = ''.join(morse_text)
            hint = "Morse Code: No letter separation"
        
        return cipher_text, hint
    
    def create_binary_cipher(self, word, difficulty):
        """Create a binary code cipher."""
        binary_text = []
        
        for char in word.lower():
            # Convert character to ASCII and then to binary
            binary = bin(ord(char))[2:].zfill(8)  # Remove '0b' prefix and pad to 8 bits
            binary_text.append(binary)
        
        # Join with different formatting based on difficulty
        if difficulty == DIFFICULTY_EASY:
            # Easy: clear separation and hint
            cipher_text = ' '.join(binary_text)
            hint = "Binary Code: Each letter is 8 bits"
        elif difficulty == DIFFICULTY_MEDIUM:
            # Medium: less separation
            cipher_text = ''.join(binary_text)
            hint = "Binary Code: 8 bits per letter, no spaces"
        else:  # DIFFICULTY_HARD
            # Hard: hexadecimal representation
            hex_text = []
            for char in word.lower():
                hex_char = hex(ord(char))[2:].zfill(2)  # Remove '0x' prefix
                hex_text.append(hex_char)
            cipher_text = ''.join(hex_text)
            hint = "Hexadecimal Code"
        
        return cipher_text, hint
    
    def generate_cipher(self, difficulty=None, cipher_type=None):
        """Generate a new cipher of the specified type and difficulty."""
        if difficulty is None:
            difficulty = self.current_difficulty
        else:
            self.current_difficulty = difficulty
        
        # Select a word
        word = self.select_word(difficulty)
        
        # Determine cipher type if not specified
        if cipher_type is None:
            if difficulty == DIFFICULTY_EASY:
                cipher_types = [CAESAR_CIPHER, JUMBLE_CIPHER]
            elif difficulty == DIFFICULTY_MEDIUM:
                cipher_types = [CAESAR_CIPHER, SUBSTITUTION_CIPHER, JUMBLE_CIPHER, MORSE_CIPHER]
            else:  # DIFFICULTY_HARD
                cipher_types = [SUBSTITUTION_CIPHER, JUMBLE_CIPHER, MORSE_CIPHER, BINARY_CIPHER]
            
            cipher_type = random.choice(cipher_types)
        
        self.current_type = cipher_type
        self.hint_revealed = False
        
        # Generate the cipher based on type
        try:
            if cipher_type == CAESAR_CIPHER:
                cipher_text, hint = self.create_caesar_cipher(word, difficulty)
            elif cipher_type == SUBSTITUTION_CIPHER:
                cipher_text, hint = self.create_substitution_cipher(word, difficulty)
            elif cipher_type == JUMBLE_CIPHER:
                cipher_text, hint = self.create_jumble_cipher(word, difficulty)
            elif cipher_type == MORSE_CIPHER:
                cipher_text, hint = self.create_morse_cipher(word, difficulty)
            elif cipher_type == BINARY_CIPHER:
                cipher_text, hint = self.create_binary_cipher(word, difficulty)
            else:
                # Default to jumble if type not recognized
                cipher_text, hint = self.create_jumble_cipher(word, difficulty)
                cipher_type = JUMBLE_CIPHER
        except Exception as e:
            print(f"Error generating cipher: {e}")
            # Fallback to a simple cipher
            word = "cipher"
            self.current_word = word
            cipher_text = "djqifs"  # Simple Caesar shift
            hint = "Caesar Shift: 1"
            cipher_type = CAESAR_CIPHER
        
        self.current_cipher = {
            "word": word.lower(),  # Ensure lowercase for consistency
            "cipher_text": cipher_text,
            "type": cipher_type,
            "difficulty": difficulty,
            "hint": hint
        }
        
        return self.current_cipher
    
    def check_answer(self, answer):
        """Check if the provided answer matches the current word."""
        if not self.current_word:
            return False
        
        # Normalize both strings: lowercase and strip whitespace
        user_answer = answer.lower().strip()
        correct_answer = self.current_word.lower().strip()
        
        # Check for exact match
        return user_answer == correct_answer
    
    def get_hint(self):
        """Get a hint for the current cipher."""
        if not self.current_cipher:
            return ""
        
        self.hint_revealed = True
        
        # For jumble cipher in hard mode, give a more helpful hint
        if self.current_cipher["type"] == JUMBLE_CIPHER and self.current_difficulty == DIFFICULTY_HARD:
            return f"Jumbled Word: First letter is {self.current_word[0]}"
        
        return self.current_cipher["hint"]
    
    def get_first_letter(self):
        """Get the first letter of the current word as an additional hint."""
        if not self.current_word:
            return ""
        
        return self.current_word[0]
