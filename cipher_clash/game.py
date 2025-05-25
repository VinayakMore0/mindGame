"""
Game module for Cipher Clash game.
Game loop and state manager.
"""
import pygame
import sys
import os
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, GRAY, DARK_GRAY, 
    MATRIX_GREEN, NEON_BLUE, NEON_PINK, RED, YELLOW,
    EASY_TIME_LIMIT, MEDIUM_TIME_LIMIT, HARD_TIME_LIMIT,
    BASE_SCORE, TIME_BONUS_FACTOR, STREAK_BONUS, MAX_STREAK_BONUS,
    MAX_ATTEMPTS, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
    SINGLE_PLAYER, TWO_PLAYER, DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD
)
from cipher_engine import CipherEngine
from player_input import PlayerInput
from utils.helpers import draw_text, load_image, load_sound, Timer, format_time

class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cipher Clash")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.title_font = pygame.font.SysFont('Arial', 48)
        self.cipher_font = pygame.font.SysFont('Courier New', 36)  # Monospace font for ciphers
        self.input_font = pygame.font.SysFont('Arial', 24)
        self.info_font = pygame.font.SysFont('Arial', 20)
        
        # Try to load custom font if available
        try:
            techno_font_path = os.path.join("assets", "fonts", "techno.ttf")
            if os.path.exists(techno_font_path):
                self.cipher_font = pygame.font.Font(techno_font_path, 36)
        except:
            print("Custom font not loaded, using system font")
        
        # Load sounds
        try:
            self.correct_sound = load_sound("correct.wav")
            self.wrong_sound = load_sound("wrong.wav")
            self.tick_sound = load_sound("tick.wav")
        except:
            print("Sound files not found. Continuing without sound.")
            self.correct_sound = None
            self.wrong_sound = None
            self.tick_sound = None
        
        # Load images
        try:
            self.bg_image = load_image("bg.jpg")
            self.key_image = load_image("key.png")
            self.timer_image = load_image("timer.png")
        except:
            print("Image files not found. Continuing without images.")
            self.bg_image = None
            self.key_image = None
            self.timer_image = None
        
        # Game components
        self.cipher_engine = CipherEngine()
        self.player_input = PlayerInput()
        self.timer = Timer()
        
        # Game state
        self.running = True
        self.game_state = "menu"  # menu, playing, game_over
        self.current_cipher = None
        self.scores = {1: 0, 2: 0}  # Player scores
        self.ciphers_solved = 0
        self.streak = 0
        self.attempts = 0
        self.game_mode = SINGLE_PLAYER
        self.current_difficulty = DIFFICULTY_EASY
        self.feedback_message = ""
        self.feedback_color = WHITE
        self.feedback_timer = Timer()
        
        # Set up input box
        input_box_x = (SCREEN_WIDTH - INPUT_BOX_WIDTH) // 2
        input_box_y = SCREEN_HEIGHT - 150
        self.input_box_rect = pygame.Rect(input_box_x, input_box_y, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)
        self.player_input.set_input_rect(self.input_box_rect)
    
    def start_game(self, mode):
        """Start a new game with the specified mode."""
        self.game_mode = mode
        self.scores = {1: 0, 2: 0}
        self.ciphers_solved = 0
        self.streak = 0
        self.attempts = 0
        self.player_input.current_player = 1
        self.current_difficulty = DIFFICULTY_EASY
        self.game_state = "playing"
        self.load_next_cipher()
    
    def load_next_cipher(self):
        """Load the next cipher."""
        # Determine difficulty based on ciphers solved
        if self.ciphers_solved >= 10:
            self.current_difficulty = DIFFICULTY_HARD
        elif self.ciphers_solved >= 5:
            self.current_difficulty = DIFFICULTY_MEDIUM
        else:
            self.current_difficulty = DIFFICULTY_EASY
        
        # Generate a new cipher
        self.current_cipher = self.cipher_engine.generate_cipher(self.current_difficulty)
        
        if not self.current_cipher:
            print("Error: Failed to generate cipher")
            self.game_state = "game_over"
            return
        
        # Reset attempts
        self.attempts = 0
        
        # Start the timer based on difficulty
        if self.current_difficulty == DIFFICULTY_EASY:
            time_limit = EASY_TIME_LIMIT
        elif self.current_difficulty == DIFFICULTY_MEDIUM:
            time_limit = MEDIUM_TIME_LIMIT
        else:  # DIFFICULTY_HARD
            time_limit = HARD_TIME_LIMIT
        
        self.timer.start(time_limit)
        self.player_input.enable_input()
        self.player_input.clear_input()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.game_state == "menu":
                        # Check for menu button clicks
                        if self.single_player_button.collidepoint(event.pos):
                            self.start_game(SINGLE_PLAYER)
                        elif self.two_player_button.collidepoint(event.pos):
                            self.start_game(TWO_PLAYER)
                    
                    elif self.game_state == "playing":
                        # Handle input box click
                        self.player_input.handle_click(event.pos)
                        
                        # Check for hint button click
                        if self.hint_button.collidepoint(event.pos):
                            self.show_hint()
                    
                    elif self.game_state == "game_over":
                        # Return to menu on click after game over
                        self.game_state = "menu"
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "playing":
                    # Handle text input
                    result = self.player_input.handle_key_event(event)
                    if result is not None:  # Enter key was pressed
                        self.check_answer(result)
    
    def check_answer(self, answer):
        """Check if the provided answer is correct."""
        if not self.current_cipher:
            return
        
        is_correct = self.cipher_engine.check_answer(answer)
        current_player = self.player_input.get_current_player()
        
        if is_correct:
            # Correct answer
            if self.correct_sound:
                self.correct_sound.play()
            
            # Calculate score based on difficulty and time remaining
            if self.current_difficulty == DIFFICULTY_EASY:
                score = BASE_SCORE
            elif self.current_difficulty == DIFFICULTY_MEDIUM:
                score = BASE_SCORE * 2
            else:  # DIFFICULTY_HARD
                score = BASE_SCORE * 3
            
            # Add time bonus
            time_remaining = self.timer.get_remaining()
            time_bonus = int(time_remaining * TIME_BONUS_FACTOR)
            
            # Add streak bonus
            self.streak += 1
            streak_bonus = min(STREAK_BONUS * self.streak, MAX_STREAK_BONUS)
            
            total_score = score + time_bonus + streak_bonus
            self.scores[current_player] += total_score
            self.ciphers_solved += 1
            
            self.show_feedback(f"Correct! +{total_score} points", MATRIX_GREEN)
            
            # Handle player switching in versus mode
            if self.game_mode == TWO_PLAYER:
                self.player_input.switch_player()
            
            # Load next cipher
            self.load_next_cipher()
        else:
            # Wrong answer
            if self.wrong_sound:
                self.wrong_sound.play()
            
            self.attempts += 1
            self.streak = 0  # Reset streak on wrong answer
            
            if self.attempts >= MAX_ATTEMPTS:
                # Failed after max attempts
                self.show_feedback(f"Wrong! The answer was: {self.cipher_engine.current_word}", RED)
                
                # Handle player switching in versus mode
                if self.game_mode == TWO_PLAYER:
                    self.player_input.switch_player()
                
                # Load next cipher
                self.load_next_cipher()
            else:
                # Still have attempts left
                remaining = MAX_ATTEMPTS - self.attempts
                self.show_feedback(f"Wrong! {remaining} attempts left", YELLOW)
                self.player_input.clear_input()
    
    def show_hint(self):
        """Show a hint for the current cipher."""
        if not self.current_cipher:
            return
        
        hint = self.cipher_engine.get_hint()
        self.show_feedback(f"Hint: {hint}", NEON_BLUE)
    
    def show_feedback(self, message, color):
        """Show feedback message for a short time."""
        self.feedback_message = message
        self.feedback_color = color
        self.feedback_timer.start(3)  # Show for 3 seconds
    
    def update(self):
        """Update game state."""
        if self.game_state == "playing":
            # Check if timer has expired
            if self.timer.is_expired():
                if self.wrong_sound:
                    self.wrong_sound.play()
                
                self.show_feedback(f"Time's up! The answer was: {self.cipher_engine.current_word}", RED)
                self.streak = 0  # Reset streak when time expires
                
                if self.game_mode == SINGLE_PLAYER:
                    # In single player, check if we've reached game over condition
                    if self.ciphers_solved == 0:
                        self.game_state = "game_over"
                    else:
                        # Load next cipher
                        self.load_next_cipher()
                else:
                    # In versus mode, switch players
                    self.player_input.switch_player()
                    self.load_next_cipher()
            
            # Play tick sound when time is running low
            remaining = self.timer.get_remaining()
            if remaining <= 5 and remaining > 0 and int(remaining) != int(remaining + 0.1):
                if self.tick_sound:
                    self.tick_sound.play()
        
        # Update feedback timer
        if self.feedback_timer.get_remaining() <= 0:
            self.feedback_message = ""
    
    def render(self):
        """Render the game."""
        # Draw background
        if self.bg_image:
            # Scale background to fit screen
            scaled_bg = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill(DARK_GRAY)
        
        if self.game_state == "menu":
            self.render_menu()
        elif self.game_state == "playing":
            self.render_game()
        elif self.game_state == "game_over":
            self.render_game_over()
        
        pygame.display.flip()
    
    def render_menu(self):
        """Render the main menu."""
        # Title
        draw_text(self.screen, "CIPHER CLASH", self.title_font, MATRIX_GREEN, 
                 SCREEN_WIDTH // 2, 100, "center")
        
        # Game mode buttons
        button_y = 250
        
        # Single player button
        single_player_rect = pygame.Rect(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 
            button_y, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
        pygame.draw.rect(self.screen, NEON_BLUE, single_player_rect)
        draw_text(self.screen, "Single Player", self.input_font, WHITE, 
                 SCREEN_WIDTH // 2, button_y + BUTTON_HEIGHT // 2, "center")
        self.single_player_button = single_player_rect
        
        # Two player button
        two_player_rect = pygame.Rect(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 
            button_y + BUTTON_HEIGHT + 20, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
        pygame.draw.rect(self.screen, NEON_PINK, two_player_rect)
        draw_text(self.screen, "Two Player", self.input_font, WHITE, 
                 SCREEN_WIDTH // 2, button_y + BUTTON_HEIGHT + 20 + BUTTON_HEIGHT // 2, "center")
        self.two_player_button = two_player_rect
        
        # Instructions
        instructions = [
            "Decode ciphers to earn points!",
            "Type your answer and press Enter.",
            "Solve quickly for bonus points.",
            "The difficulty increases as you progress."
        ]
        
        for i, line in enumerate(instructions):
            draw_text(self.screen, line, self.info_font, WHITE, 
                     SCREEN_WIDTH // 2, 400 + i * 30, "center")
    
    def render_game(self):
        """Render the game screen."""
        # Draw header info
        current_player = self.player_input.get_current_player()
        
        # Player info for two-player mode
        if self.game_mode == TWO_PLAYER:
            player_text = f"Player {current_player}'s Turn"
            player_color = NEON_BLUE if current_player == 1 else NEON_PINK
            draw_text(self.screen, player_text, self.input_font, player_color, 
                     SCREEN_WIDTH // 2, 20, "center")
        
        # Difficulty
        diff_text = f"Difficulty: {self.current_difficulty.capitalize()}"
        draw_text(self.screen, diff_text, self.info_font, WHITE, 20, 20)
        
        # Score
        score_text = f"Score: {self.scores[current_player]}"
        draw_text(self.screen, score_text, self.info_font, WHITE, 
                 SCREEN_WIDTH - 20, 20, "topright")
        
        # Ciphers solved
        solved_text = f"Ciphers: {self.ciphers_solved}"
        draw_text(self.screen, solved_text, self.info_font, WHITE, 20, 50)
        
        # Streak
        if self.streak > 0:
            streak_text = f"Streak: {self.streak}"
            draw_text(self.screen, streak_text, self.info_font, MATRIX_GREEN, 
                     SCREEN_WIDTH - 20, 50, "topright")
        
        # Timer
        remaining = self.timer.get_remaining()
        timer_text = format_time(int(remaining))
        timer_color = WHITE if remaining > 10 else YELLOW if remaining > 5 else RED
        draw_text(self.screen, timer_text, self.input_font, timer_color, 
                 SCREEN_WIDTH // 2, 50, "center")
        
        # Timer bar
        max_time = EASY_TIME_LIMIT
        if self.current_difficulty == DIFFICULTY_MEDIUM:
            max_time = MEDIUM_TIME_LIMIT
        elif self.current_difficulty == DIFFICULTY_HARD:
            max_time = HARD_TIME_LIMIT
        
        bar_width = SCREEN_WIDTH - 100
        bar_height = 10
        bar_x = 50
        bar_y = 80
        
        # Background bar
        pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Fill bar based on remaining time
        fill_width = int(bar_width * (remaining / max_time))
        fill_color = MATRIX_GREEN if remaining > 10 else YELLOW if remaining > 5 else RED
        pygame.draw.rect(self.screen, fill_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Draw cipher
        if self.current_cipher:
            # Cipher type
            type_text = f"Cipher Type: {self.current_cipher['type'].capitalize()}"
            draw_text(self.screen, type_text, self.info_font, WHITE, 
                     SCREEN_WIDTH // 2, 120, "center")
            
            # Cipher text
            cipher_text = self.current_cipher["cipher_text"]
            draw_text(self.screen, cipher_text, self.cipher_font, MATRIX_GREEN, 
                     SCREEN_WIDTH // 2, 200, "center")
            
            # Attempts remaining
            attempts_text = f"Attempts: {MAX_ATTEMPTS - self.attempts}/{MAX_ATTEMPTS}"
            draw_text(self.screen, attempts_text, self.info_font, WHITE, 
                     SCREEN_WIDTH // 2, 250, "center")
        
        # Draw input box
        self.player_input.render(self.screen, self.input_font, WHITE, MATRIX_GREEN, GRAY)
        
        # Draw hint button
        hint_button_width = 100
        hint_button_height = 40
        hint_button_x = (SCREEN_WIDTH - hint_button_width) // 2
        hint_button_y = SCREEN_HEIGHT - 80
        
        self.hint_button = pygame.Rect(hint_button_x, hint_button_y, hint_button_width, hint_button_height)
        pygame.draw.rect(self.screen, NEON_BLUE, self.hint_button)
        draw_text(self.screen, "Hint", self.info_font, WHITE, 
                 hint_button_x + hint_button_width // 2, hint_button_y + hint_button_height // 2, "center")
        
        # Draw feedback message
        if self.feedback_message:
            draw_text(self.screen, self.feedback_message, self.input_font, self.feedback_color, 
                     SCREEN_WIDTH // 2, 300, "center")
    
    def render_game_over(self):
        """Render the game over screen."""
        # Game over text
        draw_text(self.screen, "GAME OVER", self.title_font, RED, 
                 SCREEN_WIDTH // 2, 100, "center")
        
        # Final scores
        if self.game_mode == SINGLE_PLAYER:
            score_text = f"Final Score: {self.scores[1]}"
            draw_text(self.screen, score_text, self.cipher_font, MATRIX_GREEN, 
                     SCREEN_WIDTH // 2, 200, "center")
            
            stats_text = f"Ciphers Solved: {self.ciphers_solved}"
            draw_text(self.screen, stats_text, self.input_font, WHITE, 
                     SCREEN_WIDTH // 2, 250, "center")
        else:
            # Two player mode
            if self.scores[1] > self.scores[2]:
                winner_text = "Player 1 Wins!"
                winner_color = NEON_BLUE
            elif self.scores[2] > self.scores[1]:
                winner_text = "Player 2 Wins!"
                winner_color = NEON_PINK
            else:
                winner_text = "It's a Tie!"
                winner_color = WHITE
            
            draw_text(self.screen, winner_text, self.cipher_font, winner_color, 
                     SCREEN_WIDTH // 2, 200, "center")
            
            p1_score = f"Player 1: {self.scores[1]} points"
            p2_score = f"Player 2: {self.scores[2]} points"
            
            draw_text(self.screen, p1_score, self.input_font, NEON_BLUE, 
                     SCREEN_WIDTH // 2, 250, "center")
            draw_text(self.screen, p2_score, self.input_font, NEON_PINK, 
                     SCREEN_WIDTH // 2, 290, "center")
        
        # Click to continue
        draw_text(self.screen, "Click anywhere to return to menu", self.info_font, WHITE, 
                 SCREEN_WIDTH // 2, 400, "center")
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
