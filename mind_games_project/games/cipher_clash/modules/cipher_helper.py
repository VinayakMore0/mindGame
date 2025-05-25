"""
Cipher helper module for Cipher Clash game.
Contains additional functions for working with ciphers.
"""

import random
import string
from mind_games_project.games.cipher_clash.modules.playfair import playfair_encrypt, playfair_decrypt

def get_cipher_description(cipher_type):
    """
    Get a description of a cipher type.
    
    Args:
        cipher_type (str): The type of cipher
        
    Returns:
        str: Description of the cipher
    """
    descriptions = {
        'caesar': (
            "The Caesar cipher is one of the simplest and most widely known encryption techniques. "
            "It is a type of substitution cipher in which each letter in the plaintext is replaced "
            "by a letter some fixed number of positions down the alphabet. For example, with a "
            "shift of 1, A would be replaced by B, B would become C, and so on."
        ),
        'atbash': (
            "The Atbash cipher is a simple substitution cipher that was originally used for the "
            "Hebrew alphabet. It works by replacing each letter with its mirror letter in the "
            "alphabet. For example, in English, A becomes Z, B becomes Y, and so on."
        ),
        'reverse': (
            "The Reverse cipher simply reverses the order of characters in the plaintext. "
            "For example, 'HELLO' becomes 'OLLEH'. This is one of the simplest ciphers but "
            "can still be challenging when combined with other encryption methods."
        ),
        'substitution': (
            "A Substitution cipher replaces each letter of the plaintext with another letter "
            "according to a fixed mapping. Unlike the Caesar cipher, which uses a simple shift, "
            "a substitution cipher can use any permutation of the alphabet."
        ),
        'vigenere': (
            "The Vigenère cipher is a method of encrypting alphabetic text by using a simple "
            "form of polyalphabetic substitution. It uses a keyword to determine different "
            "Caesar shifts for different positions in the text, making it much stronger than "
            "a simple Caesar cipher."
        ),
        'transposition': (
            "A Transposition cipher rearranges the letters of the plaintext without changing "
            "the actual letters themselves. In a columnar transposition, the message is written "
            "in rows of a fixed length, and then read out column by column."
        ),
        'playfair': (
            "The Playfair cipher encrypts pairs of letters (digraphs) instead of single letters. "
            "It uses a 5x5 grid of letters constructed using a keyword, where I and J are "
            "typically combined. Each pair of letters in the plaintext is transformed according "
            "to their positions in the grid."
        )
    }
    
    return descriptions.get(cipher_type, "No description available for this cipher type.")

def get_cipher_hint(cipher_type, encrypted_text, solution):
    """
    Get a hint for solving a specific cipher.
    
    Args:
        cipher_type (str): The type of cipher
        encrypted_text (str): The encrypted text
        solution (str): The solution (plaintext)
        
    Returns:
        str: A hint for solving the cipher
    """
    hints = {
        'caesar': [
            "Try shifting each letter by a consistent number of positions in the alphabet.",
            "Look for common words or patterns after shifting by different amounts.",
            "The letter 'E' is the most common letter in English - it might help identify the shift.",
            f"The first letter of the solution is '{solution[0]}'."
        ],
        'atbash': [
            "This cipher replaces each letter with its mirror in the alphabet (A→Z, B→Y, etc.).",
            "Try reversing the position of each letter in the alphabet.",
            "A becomes Z, B becomes Y, C becomes X, and so on.",
            f"The first letter of the solution is '{solution[0]}'."
        ],
        'reverse': [
            "Try reading the message backwards.",
            "The last letter of the encrypted text is the first letter of the solution.",
            "Simply reverse the order of all characters.",
            f"The first letter of the solution is '{solution[0]}'."
        ],
        'substitution': [
            "Each letter is consistently replaced with another letter throughout the text.",
            "Look for patterns in letter frequency - 'E', 'T', 'A', 'O' are common in English.",
            "Short words like 'THE', 'AND', 'OR' can help you identify substitutions.",
            f"The first letter of the solution is '{solution[0]}'."
        ],
        'vigenere': [
            "This cipher uses a keyword to determine multiple shift values.",
            "Try to identify the length of the keyword by looking for repeated patterns.",
            "Once you know the keyword length, you can solve each position separately.",
            f"The first letter of the solution is '{solution[0]}'."
        ],
        'transposition': [
            "The letters remain the same but their positions are rearranged.",
            "Try rearranging the text in columns and reading it in a different order.",
            "The number of columns is key to solving this cipher.",
            f"The first letter of the solution is '{solution[0]}'."
        ],
        'playfair': [
            "This cipher encrypts pairs of letters using a 5x5 grid.",
            "Letters in the same row shift right, letters in the same column shift down.",
            "Letters forming a rectangle swap to the opposite corners.",
            f"The first letter of the solution is '{solution[0]}'."
        ]
    }
    
    # Get hints for the specific cipher type, or use generic hints
    cipher_hints = hints.get(cipher_type, [
        "Look for patterns in the encrypted text.",
        "Try different decryption methods to see what works.",
        f"The first letter of the solution is '{solution[0]}'."
    ])
    
    # Return a random hint from the available ones
    return random.choice(cipher_hints)

def generate_cipher_challenge(difficulty):
    """
    Generate a complete cipher challenge with multiple steps.
    
    Args:
        difficulty (str): Difficulty level ('easy', 'medium', 'hard')
        
    Returns:
        dict: A challenge with instructions, ciphers, and solutions
    """
    # Define complexity based on difficulty
    if difficulty == 'easy':
        steps = 2
        cipher_types = ['caesar', 'atbash', 'reverse']
        word_count = 3
        time_limit = 180  # 3 minutes
    elif difficulty == 'medium':
        steps = 3
        cipher_types = ['caesar', 'atbash', 'reverse', 'substitution', 'vigenere']
        word_count = 4
        time_limit = 300  # 5 minutes
    else:  # hard
        steps = 4
        cipher_types = ['caesar', 'atbash', 'reverse', 'substitution', 'vigenere', 'transposition', 'playfair']
        word_count = 5
        time_limit = 420  # 7 minutes
    
    # Generate a final message
    final_message = generate_message(word_count)
    
    # Create a series of encryption steps
    challenge_steps = []
    current_text = final_message
    
    # Select random cipher types for each step (without repeating)
    selected_ciphers = random.sample(cipher_types, min(steps, len(cipher_types)))
    if len(selected_ciphers) < steps:
        # If we need more steps than available cipher types, add some repeats
        selected_ciphers.extend(random.choices(cipher_types, k=steps - len(selected_ciphers)))
    
    # Shuffle the selected ciphers
    random.shuffle(selected_ciphers)
    
    # Generate each step in reverse (from solution to initial cipher)
    for i, cipher_type in enumerate(selected_ciphers):
        # Generate parameters for this cipher
        params = generate_cipher_params(cipher_type, difficulty)
        
        # Encrypt the current text
        encrypted_text = encrypt_with_params(current_text, cipher_type, params)
        
        # Add this step to our challenge
        challenge_steps.append({
            'step': i + 1,
            'cipher_type': cipher_type,
            'params': params,
            'encrypted_text': encrypted_text,
            'decrypted_text': current_text
        })
        
        # The encrypted text becomes the input for the next step
        current_text = encrypted_text
    
    # Reverse the steps so they go from initial cipher to solution
    challenge_steps.reverse()
    
    # Create the final challenge
    challenge = {
        'difficulty': difficulty,
        'time_limit': time_limit,
        'steps': challenge_steps,
        'initial_cipher': challenge_steps[0]['encrypted_text'],
        'final_solution': final_message
    }
    
    return challenge

def generate_message(word_count):
    """
    Generate a random message for a cipher challenge.
    
    Args:
        word_count (int): Number of words in the message
        
    Returns:
        str: The generated message
    """
    # List of words for message generation
    words = [
        "CIPHER", "CODE", "SECRET", "HIDDEN", "MESSAGE", "PUZZLE", "MYSTERY",
        "ENCRYPT", "DECRYPT", "SOLVE", "CHALLENGE", "CRYPTIC", "ENIGMA",
        "KEY", "LOCK", "UNLOCK", "DISCOVER", "FIND", "REVEAL", "CONCEAL",
        "OBSCURE", "SHADOW", "LIGHT", "DARK", "NIGHT", "DAY", "SUN", "MOON",
        "STAR", "PLANET", "GALAXY", "UNIVERSE", "COSMIC", "QUANTUM", "ATOM",
        "PARTICLE", "WAVE", "ENERGY", "MATTER", "TIME", "SPACE", "DIMENSION",
        "REALITY", "VIRTUAL", "DIGITAL", "ANALOG", "BINARY", "ALGORITHM"
    ]
    
    # Select random words
    selected_words = random.sample(words, min(word_count, len(words)))
    
    # Create a message
    message = " ".join(selected_words)
    
    return message

def generate_cipher_params(cipher_type, difficulty):
    """
    Generate parameters for a specific cipher type.
    
    Args:
        cipher_type (str): The type of cipher
        difficulty (str): Difficulty level
        
    Returns:
        dict: Parameters for the cipher
    """
    if cipher_type == 'caesar':
        # For Caesar cipher, generate a shift value
        if difficulty == 'easy':
            shift = random.randint(1, 5)
        elif difficulty == 'medium':
            shift = random.randint(6, 15)
        else:  # hard
            shift = random.randint(16, 25)
        return {'shift': shift}
    
    elif cipher_type == 'vigenere':
        # For Vigenère cipher, generate a key
        if difficulty == 'easy':
            key_length = random.randint(2, 3)
        elif difficulty == 'medium':
            key_length = random.randint(4, 6)
        else:  # hard
            key_length = random.randint(7, 10)
        
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(key_length))
        return {'key': key}
    
    elif cipher_type == 'transposition':
        # For transposition cipher, generate number of columns
        if difficulty == 'easy':
            columns = random.randint(2, 3)
        elif difficulty == 'medium':
            columns = random.randint(4, 6)
        else:  # hard
            columns = random.randint(7, 10)
        return {'columns': columns}
    
    elif cipher_type == 'playfair':
        # For Playfair cipher, generate a key
        if difficulty == 'easy':
            key = random.choice(['CIPHER', 'PUZZLE', 'SECRET', 'ENIGMA', 'CRYPTO'])
        elif difficulty == 'medium':
            key = random.choice(['KEYBOARD', 'ALGORITHM', 'CHALLENGE', 'QUESTION', 'SOLUTION'])
        else:  # hard
            key = random.choice(['CRYPTOGRAPHY', 'INTELLIGENCE', 'MATHEMATICS', 'COMPLEXITY', 'ENCRYPTION'])
        return {'key': key}
    
    elif cipher_type == 'substitution':
        # For substitution cipher, we'll generate a full substitution alphabet
        alphabet = list(string.ascii_uppercase)
        shuffled = random.sample(alphabet, len(alphabet))
        substitution_map = dict(zip(alphabet, shuffled))
        return {'substitution_map': substitution_map}
    
    # For atbash and reverse ciphers, no parameters are needed
    return {}

def encrypt_with_params(text, cipher_type, params):
    """
    Encrypt text using a specific cipher type and parameters.
    
    Args:
        text (str): The text to encrypt
        cipher_type (str): The type of cipher
        params (dict): Parameters for the cipher
        
    Returns:
        str: The encrypted text
    """
    if cipher_type == 'caesar':
        shift = params.get('shift', 3)
        return ''.join(
            chr((ord(c) - ord('A') + shift) % 26 + ord('A')) if c.isalpha() and c.isupper()
            else (chr((ord(c) - ord('a') + shift) % 26 + ord('a')) if c.isalpha() and c.islower() else c)
            for c in text
        )
    
    elif cipher_type == 'atbash':
        return ''.join(
            chr(ord('Z') - (ord(c) - ord('A'))) if c.isalpha() and c.isupper()
            else (chr(ord('z') - (ord(c) - ord('a'))) if c.isalpha() and c.islower() else c)
            for c in text
        )
    
    elif cipher_type == 'reverse':
        return text[::-1]
    
    elif cipher_type == 'substitution':
        substitution_map = params.get('substitution_map', {})
        return ''.join(
            substitution_map.get(c, c) if c.isalpha() and c.isupper()
            else (substitution_map.get(c.upper(), c).lower() if c.isalpha() and c.islower() else c)
            for c in text
        )
    
    elif cipher_type == 'vigenere':
        key = params.get('key', 'KEY')
        key = key.upper()
        result = ""
        key_index = 0
        
        for c in text:
            if c.isalpha():
                # Get the shift from the key
                shift = ord(key[key_index % len(key)]) - ord('A')
                
                if c.isupper():
                    # Encrypt uppercase letter
                    result += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
                else:
                    # Encrypt lowercase letter
                    result += chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
                
                key_index += 1
            else:
                result += c
        
        return result
    
    elif cipher_type == 'transposition':
        columns = params.get('columns', 3)
        # Remove spaces for simplicity
        text_no_spaces = ''.join(c for c in text if c != ' ')
        
        # Calculate rows needed
        rows = (len(text_no_spaces) + columns - 1) // columns
        
        # Pad the text if necessary
        padded_text = text_no_spaces + ' ' * (rows * columns - len(text_no_spaces))
        
        # Create the grid
        grid = []
        for i in range(0, len(padded_text), columns):
            grid.append(padded_text[i:i+columns])
        
        # Read by columns
        result = ""
        for col in range(columns):
            for row in range(rows):
                if col < len(grid[row]):
                    result += grid[row][col]
        
        return result
    
    elif cipher_type == 'playfair':
        key = params.get('key', 'CIPHER')
        return playfair_encrypt(text, key)
    
    # Default case
    return text
