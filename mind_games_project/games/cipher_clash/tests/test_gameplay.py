"""
Unit tests for game logic and scoring.
"""
import unittest
import sys
import os
import time

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from mind_games_project.games.cipher_clash.game_engine.game_logic import GameState
from mind_games_project.games.cipher_clash.game_engine.question_generator import QuestionGenerator

class TestQuestionGenerator(unittest.TestCase):
    """Test cases for the QuestionGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.question_generator = QuestionGenerator()
    
    def test_generate_question(self):
        """Test question generation for different difficulties and cipher types."""
        # Test for each difficulty
        for difficulty in ["easy", "medium", "hard"]:
            question = self.question_generator.generate_question(difficulty)
            
            self.assertIsNotNone(question)
            self.assertEqual(question["difficulty"], difficulty)
            self.assertIn(question["cipher_type"], ["caesar", "vigenere", "morse", "substitution", "transposition"])
            self.assertIsNotNone(question["original_text"])
            self.assertIsNotNone(question["encrypted_text"])
            self.assertIsNotNone(question["hint"])
        
        # Test for specific cipher type
        for cipher_type in ["caesar", "vigenere", "morse", "substitution", "transposition"]:
            question = self.question_generator.generate_question("medium", cipher_type)
            
            self.assertIsNotNone(question)
            self.assertEqual(question["cipher_type"], cipher_type)
    
    def test_verify_answer(self):
        """Test answer verification."""
        # Generate a question
        question = self.question_generator.generate_question("medium")
        
        # Test correct answer
        is_correct, score = self.question_generator.verify_answer(question, question["original_text"])
        self.assertTrue(is_correct)
        self.assertGreater(score, 0)
        
        # Test incorrect answer
        is_correct, score = self.question_generator.verify_answer(question, "WRONG ANSWER")
        self.assertFalse(is_correct)
        
        # Test partial answer (should be considered incorrect)
        partial_text = question["original_text"][:5]
        is_correct, score = self.question_generator.verify_answer(question, partial_text)
        self.assertFalse(is_correct)
        
        # Test answer with typos (should be somewhat tolerant)
        typo_text = question["original_text"].replace("E", "3").replace("A", "4")
        is_correct, score = self.question_generator.verify_answer(question, typo_text)
        # This might be correct or incorrect depending on similarity threshold
        if is_correct:
            self.assertGreater(score, 0)

class TestGameState(unittest.TestCase):
    """Test cases for the GameState class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game_state = GameState()
    
    def test_start_game(self):
        """Test starting a new game."""
        self.game_state.start_game("medium", "caesar")
        
        self.assertEqual(self.game_state.difficulty, "medium")
        self.assertEqual(self.game_state.selected_cipher_type, "caesar")
        self.assertTrue(self.game_state.game_active)
        self.assertFalse(self.game_state.game_over)
        self.assertEqual(self.game_state.questions_answered, 0)
        self.assertEqual(self.game_state.correct_answers, 0)
        self.assertEqual(self.game_state.total_score, 0)
        self.assertIsNotNone(self.game_state.current_question)
    
    def test_submit_answer(self):
        """Test submitting answers."""
        self.game_state.start_game("medium", "caesar")
        
        # Get the current question
        question = self.game_state.current_question
        
        # Submit correct answer
        is_correct = self.game_state.submit_answer(question["original_text"])
        self.assertTrue(is_correct)
        self.assertEqual(self.game_state.questions_answered, 1)
        self.assertEqual(self.game_state.correct_answers, 1)
        self.assertGreater(self.game_state.total_score, 0)
        
        # The question should have changed
        self.assertNotEqual(self.game_state.current_question["encrypted_text"], question["encrypted_text"])
        
        # Submit incorrect answer
        old_score = self.game_state.total_score
        is_correct = self.game_state.submit_answer("WRONG ANSWER")
        self.assertFalse(is_correct)
        self.assertEqual(self.game_state.questions_answered, 2)
        self.assertEqual(self.game_state.correct_answers, 1)
        self.assertEqual(self.game_state.total_score, old_score)  # Score shouldn't change
    
    def test_use_hint(self):
        """Test using hints."""
        self.game_state.start_game("medium")
        
        # Get initial hint count
        initial_hints = self.game_state.hints_available
        
        # Use a hint
        hint = self.game_state.use_hint()
        self.assertIsNotNone(hint)
        self.assertEqual(self.game_state.hints_available, initial_hints - 1)
        self.assertTrue(self.game_state.hint_revealed)
        
        # Try to use the same hint again (should fail)
        hint = self.game_state.use_hint()
        self.assertIsNone(hint)
        self.assertEqual(self.game_state.hints_available, initial_hints - 1)
        
        # Generate a new question
        self.game_state.generate_new_question()
        self.assertFalse(self.game_state.hint_revealed)
        
        # Use all remaining hints
        for _ in range(initial_hints - 1):
            hint = self.game_state.use_hint()
            self.assertIsNotNone(hint)
            self.game_state.generate_new_question()
        
        # Try to use a hint when none are left
        hint = self.game_state.use_hint()
        self.assertIsNone(hint)
        self.assertEqual(self.game_state.hints_available, 0)
    
    def test_timer(self):
        """Test the game timer."""
        self.game_state.start_game("easy")  # Easy mode has longer time limit
        
        # Check initial time
        self.assertGreater(self.game_state.get_time_remaining(), 0)
        self.assertEqual(self.game_state.get_progress_percentage(), 0)
        
        # Wait a short time and update
        time.sleep(0.1)
        self.game_state.update_timer()
        
        # Time should have decreased
        self.assertLess(self.game_state.get_progress_percentage(), 0.1)  # Less than 10% elapsed
        
        # Format check
        time_str = self.game_state.get_time_remaining_formatted()
        self.assertRegex(time_str, r"\d{2}:\d{2}")  # Should be in MM:SS format
    
    def test_end_game(self):
        """Test ending the game."""
        self.game_state.start_game("medium")
        self.game_state.end_game()
        
        self.assertFalse(self.game_state.game_active)
        self.assertTrue(self.game_state.game_over)
        
        # Check results
        results = self.game_state.get_results()
        self.assertIn("total_score", results)
        self.assertIn("questions_answered", results)
        self.assertIn("correct_answers", results)
        self.assertIn("accuracy", results)
        self.assertIn("time_taken", results)
        self.assertIn("difficulty", results)

if __name__ == "__main__":
    unittest.main()
