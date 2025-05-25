"""
Unit tests for cipher algorithms.
"""
import unittest
import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from mind_games_project.games.cipher_clash.game_engine.cipher_manager import CipherManager

class TestCipherManager(unittest.TestCase):
    """Test cases for the CipherManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cipher_manager = CipherManager()
        self.test_text = "HELLO WORLD"
    
    def test_caesar_cipher(self):
        """Test Caesar cipher encryption and decryption."""
        # Test with a specific shift
        encrypted, shift, _ = self.cipher_manager.caesar_cipher(self.test_text, encrypt=True, shift=3)
        decrypted = self.cipher_manager.caesar_cipher(encrypted, encrypt=False, shift=3)
        
        self.assertEqual(shift, 3)
        self.assertEqual(decrypted, self.test_text)
        
        # Test with random shift
        encrypted, shift, _ = self.cipher_manager.caesar_cipher(self.test_text, encrypt=True)
        decrypted = self.cipher_manager.caesar_cipher(encrypted, encrypt=False, shift=shift)
        
        self.assertEqual(decrypted, self.test_text)
    
    def test_vigenere_cipher(self):
        """Test Vigenère cipher encryption and decryption."""
        # Test with a specific key
        key = "KEY"
        encrypted, returned_key, _ = self.cipher_manager.vigenere_cipher(self.test_text, encrypt=True, key=key)
        decrypted = self.cipher_manager.vigenere_cipher(encrypted, encrypt=False, key=key)
        
        self.assertEqual(returned_key, key)
        self.assertEqual(decrypted, self.test_text)
        
        # Test with random key
        encrypted, key, _ = self.cipher_manager.vigenere_cipher(self.test_text, encrypt=True)
        decrypted = self.cipher_manager.vigenere_cipher(encrypted, encrypt=False, key=key)
        
        self.assertEqual(decrypted, self.test_text)
    
    def test_morse_code(self):
        """Test Morse code conversion."""
        morse, _, _ = self.cipher_manager.morse_code(self.test_text, encrypt=True)
        decrypted = self.cipher_manager.morse_code(morse, encrypt=False)
        
        # Morse code conversion might lose some formatting, so compare without spaces
        self.assertEqual(decrypted.replace(" ", ""), self.test_text.replace(" ", ""))
    
    def test_substitution_cipher(self):
        """Test substitution cipher encryption and decryption."""
        encrypted, key, _ = self.cipher_manager.substitution_cipher(self.test_text, encrypt=True)
        decrypted = self.cipher_manager.substitution_cipher(encrypted, encrypt=False, key=key)
        
        self.assertEqual(decrypted, self.test_text)
    
    def test_transposition_cipher(self):
        """Test transposition cipher encryption and decryption."""
        encrypted, key, _ = self.cipher_manager.transposition_cipher(self.test_text, encrypt=True)
        decrypted = self.cipher_manager.transposition_cipher(encrypted, encrypt=False, key=key)
        
        # Transposition might add padding spaces, so strip them
        self.assertEqual(decrypted.strip(), self.test_text.strip())
    
    def test_encrypt_decrypt_workflow(self):
        """Test the full encrypt/decrypt workflow for all cipher types."""
        for cipher_type in self.cipher_manager.cipher_types:
            # Encrypt
            encrypted, key, hint = self.cipher_manager.encrypt(self.test_text, cipher_type)
            
            # Decrypt
            if cipher_type == "morse":
                # Morse code doesn't use a key
                decrypted = self.cipher_manager.decrypt(encrypted, cipher_type)
                self.assertEqual(decrypted.replace(" ", ""), self.test_text.replace(" ", ""))
            else:
                # Other ciphers use a key
                decrypted = self.cipher_manager.decrypt(encrypted, cipher_type, key=key)
                self.assertEqual(decrypted.strip(), self.test_text.strip())
            
            # Check that hint is provided
            self.assertIsNotNone(hint)

if __name__ == "__main__":
    unittest.main()
