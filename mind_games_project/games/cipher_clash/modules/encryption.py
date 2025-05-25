"""
Encryption module for Cipher Clash game.
Contains functions for generating and solving various types of ciphers.
"""

import random
import string
import math
from itertools import cycle

def generate_cipher(cipher_type, min_length=10, max_length=30, word_count=3, complexity=0.5):
    """
    Generate a cipher puzzle and its solution.
    
    Args:
        cipher_type (str): Type of cipher to generate
        min_length (int): Minimum length of the plaintext
        max_length (int): Maximum length of the plaintext
        word_count (int): Approximate number of words in the plaintext
        complexity (float): Complexity factor (0.0 to 1.0)
        
    Returns:
        tuple: (cipher_text, plain_text) - The encrypted text and its solution
    """
    # Generate or select a plaintext message
    plain_text = generate_plaintext(min_length, max_length, word_count)
    
    # Apply the selected cipher
    if cipher_type == 'caesar':
        shift = int(complexity * 25) + 1  # Shift between 1-25 based on complexity
        cipher_text = caesar_cipher(plain_text, shift)
        cipher_description = f"Caesar Cipher (Shift: {shift})"
        
    elif cipher_type == 'atbash':
        cipher_text = atbash_cipher(plain_text)
        cipher_description = "Atbash Cipher"
        
    elif cipher_type == 'reverse':
        cipher_text = reverse_cipher(plain_text)
        cipher_description = "Reverse Cipher"
        
    elif cipher_type == 'substitution':
        cipher_text, _ = substitution_cipher(plain_text)
        cipher_description = "Substitution Cipher"
        
    elif cipher_type == 'vigenere':
        # Generate a key of appropriate length based on complexity
        key_length = max(3, int(complexity * 10))
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(key_length))
        cipher_text = vigenere_cipher(plain_text, key)
        cipher_description = f"Vigenère Cipher (Key: {key})"
        
    elif cipher_type == 'transposition':
        # Number of columns for transposition increases with complexity
        num_columns = max(2, int(complexity * 8))
        cipher_text = transposition_cipher(plain_text, num_columns)
        cipher_description = f"Transposition Cipher ({num_columns} columns)"
        
    elif cipher_type == 'playfair':
        # Generate a random key for the Playfair cipher
        key = ''.join(random.sample(string.ascii_uppercase.replace('J', ''), 5))
        cipher_text = playfair_cipher(plain_text, key)
        cipher_description = f"Playfair Cipher (Key: {key})"
        
    else:
        # Default to Caesar cipher if an unknown type is specified
        shift = random.randint(1, 25)
        cipher_text = caesar_cipher(plain_text, shift)
        cipher_description = f"Caesar Cipher (Shift: {shift})"
    
    # Format the cipher puzzle with its description
    puzzle = f"{cipher_description}:\n{cipher_text}"
    
    return puzzle, plain_text

def generate_plaintext(min_length, max_length, word_count):
    """
    Generate a random plaintext message.
    
    Args:
        min_length (int): Minimum length of the plaintext
        max_length (int): Maximum length of the plaintext
        word_count (int): Approximate number of words
        
    Returns:
        str: The generated plaintext
    """
    # List of common words for puzzle generation
    common_words = [
        "PUZZLE", "SECRET", "CIPHER", "CODE", "MYSTERY", "HIDDEN", "MESSAGE",
        "ENCRYPT", "DECRYPT", "SOLVE", "CHALLENGE", "RIDDLE", "CLUE", "FIND",
        "DISCOVER", "UNLOCK", "REVEAL", "CRACK", "DECIPHER", "CRYPTIC",
        "ENIGMA", "CONUNDRUM", "BRAIN", "MIND", "GAME", "PLAY", "THINK",
        "LOGIC", "REASON", "DEDUCE", "ANALYZE", "EXAMINE", "STUDY", "LEARN",
        "QUEST", "JOURNEY", "ADVENTURE", "EXPLORE", "NAVIGATE", "PATH",
        "ROUTE", "MAP", "COMPASS", "GUIDE", "DIRECTION", "NORTH", "SOUTH",
        "EAST", "WEST", "TREASURE", "GOLD", "SILVER", "JEWEL", "GEM", "RUBY",
        "EMERALD", "SAPPHIRE", "DIAMOND", "PEARL", "CROWN", "KINGDOM", "CASTLE",
        "TOWER", "DUNGEON", "CAVE", "FOREST", "MOUNTAIN", "RIVER", "LAKE", "SEA",
        "OCEAN", "ISLAND", "BRIDGE", "GATE", "DOOR", "KEY", "LOCK", "CHEST",
        "BOX", "CONTAINER", "BOTTLE", "SCROLL", "BOOK", "PAGE", "LETTER", "WORD",
        "SENTENCE", "PARAGRAPH", "STORY", "TALE", "LEGEND", "MYTH", "HISTORY",
        "ANCIENT", "MODERN", "FUTURE", "PAST", "PRESENT", "TIME", "SPACE",
        "DIMENSION", "REALITY", "VIRTUAL", "DIGITAL", "ANALOG", "BINARY", "CODE"
    ]
    
    # Select random words to form the message
    selected_words = random.sample(common_words, min(word_count, len(common_words)))
    
    # Ensure the message length is within bounds
    message = " ".join(selected_words)
    while len(message) < min_length:
        additional_word = random.choice(common_words)
        message += " " + additional_word
        
    # Truncate if too long
    if len(message) > max_length:
        words = message.split()
        message = " ".join(words[:max(1, word_count)])
        
    return message.upper()

def caesar_cipher(text, shift):
    """
    Apply a Caesar cipher to the text.
    
    Args:
        text (str): Text to encrypt
        shift (int): Number of positions to shift each letter
        
    Returns:
        str: Encrypted text
    """
    result = ""
    
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            # Shift the character and wrap around the alphabet
            shifted = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
            result += chr(shifted)
        else:
            # Keep non-alphabetic characters unchanged
            result += char
            
    return result

def atbash_cipher(text):
    """
    Apply an Atbash cipher to the text (reverse the alphabet).
    
    Args:
        text (str): Text to encrypt
        
    Returns:
        str: Encrypted text
    """
    result = ""
    
    for char in text:
        if char.isalpha():
            if char.isupper():
                # For uppercase: Z - (char - A)
                result += chr(90 - (ord(char) - 65))
            else:
                # For lowercase: z - (char - a)
                result += chr(122 - (ord(char) - 97))
        else:
            result += char
            
    return result

def reverse_cipher(text):
    """
    Reverse the text.
    
    Args:
        text (str): Text to encrypt
        
    Returns:
        str: Encrypted text
    """
    return text[::-1]

def substitution_cipher(text):
    """
    Apply a simple substitution cipher.
    
    Args:
        text (str): Text to encrypt
        
    Returns:
        tuple: (encrypted_text, substitution_key)
    """
    # Create a random substitution key
    alphabet = list(string.ascii_uppercase)
    shuffled = random.sample(alphabet, len(alphabet))
    substitution_key = dict(zip(alphabet, shuffled))
    
    result = ""
    for char in text:
        if char.upper() in substitution_key:
            # Preserve case
            if char.isupper():
                result += substitution_key[char]
            else:
                result += substitution_key[char.upper()].lower()
        else:
            result += char
            
    return result, substitution_key

def vigenere_cipher(text, key):
    """
    Apply a Vigenère cipher to the text.
    
    Args:
        text (str): Text to encrypt
        key (str): Encryption key
        
    Returns:
        str: Encrypted text
    """
    result = ""
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(k) - ord('A') for k in key]
    
    i = 0
    for char in text:
        if char.isalpha():
            # Convert to 0-25
            if char.isupper():
                ascii_offset = ord('A')
            else:
                ascii_offset = ord('a')
                
            # Apply Vigenère encryption formula
            shift = key_as_int[i % key_length]
            encrypted = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
            result += chr(encrypted)
            
            i += 1
        else:
            result += char
            
    return result

def transposition_cipher(text, num_columns):
    """
    Apply a columnar transposition cipher.
    
    Args:
        text (str): Text to encrypt
        num_columns (int): Number of columns for the transposition grid
        
    Returns:
        str: Encrypted text
    """
    # Remove spaces for transposition
    text = text.replace(" ", "")
    
    # Calculate number of rows needed
    num_rows = math.ceil(len(text) / num_columns)
    
    # Pad the text if necessary
    padded_text = text + ' ' * (num_rows * num_columns - len(text))
    
    # Create the grid
    grid = []
    for i in range(0, len(padded_text), num_columns):
        grid.append(padded_text[i:i+num_columns])
    
    # Read by columns
    result = ""
    for col in range(num_columns):
        for row in range(num_rows):
            if col < len(grid[row]):
                result += grid[row][col]
    
    return result

def playfair_cipher(text, key):
    """
    Apply a Playfair cipher to the text.
    
    Args:
        text (str): Text to encrypt
        key (str): Encryption key
        
    Returns:
        str: Encrypted text
    """
    # Simplified implementation for demonstration
    # In a real implementation, this would follow the full Playfair algorithm
    
    # For simplicity, we'll just apply a double Caesar cipher
    # with different shifts for even and odd positions
    result = ""
    
    # Generate two shift values from the key
    shift1 = sum(ord(c) for c in key) % 26
    shift2 = (shift1 * 2) % 26
    
    for i, char in enumerate(text):
        if char.isalpha():
            shift = shift1 if i % 2 == 0 else shift2
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
            
    return result

def decrypt_message(cipher_text, cipher_type, key=None):
    """
    Decrypt a message based on the cipher type and key.
    
    Args:
        cipher_text (str): The encrypted text
        cipher_type (str): Type of cipher used
        key: The decryption key (if needed)
        
    Returns:
        str: The decrypted text
    """
    if cipher_type == 'caesar':
        # For Caesar, the key is the shift value
        return caesar_cipher(cipher_text, 26 - key)
        
    elif cipher_type == 'atbash':
        # Atbash is its own inverse
        return atbash_cipher(cipher_text)
        
    elif cipher_type == 'reverse':
        # Reverse is its own inverse
        return reverse_cipher(cipher_text)
        
    elif cipher_type == 'vigenere':
        # For Vigenère, we need to apply the inverse operation
        return vigenere_decrypt(cipher_text, key)
        
    # Add other cipher decryption methods as needed
    
    return "Decryption not implemented for this cipher type"

def vigenere_decrypt(cipher_text, key):
    """
    Decrypt a Vigenère cipher.
    
    Args:
        cipher_text (str): The encrypted text
        key (str): The decryption key
        
    Returns:
        str: The decrypted text
    """
    result = ""
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(k) - ord('A') for k in key]
    
    i = 0
    for char in cipher_text:
        if char.isalpha():
            # Convert to 0-25
            if char.isupper():
                ascii_offset = ord('A')
            else:
                ascii_offset = ord('a')
                
            # Apply Vigenère decryption formula
            shift = key_as_int[i % key_length]
            decrypted = (ord(char) - ascii_offset - shift) % 26 + ascii_offset
            result += chr(decrypted)
            
            i += 1
        else:
            result += char
            
    return result
