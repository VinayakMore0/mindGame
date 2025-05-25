"""
Question Generator module for Cipher Clash.
Generates random cipher puzzles of varying difficulty.
"""
import random
import json
import os
from mind_games_project.games.cipher_clash.config import DATA_DIR, CIPHER_TYPES, DIFFICULTY_LEVELS
from mind_games_project.games.cipher_clash.game_engine.cipher_manager import CipherManager

class QuestionGenerator:
    """Generates cipher puzzles for the game."""
    
    def __init__(self):
        """Initialize the question generator."""
        self.cipher_manager = CipherManager()
        self.phrases_file = os.path.join(DATA_DIR, "phrases.json")
        self.phrases = self._load_phrases()
    
    def _load_phrases(self):
        """Load phrases from the phrases.json file."""
        try:
            if os.path.exists(self.phrases_file):
                with open(self.phrases_file, 'r') as f:
                    return json.load(f)
            else:
                # Default phrases if file doesn't exist
                return {
                    "easy": [
                        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
                        "HELLO WORLD",
                        "PRACTICE MAKES PERFECT",
                        "KEEP IT SIMPLE",
                        "TIME FLIES WHEN HAVING FUN"
                    ],
                    "medium": [
                        "CRYPTOGRAPHY IS THE PRACTICE OF SECURE COMMUNICATION",
                        "THE ART OF WRITING AND SOLVING CODES",
                        "KNOWLEDGE IS POWER BUT ENTHUSIASM PULLS THE SWITCH",
                        "EVERY SOLUTION BREEDS NEW PROBLEMS",
                        "THE ONLY WAY TO DO GREAT WORK IS TO LOVE WHAT YOU DO"
                    ],
                    "hard": [
                        "CRYPTANALYSIS IS THE ART OF BREAKING CODES AND CIPHERS",
                        "IN THE WORLD OF CRYPTOGRAPHY SECURITY DEPENDS ON THE KEY LENGTH",
                        "THE SCIENCE OF MAKING AND BREAKING SECRET CODES HAS A LONG HISTORY",
                        "QUANTUM COMPUTERS MAY SOMEDAY BREAK MANY ENCRYPTION SYSTEMS",
                        "STEGANOGRAPHY HIDES THE EXISTENCE OF A SECRET MESSAGE"
                    ]
                }
        except Exception as e:
            print(f"Error loading phrases: {e}")
            # Fallback phrases
            return {
                "easy": ["HELLO WORLD", "CIPHER CLASH"],
                "medium": ["CRYPTOGRAPHY IS FUN", "DECODE THIS MESSAGE"],
                "hard": ["CRYPTANALYSIS IS CHALLENGING", "ENCRYPTION PROTECTS DATA"]
            }
    
    def generate_question(self, difficulty, cipher_type=None):
        """
        Generate a cipher puzzle.
        
        Args:
            difficulty (str): The difficulty level ('easy', 'medium', 'hard')
            cipher_type (str, optional): The specific cipher type to use
            
        Returns:
            dict: A question object with the following keys:
                - original_text: The plain text
                - encrypted_text: The encrypted text
                - cipher_type: The type of cipher used
                - key: The encryption key
                - hint: A hint for solving the puzzle
                - difficulty: The difficulty level
        """
        # Validate difficulty
        if difficulty not in DIFFICULTY_LEVELS:
            difficulty = "medium"
        
        # Select a random cipher type if not specified
        if cipher_type is None or cipher_type not in CIPHER_TYPES:
            available_ciphers = list(CIPHER_TYPES.keys())
            cipher_type = random.choice(available_ciphers)
        
        # Select a random phrase based on difficulty
        phrases = self.phrases.get(difficulty, self.phrases["medium"])
        original_text = random.choice(phrases)
        
        # Apply complexity adjustments based on difficulty
        complexity = DIFFICULTY_LEVELS[difficulty]["cipher_complexity"]
        
        # Generate encryption parameters based on complexity
        params = {}
        if cipher_type == "caesar":
            # For Caesar cipher, higher complexity means larger shifts
            if complexity < 0.5:
                params["shift"] = random.randint(1, 10)
            else:
                params["shift"] = random.randint(11, 25)
        
        elif cipher_type == "vigenere":
            # For Vigenère cipher, higher complexity means longer keys
            key_length = int(3 + complexity * 5)  # 3-8 characters
            params["key"] = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(key_length))
        
        # Encrypt the text
        encrypted_text, key, hint = self.cipher_manager.encrypt(original_text, cipher_type, **params)
        
        # Create the question object
        question = {
            "original_text": original_text,
            "encrypted_text": encrypted_text,
            "cipher_type": cipher_type,
            "key": key,
            "hint": hint,
            "difficulty": difficulty
        }
        
        return question
    
    def verify_answer(self, question, user_answer):
        """
        Verify if the user's answer is correct.
        
        Args:
            question (dict): The question object
            user_answer (str): The user's answer
            
        Returns:
            tuple: (is_correct, score)
                - is_correct (bool): True if the answer is correct
                - score (int): The score for this answer
        """
        # Normalize both texts for comparison (remove spaces, convert to uppercase)
        original = ''.join(question["original_text"].upper().split())
        user = ''.join(user_answer.upper().split())
        
        # Calculate similarity (allowing for some typos)
        similarity = self._calculate_similarity(original, user)
        
        # Determine if the answer is correct (e.g., >80% similarity)
        is_correct = similarity >= 0.8
        
        # Calculate score based on similarity and difficulty
        difficulty_multiplier = DIFFICULTY_LEVELS[question["difficulty"]]["score_multiplier"]
        base_score = int(100 * similarity)
        score = int(base_score * difficulty_multiplier)
        
        return is_correct, score
    
    def _calculate_similarity(self, str1, str2):
        """
        Calculate the similarity between two strings.
        Uses a simple ratio of matching characters.
        
        Args:
            str1 (str): First string
            str2 (str): Second string
            
        Returns:
            float: Similarity ratio (0.0 to 1.0)
        """
        # Simple implementation - can be improved with more sophisticated algorithms
        if not str1 or not str2:
            return 0.0
        
        # Use the shorter string as reference
        if len(str1) < len(str2):
            str1, str2 = str2, str1
        
        # Count matching characters
        matches = sum(c1 == c2 for c1, c2 in zip(str1[:len(str2)], str2))
        
        # Calculate similarity ratio
        similarity = matches / max(len(str1), len(str2))
        
        return similarity
