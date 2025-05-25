"""
Cipher Manager module for Cipher Clash.
Handles encoding and decoding of various cipher types.
"""
import random
import string
import re

class CipherManager:
    """Manages different cipher types and their encoding/decoding."""
    
    def __init__(self):
        """Initialize the cipher manager."""
        # Dictionary of available cipher types and their functions
        self.cipher_types = {
            "caesar": self.caesar_cipher,
            "vigenere": self.vigenere_cipher,
            "morse": self.morse_code,
            "substitution": self.substitution_cipher,
            "transposition": self.transposition_cipher
        }
    
    def get_cipher_function(self, cipher_type):
        """Get the cipher function for the specified type."""
        return self.cipher_types.get(cipher_type)
    
    def encrypt(self, text, cipher_type, **kwargs):
        """
        Encrypt text using the specified cipher type.
        
        Args:
            text (str): The text to encrypt
            cipher_type (str): The type of cipher to use
            **kwargs: Additional parameters for the specific cipher
            
        Returns:
            tuple: (encrypted_text, encryption_key, hint)
        """
        cipher_func = self.get_cipher_function(cipher_type)
        if cipher_func:
            return cipher_func(text, encrypt=True, **kwargs)
        else:
            raise ValueError(f"Unknown cipher type: {cipher_type}")
    
    def decrypt(self, encrypted_text, cipher_type, **kwargs):
        """
        Decrypt text using the specified cipher type.
        
        Args:
            encrypted_text (str): The text to decrypt
            cipher_type (str): The type of cipher to use
            **kwargs: Additional parameters for the specific cipher
            
        Returns:
            str: The decrypted text
        """
        cipher_func = self.get_cipher_function(cipher_type)
        if cipher_func:
            result = cipher_func(encrypted_text, encrypt=False, **kwargs)
            return result[0] if isinstance(result, tuple) else result
        else:
            raise ValueError(f"Unknown cipher type: {cipher_type}")
    
    def caesar_cipher(self, text, encrypt=True, shift=None, **kwargs):
        """
        Apply Caesar cipher to the text.
        
        Args:
            text (str): The text to encrypt/decrypt
            encrypt (bool): True for encryption, False for decryption
            shift (int): The shift value (if None, a random shift is generated)
            
        Returns:
            tuple: (result_text, shift, hint) for encryption
            str: result_text for decryption
        """
        if shift is None:
            shift = random.randint(1, 25)
        
        result = ""
        
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                # Apply shift (for encryption) or reverse shift (for decryption)
                if encrypt:
                    shifted = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
                else:
                    shifted = (ord(char) - ascii_offset - shift) % 26 + ascii_offset
                result += chr(shifted)
            else:
                result += char
        
        if encrypt:
            hint = f"The alphabet is shifted by {shift} positions."
            return result, shift, hint
        else:
            return result
    
    def vigenere_cipher(self, text, encrypt=True, key=None, **kwargs):
        """
        Apply Vigenère cipher to the text.
        
        Args:
            text (str): The text to encrypt/decrypt
            encrypt (bool): True for encryption, False for decryption
            key (str): The keyword (if None, a random key is generated)
            
        Returns:
            tuple: (result_text, key, hint) for encryption
            str: result_text for decryption
        """
        if key is None:
            # Generate a random key of length 3-6
            key_length = random.randint(3, 6)
            key = ''.join(random.choice(string.ascii_lowercase) for _ in range(key_length))
        
        # Convert key to lowercase
        key = key.lower()
        
        result = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                # Get the shift value from the key
                key_char = key[key_index % len(key)]
                key_shift = ord(key_char) - ord('a')
                
                ascii_offset = ord('A') if char.isupper() else ord('a')
                
                # Apply Vigenère cipher
                if encrypt:
                    shifted = (ord(char) - ascii_offset + key_shift) % 26 + ascii_offset
                else:
                    shifted = (ord(char) - ascii_offset - key_shift) % 26 + ascii_offset
                
                result += chr(shifted)
                key_index += 1
            else:
                result += char
        
        if encrypt:
            hint = f"The key is '{key}'. Each letter shifts by the corresponding letter in the key."
            return result, key, hint
        else:
            return result
    
    def morse_code(self, text, encrypt=True, **kwargs):
        """
        Convert text to/from Morse code.
        
        Args:
            text (str): The text to convert
            encrypt (bool): True for text to Morse, False for Morse to text
            
        Returns:
            tuple: (morse_code, None, hint) for encryption
            str: decoded_text for decryption
        """
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', 
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
            '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..', 
            "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', 
            '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', 
            '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
        }
        
        # Create reverse dictionary for decoding
        reverse_morse_dict = {v: k for k, v in morse_dict.items()}
        
        if encrypt:
            result = []
            for char in text.upper():
                if char == ' ':
                    result.append('/')  # Use / to represent word spaces
                elif char in morse_dict:
                    result.append(morse_dict[char])
            
            morse_text = ' '.join(result)
            hint = "Dots (.) and dashes (-) represent Morse code. / separates words."
            return morse_text, None, hint
        else:
            words = text.split('/')
            result = []
            
            for word in words:
                morse_chars = word.strip().split()
                decoded_chars = []
                
                for morse_char in morse_chars:
                    if morse_char in reverse_morse_dict:
                        decoded_chars.append(reverse_morse_dict[morse_char])
                
                result.append(''.join(decoded_chars))
            
            return ' '.join(result)
    
    def substitution_cipher(self, text, encrypt=True, key=None, **kwargs):
        """
        Apply a simple substitution cipher to the text.
        
        Args:
            text (str): The text to encrypt/decrypt
            encrypt (bool): True for encryption, False for decryption
            key (dict): The substitution key (if None, a random key is generated)
            
        Returns:
            tuple: (result_text, key, hint) for encryption
            str: result_text for decryption
        """
        if key is None and encrypt:
            # Generate a random substitution key
            alphabet = list(string.ascii_uppercase)
            shuffled = alphabet.copy()
            random.shuffle(shuffled)
            key = {a: s for a, s in zip(alphabet, shuffled)}
        
        result = ""
        
        if encrypt:
            for char in text:
                if char.upper() in key:
                    # Preserve case
                    if char.isupper():
                        result += key[char]
                    else:
                        result += key[char.upper()].lower()
                else:
                    result += char
            
            # Create a hint showing part of the substitution
            hint_letters = random.sample(string.ascii_uppercase, 5)
            hint = "Substitution key (partial): "
            hint += ", ".join([f"{letter} → {key[letter]}" for letter in hint_letters])
            
            return result, key, hint
        else:
            # For decryption, invert the key
            inv_key = {v: k for k, v in key.items()}
            
            for char in text:
                if char.upper() in inv_key:
                    # Preserve case
                    if char.isupper():
                        result += inv_key[char]
                    else:
                        result += inv_key[char.upper()].lower()
                else:
                    result += char
            
            return result
    
    def transposition_cipher(self, text, encrypt=True, key=None, **kwargs):
        """
        Apply a columnar transposition cipher to the text.
        
        Args:
            text (str): The text to encrypt/decrypt
            encrypt (bool): True for encryption, False for decryption
            key (list): The column order (if None, a random key is generated)
            
        Returns:
            tuple: (result_text, key, hint) for encryption
            str: result_text for decryption
        """
        if key is None:
            # Generate a random key (column order)
            key_length = random.randint(3, 6)
            key = list(range(key_length))
            random.shuffle(key)
        
        if encrypt:
            # Remove spaces for encryption (optional)
            text = text.replace(" ", "")
            
            # Calculate number of rows needed
            num_columns = len(key)
            num_rows = (len(text) + num_columns - 1) // num_columns
            
            # Pad the text if necessary
            padded_text = text + ' ' * (num_columns * num_rows - len(text))
            
            # Create the grid
            grid = []
            for i in range(0, len(padded_text), num_columns):
                grid.append(list(padded_text[i:i+num_columns]))
            
            # Read out the columns according to the key
            result = ""
            for col_idx in key:
                for row in grid:
                    if col_idx < len(row):
                        result += row[col_idx]
            
            hint = f"This is a columnar transposition with key: {key}"
            return result, key, hint
        else:
            # Decrypt the transposition cipher
            num_columns = len(key)
            num_rows = (len(text) + num_columns - 1) // num_columns
            
            # Create empty grid
            grid = [[''] * num_columns for _ in range(num_rows)]
            
            # Calculate column heights (last column may be shorter)
            col_heights = [num_rows] * num_columns
            remaining = len(text) % num_columns
            if remaining > 0:
                for i in range(num_columns - remaining, num_columns):
                    col_heights[i] -= 1
            
            # Fill the grid according to the key
            pos = 0
            for col_idx in key:
                for row in range(col_heights[col_idx]):
                    if pos < len(text):
                        grid[row][col_idx] = text[pos]
                        pos += 1
            
            # Read the grid row by row
            result = ""
            for row in grid:
                result += ''.join(row)
            
            # Remove any padding
            result = result.rstrip()
            
            return result
