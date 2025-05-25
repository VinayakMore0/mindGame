"""
Tutorial module for Cipher Clash game.
Provides interactive tutorials for different cipher types.
"""

import time
import random
import string
from mind_games_project.games.cipher_clash.modules.encryption import (
    caesar_cipher, atbash_cipher, reverse_cipher,
    vigenere_cipher, transposition_cipher
)
from mind_games_project.games.cipher_clash.modules.cipher_helper import get_cipher_description

class CipherTutorial:
    """Class for providing interactive cipher tutorials."""
    
    def __init__(self):
        """Initialize the tutorial."""
        self.width = 80  # Terminal width for formatting
    
    def show_tutorial_menu(self):
        """
        Display the tutorial menu and get user selection.
        
        Returns:
            str: Selected cipher type or None if user exits
        """
        print("=" * self.width)
        print("CIPHER CLASH TUTORIALS".center(self.width))
        print("=" * self.width)
        print("\nSelect a cipher type to learn about:")
        print("1. Caesar Cipher")
        print("2. Atbash Cipher")
        print("3. Reverse Cipher")
        print("4. Substitution Cipher")
        print("5. Vigenère Cipher")
        print("6. Transposition Cipher")
        print("7. Playfair Cipher")
        print("0. Return to Main Menu")
        
        while True:
            choice = input("\nEnter your choice (0-7): ")
            if choice == '0':
                return None
            elif choice == '1':
                return 'caesar'
            elif choice == '2':
                return 'atbash'
            elif choice == '3':
                return 'reverse'
            elif choice == '4':
                return 'substitution'
            elif choice == '5':
                return 'vigenere'
            elif choice == '6':
                return 'transposition'
            elif choice == '7':
                return 'playfair'
            else:
                print("Invalid choice. Please try again.")
    
    def run_tutorial(self, cipher_type):
        """
        Run a tutorial for a specific cipher type.
        
        Args:
            cipher_type (str): The type of cipher for the tutorial
        """
        print("\n" + "=" * self.width)
        print(f"{cipher_type.upper()} CIPHER TUTORIAL".center(self.width))
        print("=" * self.width + "\n")
        
        # Show description
        description = get_cipher_description(cipher_type)
        print(description)
        print("\n" + "-" * self.width + "\n")
        
        # Show examples
        print("EXAMPLES:\n")
        self.show_cipher_examples(cipher_type)
        print("\n" + "-" * self.width + "\n")
        
        # Interactive practice
        print("PRACTICE:\n")
        self.interactive_practice(cipher_type)
        
        print("\n" + "=" * self.width)
        print("Tutorial Complete!".center(self.width))
        print("=" * self.width)
        input("\nPress Enter to continue...")
    
    def show_cipher_examples(self, cipher_type):
        """
        Show examples of encryption and decryption for a cipher type.
        
        Args:
            cipher_type (str): The type of cipher
        """
        # Sample plaintext messages
        sample_texts = [
            "HELLO WORLD",
            "CIPHER CLASH",
            "SECRET MESSAGE"
        ]
        
        # Show examples for each sample text
        for text in sample_texts:
            print(f"Plaintext: {text}")
            
            if cipher_type == 'caesar':
                shift = 3
                encrypted = caesar_cipher(text, shift)
                print(f"Caesar Cipher (Shift {shift}): {encrypted}")
                print(f"Decrypted: {caesar_cipher(encrypted, 26 - shift)}")
                
            elif cipher_type == 'atbash':
                encrypted = atbash_cipher(text)
                print(f"Atbash Cipher: {encrypted}")
                print(f"Decrypted: {atbash_cipher(encrypted)}")
                
            elif cipher_type == 'reverse':
                encrypted = reverse_cipher(text)
                print(f"Reverse Cipher: {encrypted}")
                print(f"Decrypted: {reverse_cipher(encrypted)}")
                
            elif cipher_type == 'substitution':
                # Create a simple substitution for the example
                alphabet = string.ascii_uppercase
                shifted = alphabet[13:] + alphabet[:13]  # ROT13 for simplicity
                substitution_map = dict(zip(alphabet, shifted))
                
                encrypted = ''.join(substitution_map.get(c, c) for c in text)
                print(f"Substitution Cipher: {encrypted}")
                
                # Reverse the substitution map for decryption
                reverse_map = dict(zip(shifted, alphabet))
                decrypted = ''.join(reverse_map.get(c, c) for c in encrypted)
                print(f"Decrypted: {decrypted}")
                
            elif cipher_type == 'vigenere':
                key = "KEY"
                encrypted = vigenere_cipher(text, key)
                print(f"Vigenère Cipher (Key: {key}): {encrypted}")
                
                # Decrypt by using the inverse operation
                from mind_games_project.games.cipher_clash.modules.encryption import vigenere_decrypt
                decrypted = vigenere_decrypt(encrypted, key)
                print(f"Decrypted: {decrypted}")
                
            elif cipher_type == 'transposition':
                columns = 3
                encrypted = transposition_cipher(text, columns)
                print(f"Transposition Cipher ({columns} columns): {encrypted}")
                
                # Decryption would be more complex, so we'll just note that
                print("Decryption involves rearranging the columns back to rows.")
                
            elif cipher_type == 'playfair':
                key = "CIPHER"
                from mind_games_project.games.cipher_clash.modules.playfair import playfair_encrypt, playfair_decrypt
                encrypted = playfair_encrypt(text, key)
                print(f"Playfair Cipher (Key: {key}): {encrypted}")
                decrypted = playfair_decrypt(encrypted, key)
                print(f"Decrypted: {decrypted}")
            
            print()
    
    def interactive_practice(self, cipher_type):
        """
        Provide interactive practice for a cipher type.
        
        Args:
            cipher_type (str): The type of cipher
        """
        print("Let's practice with this cipher!\n")
        
        # Generate a simple plaintext
        words = ["HELLO", "WORLD", "CIPHER", "SECRET", "MESSAGE", "CODE", "PUZZLE"]
        plaintext = random.choice(words)
        
        print(f"Plaintext: {plaintext}")
        
        # Encrypt based on cipher type
        if cipher_type == 'caesar':
            shift = random.randint(1, 25)
            encrypted = caesar_cipher(plaintext, shift)
            print(f"This text has been encrypted with a Caesar cipher using shift {shift}.")
            print(f"Encrypted: {encrypted}")
            
            # Ask user to decrypt
            print("\nTry to decrypt it by shifting each letter back by the same amount.")
            user_input = input("Your decryption: ").strip().upper()
            
            if user_input == plaintext:
                print("Correct! You've successfully decrypted the message.")
            else:
                print(f"Not quite. The correct decryption is: {plaintext}")
                
        elif cipher_type == 'atbash':
            encrypted = atbash_cipher(plaintext)
            print("This text has been encrypted with an Atbash cipher.")
            print(f"Encrypted: {encrypted}")
            
            # Ask user to decrypt
            print("\nTry to decrypt it by replacing each letter with its mirror in the alphabet.")
            user_input = input("Your decryption: ").strip().upper()
            
            if user_input == plaintext:
                print("Correct! You've successfully decrypted the message.")
            else:
                print(f"Not quite. The correct decryption is: {plaintext}")
                
        elif cipher_type == 'reverse':
            encrypted = reverse_cipher(plaintext)
            print("This text has been encrypted with a Reverse cipher.")
            print(f"Encrypted: {encrypted}")
            
            # Ask user to decrypt
            print("\nTry to decrypt it by reading it backwards.")
            user_input = input("Your decryption: ").strip().upper()
            
            if user_input == plaintext:
                print("Correct! You've successfully decrypted the message.")
            else:
                print(f"Not quite. The correct decryption is: {plaintext}")
                
        elif cipher_type == 'substitution':
            # Use a simple substitution for practice
            alphabet = string.ascii_uppercase
            shifted = alphabet[13:] + alphabet[:13]  # ROT13 for simplicity
            substitution_map = dict(zip(alphabet, shifted))
            
            encrypted = ''.join(substitution_map.get(c, c) for c in plaintext)
            print("This text has been encrypted with a Substitution cipher.")
            print(f"Encrypted: {encrypted}")
            print("For this example, we're using ROT13 (each letter is replaced by the one 13 positions after it).")
            
            # Ask user to decrypt
            print("\nTry to decrypt it by reversing the substitution.")
            user_input = input("Your decryption: ").strip().upper()
            
            if user_input == plaintext:
                print("Correct! You've successfully decrypted the message.")
            else:
                print(f"Not quite. The correct decryption is: {plaintext}")
                
        elif cipher_type == 'vigenere':
            key = "KEY"
            encrypted = vigenere_cipher(plaintext, key)
            print(f"This text has been encrypted with a Vigenère cipher using the key '{key}'.")
            print(f"Encrypted: {encrypted}")
            
            # Ask user to decrypt
            print("\nTry to decrypt it using the key.")
            user_input = input("Your decryption: ").strip().upper()
            
            if user_input == plaintext:
                print("Correct! You've successfully decrypted the message.")
            else:
                print(f"Not quite. The correct decryption is: {plaintext}")
                
        elif cipher_type == 'transposition':
            columns = 3
            encrypted = transposition_cipher(plaintext, columns)
            print(f"This text has been encrypted with a Transposition cipher using {columns} columns.")
            print(f"Encrypted: {encrypted}")
            
            # Ask user to decrypt
            print("\nTry to decrypt it by rearranging the letters.")
            user_input = input("Your decryption: ").strip().upper()
            
            if user_input == plaintext:
                print("Correct! You've successfully decrypted the message.")
            else:
                print(f"Not quite. The correct decryption is: {plaintext}")
                
        elif cipher_type == 'playfair':
            key = "CIPHER"
            from mind_games_project.games.cipher_clash.modules.playfair import playfair_encrypt
            encrypted = playfair_encrypt(plaintext, key)
            print(f"This text has been encrypted with a Playfair cipher using the key '{key}'.")
            print(f"Encrypted: {encrypted}")
            
            # Ask user to decrypt
            print("\nTry to decrypt it using the Playfair rules.")
            user_input = input("Your decryption: ").strip().upper()
            
            if user_input == plaintext:
                print("Correct! You've successfully decrypted the message.")
            else:
                print(f"Not quite. The correct decryption is: {plaintext}")

def run_tutorials():
    """Run the cipher tutorials."""
    tutorial = CipherTutorial()
    
    while True:
        cipher_type = tutorial.show_tutorial_menu()
        
        if cipher_type is None:
            break
            
        tutorial.run_tutorial(cipher_type)
