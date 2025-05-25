"""
Game Logic module for Cipher Clash.
Handles the core gameplay mechanics, scoring, and game state.
"""
import time
import pygame
from mind_games_project.games.cipher_clash.config import DIFFICULTY_LEVELS, CIPHER_TYPES
from mind_games_project.games.cipher_clash.game_engine.question_generator import QuestionGenerator

class GameState:
    """Manages the game state for Cipher Clash."""
    
    def __init__(self):
        """Initialize the game state."""
        # Game settings
        self.difficulty = "medium"
        self.selected_cipher_type = None  # None means random
        self.game_mode = "solo"  # 'solo' or 'versus'
        
        # Game progress
        self.current_question = None
        self.questions_answered = 0
        self.correct_answers = 0
        self.total_score = 0
        self.current_input = ""
        self.game_active = False
        self.game_over = False
        
        # Timer
        self.start_time = 0
        self.elapsed_time = 0
        self.time_limit = DIFFICULTY_LEVELS["medium"]["time_limit"]
        
        # Hints
        self.hints_available = DIFFICULTY_LEVELS["medium"]["hint_count"]
        self.hint_revealed = False
        
        # Sound effects and music
        self.sounds = {}
        self.music_tracks = {}
        self.current_music = None
        
        # Question generator
        self.question_generator = QuestionGenerator()
    
    def start_game(self, difficulty, cipher_type=None):
        """
        Start a new game.
        
        Args:
            difficulty (str): The difficulty level
            cipher_type (str, optional): The specific cipher type to use
        """
        # Update game settings
        self.difficulty = difficulty
        self.selected_cipher_type = cipher_type
        
        # Reset game progress
        self.questions_answered = 0
        self.correct_answers = 0
        self.total_score = 0
        self.current_input = ""
        self.game_active = True
        self.game_over = False
        
        # Reset timer
        self.time_limit = DIFFICULTY_LEVELS[difficulty]["time_limit"]
        self.start_time = time.time()
        self.elapsed_time = 0
        
        # Reset hints
        self.hints_available = DIFFICULTY_LEVELS[difficulty]["hint_count"]
        self.hint_revealed = False
        
        # Generate first question
        self.generate_new_question()
        
        # Play game music
        self.play_music("gameplay_calm")
    
    def generate_new_question(self):
        """Generate a new cipher question."""
        self.current_question = self.question_generator.generate_question(
            self.difficulty, self.selected_cipher_type
        )
        self.current_input = ""
        self.hint_revealed = False
    
    def update_timer(self):
        """Update the elapsed time and check for time limit."""
        if self.game_active and not self.game_over:
            self.elapsed_time = time.time() - self.start_time
            
            # Check if time is running out (last 10 seconds)
            if self.time_limit - self.elapsed_time <= 10:
                # Switch to intense music if not already playing
                if self.current_music != "gameplay_intense":
                    self.play_music("gameplay_intense")
            
            # Check if time is up
            if self.elapsed_time >= self.time_limit:
                self.end_game()
    
    def submit_answer(self, answer):
        """
        Submit an answer and check if it's correct.
        
        Args:
            answer (str): The user's answer
            
        Returns:
            bool: True if the answer is correct
        """
        if not self.game_active or self.game_over:
            return False
        
        is_correct, score = self.question_generator.verify_answer(self.current_question, answer)
        
        # Play sound effect
        if is_correct:
            self.play_sound("correct")
        else:
            self.play_sound("wrong")
        
        # Update game progress
        self.questions_answered += 1
        if is_correct:
            self.correct_answers += 1
            self.total_score += score
            
            # Generate a new question
            self.generate_new_question()
        
        return is_correct
    
    def use_hint(self):
        """
        Use a hint if available.
        
        Returns:
            str: The hint text, or None if no hints are available
        """
        if self.hints_available > 0 and not self.hint_revealed:
            self.hints_available -= 1
            self.hint_revealed = True
            self.play_sound("menu_click")
            return self.current_question["hint"]
        return None
    
    def end_game(self):
        """End the current game."""
        self.game_active = False
        self.game_over = True
        self.play_sound("game_over")
        self.play_music("victory")
    
    def get_time_remaining(self):
        """
        Get the remaining time in seconds.
        
        Returns:
            float: The remaining time in seconds
        """
        return max(0, self.time_limit - self.elapsed_time)
    
    def get_time_remaining_formatted(self):
        """
        Get the remaining time formatted as MM:SS.
        
        Returns:
            str: The formatted time string
        """
        remaining = self.get_time_remaining()
        minutes = int(remaining) // 60
        seconds = int(remaining) % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_progress_percentage(self):
        """
        Get the progress as a percentage of time elapsed.
        
        Returns:
            float: The progress percentage (0.0 to 1.0)
        """
        if self.time_limit == 0:
            return 1.0
        return min(1.0, self.elapsed_time / self.time_limit)
    
    def get_results(self):
        """
        Get the game results.
        
        Returns:
            dict: The game results
        """
        return {
            "total_score": self.total_score,
            "questions_answered": self.questions_answered,
            "correct_answers": self.correct_answers,
            "accuracy": self.correct_answers / max(1, self.questions_answered),
            "time_taken": self.elapsed_time,
            "difficulty": self.difficulty
        }
    
    def play_sound(self, sound_name):
        """
        Play a sound effect.
        
        Args:
            sound_name (str): The name of the sound to play
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, track_name):
        """
        Play a music track.
        
        Args:
            track_name (str): The name of the track to play
        """
        if track_name in self.music_tracks:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.music_tracks[track_name])
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.current_music = track_name
