"""
Question manager for Logic Arena game.
Handles logic question generation and validation.
"""
import random
import os
import json
from config import (
    QUESTIONS_DIR, SEQUENCE_COMPLETION, NUMBER_PATTERN, 
    ODD_ONE_OUT, GRID_DEDUCTION
)
from utils.helpers import load_questions

class QuestionManager:
    def __init__(self):
        """Initialize the question manager."""
        self.difficulties = ["easy", "medium", "hard"]
        self.questions = {}
        self.current_question = None
        self.current_difficulty = "easy"
        
        # Load questions from files
        self.load_all_questions()
    
    def load_all_questions(self):
        """Load questions for all difficulties."""
        for difficulty in self.difficulties:
            self.questions[difficulty] = load_questions(difficulty)
    
    def get_random_question(self, difficulty=None):
        """Get a random question of the specified difficulty."""
        if difficulty is None:
            difficulty = self.current_difficulty
        
        if difficulty not in self.questions or not self.questions[difficulty]:
            print(f"No questions available for difficulty: {difficulty}")
            return None
        
        self.current_question = random.choice(self.questions[difficulty])
        self.current_difficulty = difficulty
        return self.current_question
    
    def check_answer(self, answer):
        """Check if the provided answer is correct."""
        if not self.current_question:
            return False
        
        correct_answer = self.current_question["answer"]
        
        # Debug info
        print(f"User answer: {answer}")
        print(f"Correct answer: {correct_answer}")
        
        # Handle different types of answers
        if isinstance(correct_answer, list):
            return answer in correct_answer
        else:
            return answer == correct_answer
    
    def get_current_question(self):
        """Get the current question."""
        return self.current_question
    
    def get_current_difficulty(self):
        """Get the current difficulty."""
        return self.current_difficulty
    
    def set_difficulty(self, difficulty):
        """Set the current difficulty."""
        if difficulty in self.difficulties:
            self.current_difficulty = difficulty
    
    def get_next_difficulty(self):
        """Get the next difficulty level."""
        current_index = self.difficulties.index(self.current_difficulty)
        if current_index < len(self.difficulties) - 1:
            return self.difficulties[current_index + 1]
        return self.current_difficulty
    
    def increase_difficulty(self):
        """Increase the difficulty level if possible."""
        next_difficulty = self.get_next_difficulty()
        if next_difficulty != self.current_difficulty:
            self.current_difficulty = next_difficulty
            return True
        return False
    
    def generate_sequence_question(self, difficulty):
        """Generate a sequence completion question."""
        if difficulty == "easy":
            # Simple arithmetic sequence
            start = random.randint(1, 10)
            step = random.randint(1, 5)
            sequence = [start + i * step for i in range(5)]
            answer = start + 5 * step
        elif difficulty == "medium":
            # Fibonacci-like sequence
            a, b = random.randint(1, 5), random.randint(6, 10)
            sequence = [a, b]
            for i in range(3):
                sequence.append(sequence[-1] + sequence[-2])
            answer = sequence[-1] + sequence[-2]
        else:  # hard
            # Quadratic sequence
            start = random.randint(1, 5)
            sequence = [start + i**2 for i in range(5)]
            answer = start + 5**2
        
        # Generate options and ensure the correct answer is included
        options = self._generate_options(answer, difficulty)
        if answer not in options:
            # Replace a random option with the correct answer
            options[random.randint(0, len(options) - 1)] = answer
        
        return {
            "type": SEQUENCE_COMPLETION,
            "question": "What comes next in this sequence?",
            "sequence": sequence,
            "options": options,
            "answer": answer
        }
    
    def generate_odd_one_out_question(self, difficulty):
        """Generate an odd-one-out question."""
        if difficulty == "easy":
            # Simple shape or color difference
            categories = ["circle", "square", "triangle", "rectangle"]
            odd_category = random.choice(categories)
            categories.remove(odd_category)
            main_category = random.choice(categories)
            
            options = [main_category] * 3 + [odd_category]
            random.shuffle(options)
            answer = options.index(odd_category)
        elif difficulty == "medium":
            # Number properties (even/odd, prime/composite)
            even_numbers = [2, 4, 6, 8, 10]
            odd_numbers = [1, 3, 5, 7, 9]
            
            if random.choice([True, False]):
                options = random.sample(even_numbers, 3) + random.sample(odd_numbers, 1)
                answer = 3  # The odd number is the odd one out
            else:
                options = random.sample(odd_numbers, 3) + random.sample(even_numbers, 1)
                answer = 3  # The even number is the odd one out
            
            random.shuffle(options)
            answer = options.index(options[answer])
        else:  # hard
            # Complex pattern
            patterns = ["AB", "BC", "CD", "DE", "AC", "BD"]
            odd_pattern = random.choice(patterns)
            patterns.remove(odd_pattern)
            main_pattern = random.choice(patterns)
            
            options = [main_pattern] * 3 + [odd_pattern]
            random.shuffle(options)
            answer = options.index(odd_pattern)
        
        return {
            "type": ODD_ONE_OUT,
            "question": "Which one doesn't belong with the others?",
            "options": options,
            "answer": answer
        }
    
    def _generate_options(self, correct_answer, difficulty):
        """Generate multiple choice options including the correct answer."""
        options = [correct_answer]
        
        # Generate wrong options based on difficulty
        if difficulty == "easy":
            variance = 5
        elif difficulty == "medium":
            variance = 3
        else:  # hard
            variance = 2
        
        # Generate 3 wrong options
        attempts = 0
        while len(options) < 4 and attempts < 20:
            attempts += 1
            if random.choice([True, False]):
                wrong_answer = correct_answer + random.randint(1, variance)
            else:
                wrong_answer = correct_answer - random.randint(1, variance)
            
            if wrong_answer not in options:
                options.append(wrong_answer)
        
        # Fill remaining slots if needed
        while len(options) < 4:
            wrong_answer = correct_answer + random.randint(6, 10)
            if wrong_answer not in options:
                options.append(wrong_answer)
        
        # Shuffle the options
        random.shuffle(options)
        
        return options
    
    def generate_question(self, question_type=None, difficulty=None):
        """Generate a question of the specified type and difficulty."""
        if difficulty is None:
            difficulty = self.current_difficulty
        
        if question_type is None:
            question_type = random.choice([SEQUENCE_COMPLETION, NUMBER_PATTERN, ODD_ONE_OUT, GRID_DEDUCTION])
        
        if question_type == SEQUENCE_COMPLETION:
            self.current_question = self.generate_sequence_question(difficulty)
        elif question_type == ODD_ONE_OUT:
            self.current_question = self.generate_odd_one_out_question(difficulty)
        else:
            # Default to a pre-defined question if available
            self.current_question = self.get_random_question(difficulty)
        
        return self.current_question
