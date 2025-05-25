"""
Playfair cipher implementation for Cipher Clash game.
"""

def create_playfair_matrix(key):
    """
    Create a 5x5 Playfair cipher matrix from a key.
    
    Args:
        key (str): The key to use for the matrix
        
    Returns:
        list: 5x5 matrix of characters
    """
    # Convert key to uppercase and remove duplicates while preserving order
    key = key.upper()
    key_chars = []
    for char in key:
        if char.isalpha() and char not in key_chars:
            # Replace J with I in the Playfair cipher
            if char == 'J':
                char = 'I'
            key_chars.append(char)
    
    # Create the alphabet without duplicates from the key
    # and replacing J with I
    alphabet = [c for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ" if c not in key_chars]
    
    # Combine key characters and remaining alphabet
    matrix_chars = key_chars + alphabet
    
    # Create 5x5 matrix
    matrix = []
    for i in range(0, 25, 5):
        matrix.append(matrix_chars[i:i+5])
    
    return matrix

def find_position(matrix, char):
    """
    Find the position of a character in the Playfair matrix.
    
    Args:
        matrix (list): The 5x5 Playfair matrix
        char (str): The character to find
        
    Returns:
        tuple: (row, col) position of the character
    """
    char = char.upper()
    # Replace J with I in the Playfair cipher
    if char == 'J':
        char = 'I'
        
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return (row, col)
    
    return None

def encrypt_playfair_digraph(matrix, a, b):
    """
    Encrypt a digraph (pair of letters) using the Playfair cipher.
    
    Args:
        matrix (list): The 5x5 Playfair matrix
        a (str): First character of the digraph
        b (str): Second character of the digraph
        
    Returns:
        tuple: (encrypted_a, encrypted_b) - The encrypted digraph
    """
    a_pos = find_position(matrix, a)
    b_pos = find_position(matrix, b)
    
    if a_pos is None or b_pos is None:
        # Non-alphabetic characters are left unchanged
        return a, b
    
    a_row, a_col = a_pos
    b_row, b_col = b_pos
    
    # Same row: take the character to the right (wrapping around)
    if a_row == b_row:
        return matrix[a_row][(a_col + 1) % 5], matrix[b_row][(b_col + 1) % 5]
    
    # Same column: take the character below (wrapping around)
    elif a_col == b_col:
        return matrix[(a_row + 1) % 5][a_col], matrix[(b_row + 1) % 5][b_col]
    
    # Rectangle: take the character in the same row but in the column of the other character
    else:
        return matrix[a_row][b_col], matrix[b_row][a_col]

def decrypt_playfair_digraph(matrix, a, b):
    """
    Decrypt a digraph (pair of letters) using the Playfair cipher.
    
    Args:
        matrix (list): The 5x5 Playfair matrix
        a (str): First character of the encrypted digraph
        b (str): Second character of the encrypted digraph
        
    Returns:
        tuple: (decrypted_a, decrypted_b) - The decrypted digraph
    """
    a_pos = find_position(matrix, a)
    b_pos = find_position(matrix, b)
    
    if a_pos is None or b_pos is None:
        # Non-alphabetic characters are left unchanged
        return a, b
    
    a_row, a_col = a_pos
    b_row, b_col = b_pos
    
    # Same row: take the character to the left (wrapping around)
    if a_row == b_row:
        return matrix[a_row][(a_col - 1) % 5], matrix[b_row][(b_col - 1) % 5]
    
    # Same column: take the character above (wrapping around)
    elif a_col == b_col:
        return matrix[(a_row - 1) % 5][a_col], matrix[(b_row - 1) % 5][b_col]
    
    # Rectangle: take the character in the same row but in the column of the other character
    else:
        return matrix[a_row][b_col], matrix[b_row][a_col]

def prepare_text_for_playfair(text):
    """
    Prepare text for Playfair encryption by:
    1. Converting to uppercase
    2. Removing non-alphabetic characters
    3. Replacing J with I
    4. Splitting into digraphs (pairs of letters)
    5. Handling repeated letters by inserting 'X' between them
    6. Adding a padding 'X' if the text has an odd length
    
    Args:
        text (str): The text to prepare
        
    Returns:
        list: List of digraphs
    """
    # Convert to uppercase and replace J with I
    text = text.upper().replace('J', 'I')
    
    # Remove non-alphabetic characters
    text = ''.join(char for char in text if char.isalpha())
    
    # Split into digraphs and handle repeated letters
    digraphs = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            # If the two letters are the same, insert an 'X'
            if text[i] == text[i+1]:
                digraphs.append((text[i], 'X'))
                i += 1
            else:
                digraphs.append((text[i], text[i+1]))
                i += 2
        else:
            # If there's a single letter left, add an 'X'
            digraphs.append((text[i], 'X'))
            i += 1
    
    return digraphs

def playfair_encrypt(text, key):
    """
    Encrypt text using the Playfair cipher.
    
    Args:
        text (str): The text to encrypt
        key (str): The encryption key
        
    Returns:
        str: The encrypted text
    """
    matrix = create_playfair_matrix(key)
    digraphs = prepare_text_for_playfair(text)
    
    encrypted_digraphs = []
    for a, b in digraphs:
        encrypted_a, encrypted_b = encrypt_playfair_digraph(matrix, a, b)
        encrypted_digraphs.append(encrypted_a + encrypted_b)
    
    return ''.join(encrypted_digraphs)

def playfair_decrypt(text, key):
    """
    Decrypt text using the Playfair cipher.
    
    Args:
        text (str): The text to decrypt
        key (str): The decryption key
        
    Returns:
        str: The decrypted text
    """
    matrix = create_playfair_matrix(key)
    
    # Split the text into digraphs
    digraphs = [(text[i], text[i+1]) for i in range(0, len(text), 2) if i+1 < len(text)]
    
    decrypted_digraphs = []
    for a, b in digraphs:
        decrypted_a, decrypted_b = decrypt_playfair_digraph(matrix, a, b)
        decrypted_digraphs.append(decrypted_a + decrypted_b)
    
    # Join the decrypted digraphs
    decrypted_text = ''.join(decrypted_digraphs)
    
    # Remove padding 'X' characters that might have been added
    # This is a simplified approach and might not be perfect
    if decrypted_text.endswith('X'):
        decrypted_text = decrypted_text[:-1]
    
    return decrypted_text
