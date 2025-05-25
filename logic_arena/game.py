"""
Game module for Logic Arena game.
Main game loop and scene controller.
"""
import pygame
import sys
import os
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, GRAY, LIGHT_GRAY, 
    BLUE, GREEN, RED, YELLOW, ORANGE,
    EASY_TIME_LIMIT, MEDIUM_TIME_LIMIT, HARD_TIME_LIMIT,
    EASY_SCORE, MEDIUM_SCORE, HARD_SCORE, TIME_BONUS_FACTOR,
    WRONG_ANSWER_PENALTY, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN,
    OPTION_BUTTON_WIDTH, OPTION_BUTTON_HEIGHT, SOLO_MODE, VERSUS_MODE
)
from question_manager import QuestionManager
from player_input import PlayerInput
from utils.helpers import draw_text, load_sound, Timer, format_time

class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Logic Arena")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.title_font = pygame.font.SysFont('Arial', 48)
        self.question_font = pygame.font.SysFont('Arial', 32)
        self.option_font = pygame.font.SysFont('Arial', 24)
        self.info_font = pygame.font.SysFont('Arial', 20)
        
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
        
        # Game components
        self.question_manager = QuestionManager()
        self.player_input = PlayerInput()
        self.timer = Timer()
        
        # Game state
        self.running = True
        self.game_state = "menu"  # menu, playing, game_over
        self.current_question = None
        self.scores = {1: 0, 2: 0}  # Player scores
        self.questions_answered = 0
        self.correct_answers = 0
        self.game_mode = SOLO_MODE
        self.feedback_message = ""
        self.feedback_color = WHITE
        self.feedback_timer = Timer()
    
    def start_game(self, mode):
        """Start a new game with the specified mode."""
        self.game_mode = mode
        self.scores = {1: 0, 2: 0}
        self.questions_answered = 0
        self.correct_answers = 0
        self.player_input.current_player = 1
        self.question_manager.set_difficulty("easy")
        self.game_state = "playing"
        self.load_next_question()
    
    def load_next_question(self):
        """Load the next question."""
        # Generate a new question
        self.current_question = self.question_manager.generate_question()
        
        if not self.current_question:
            print("Error: Failed to load question")
            self.game_state = "game_over"
            return
        
        # Debug info
        print(f"New question loaded: {self.current_question['question']}")
        print(f"Answer: {self.current_question['answer']}")
        
        # Set up option buttons
        self.setup_option_buttons()
        
        # Start the timer based on difficulty
        difficulty = self.question_manager.get_current_difficulty()
        if difficulty == "easy":
            time_limit = EASY_TIME_LIMIT
        elif difficulty == "medium":
            time_limit = MEDIUM_TIME_LIMIT
        else:  # hard
            time_limit = HARD_TIME_LIMIT
        
        self.timer.start(time_limit)
        self.player_input.enable_input()
    
    def setup_option_buttons(self):
        """Set up option buttons based on the current question."""
        if not self.current_question:
            return
        
        options = self.current_question.get("options", [])
        if not options:
            return
        
        # Calculate button positions
        num_options = len(options)
        total_width = num_options * OPTION_BUTTON_WIDTH + (num_options - 1) * BUTTON_MARGIN
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = SCREEN_HEIGHT - OPTION_BUTTON_HEIGHT - 50
        
        buttons = []
        for i in range(num_options):
            x = start_x + i * (OPTION_BUTTON_WIDTH + BUTTON_MARGIN)
            buttons.append(pygame.Rect(x, y, OPTION_BUTTON_WIDTH, OPTION_BUTTON_HEIGHT))
        
        self.player_input.set_option_buttons(buttons)
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.game_state == "menu":
                        # Check for menu button clicks
                        if self.solo_button.collidepoint(event.pos):
                            self.start_game(SOLO_MODE)
                        elif self.versus_button.collidepoint(event.pos):
                            self.start_game(VERSUS_MODE)
                    
                    elif self.game_state == "playing":
                        # Handle option selection
                        selected = self.player_input.handle_click(event.pos)
                        if selected is not None:
                            self.check_answer(selected)
                    
                    elif self.game_state == "game_over":
                        # Return to menu on click after game over
                        self.game_state = "menu"
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "playing":
                    # Handle keyboard input for options
                    selected = self.player_input.handle_keyboard_input(event.key)
                    if selected is not None:
                        self.check_answer(selected)
    
    def check_answer(self, selected_option):
        """Check if the selected answer is correct."""
        if not self.current_question:
            return
        
        options = self.current_question.get("options", [])
        if not options or selected_option >= len(options):
            return
        
        selected_answer = options[selected_option]
        
        # Debug info
        print(f"Selected option index: {selected_option}")
        print(f"Selected answer value: {selected_answer}")
        print(f"All options: {options}")
        
        is_correct = self.question_manager.check_answer(selected_answer)
        
        current_player = self.player_input.get_current_player()
        difficulty = self.question_manager.get_current_difficulty()
        
        if is_correct:
            # Correct answer
            if self.correct_sound:
                self.correct_sound.play()
            
            # Calculate score based on difficulty and time remaining
            if difficulty == "easy":
                score = EASY_SCORE
            elif difficulty == "medium":
                score = MEDIUM_SCORE
            else:  # hard
                score = HARD_SCORE
            
            # Add time bonus
            time_remaining = self.timer.get_remaining()
            time_bonus = int(time_remaining * TIME_BONUS_FACTOR)
            total_score = score + time_bonus
            
            self.scores[current_player] += total_score
            self.correct_answers += 1
            
            self.show_feedback(f"Correct! +{total_score} points", GREEN)
            
            # Increase difficulty every 3 correct answers
            if self.correct_answers % 3 == 0:
                self.question_manager.increase_difficulty()
        else:
            # Wrong answer
            if self.wrong_sound:
                self.wrong_sound.play()
            
            self.show_feedback("Wrong answer!", RED)
            
            # Apply time penalty in solo mode
            if self.game_mode == SOLO_MODE:
                remaining = self.timer.get_remaining()
                if remaining > WRONG_ANSWER_PENALTY:
                    # Restart timer with reduced time
                    self.timer.start(remaining - WRONG_ANSWER_PENALTY)
        
        self.questions_answered += 1
        
        # Handle player switching in versus mode
        if self.game_mode == VERSUS_MODE:
            self.player_input.switch_player()
        
        # Load next question
        self.load_next_question()
    
    def show_feedback(self, message, color):
        """Show feedback message for a short time."""
        self.feedback_message = message
        self.feedback_color = color
        self.feedback_timer.start(2)  # Show for 2 seconds
    
    def update(self):
        """Update game state."""
        if self.game_state == "playing":
            # Check if timer has expired
            if self.timer.is_expired():
                if self.wrong_sound:
                    self.wrong_sound.play()
                
                if self.game_mode == SOLO_MODE:
                    # Game over in solo mode when time runs out
                    self.game_state = "game_over"
                else:
                    # Switch players in versus mode
                    self.show_feedback("Time's up!", RED)
                    self.player_input.switch_player()
                    self.load_next_question()
            
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
        self.screen.fill(LIGHT_GRAY)
        
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
        draw_text(self.screen, "LOGIC ARENA", self.title_font, BLUE, 
                 SCREEN_WIDTH // 2, 100, "center")
        
        # Game mode buttons
        button_y = 250
        
        # Solo mode button
        solo_rect = pygame.Rect(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 
            button_y, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
        pygame.draw.rect(self.screen, GREEN, solo_rect)
        draw_text(self.screen, "Solo Mode", self.option_font, WHITE, 
                 SCREEN_WIDTH // 2, button_y + BUTTON_HEIGHT // 2, "center")
        self.solo_button = solo_rect
        
        # Versus mode button
        versus_rect = pygame.Rect(
            (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 
            button_y + BUTTON_HEIGHT + BUTTON_MARGIN, 
            BUTTON_WIDTH, 
            BUTTON_HEIGHT
        )
        pygame.draw.rect(self.screen, BLUE, versus_rect)
        draw_text(self.screen, "Versus Mode", self.option_font, WHITE, 
                 SCREEN_WIDTH // 2, button_y + BUTTON_HEIGHT + BUTTON_MARGIN + BUTTON_HEIGHT // 2, "center")
        self.versus_button = versus_rect
        
        # Instructions
        instructions = [
            "Solve logic puzzles to earn points!",
            "Each correct answer increases your score.",
            "Answer quickly for bonus points.",
            "The difficulty increases as you progress."
        ]
        
        for i, line in enumerate(instructions):
            draw_text(self.screen, line, self.info_font, BLACK, 
                     SCREEN_WIDTH // 2, 400 + i * 30, "center")
    
    def render_game(self):
        """Render the game screen."""
        # Draw header info
        current_player = self.player_input.get_current_player()
        difficulty = self.question_manager.get_current_difficulty()
        
        # Player info
        if self.game_mode == VERSUS_MODE:
            player_text = f"Player {current_player}'s Turn"
            player_color = GREEN if current_player == 1 else BLUE
            draw_text(self.screen, player_text, self.option_font, player_color, 
                     SCREEN_WIDTH // 2, 20, "center")
        
        # Difficulty
        diff_text = f"Difficulty: {difficulty.capitalize()}"
        draw_text(self.screen, diff_text, self.info_font, BLACK, 20, 20)
        
        # Score
        score_text = f"Score: {self.scores[current_player]}"
        draw_text(self.screen, score_text, self.info_font, BLACK, 
                 SCREEN_WIDTH - 20, 20, "topright")
        
        # Timer
        remaining = self.timer.get_remaining()
        timer_text = f"Time: {int(remaining)}"
        timer_color = GREEN if remaining > 10 else ORANGE if remaining > 5 else RED
        draw_text(self.screen, timer_text, self.option_font, timer_color, 
                 SCREEN_WIDTH // 2, 50, "center")
        
        # Timer bar
        max_time = EASY_TIME_LIMIT
        if difficulty == "medium":
            max_time = MEDIUM_TIME_LIMIT
        elif difficulty == "hard":
            max_time = HARD_TIME_LIMIT
        
        bar_width = SCREEN_WIDTH - 100
        bar_height = 20
        bar_x = 50
        bar_y = 80
        
        # Background bar
        pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Fill bar based on remaining time
        fill_width = int(bar_width * (remaining / max_time))
        fill_color = GREEN if remaining > 10 else ORANGE if remaining > 5 else RED
        pygame.draw.rect(self.screen, fill_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Draw question
        if self.current_question:
            question_text = self.current_question.get("question", "")
            draw_text(self.screen, question_text, self.question_font, BLACK, 
                     SCREEN_WIDTH // 2, 150, "center")
            
            # Draw sequence if available
            sequence = self.current_question.get("sequence", [])
            if sequence:
                sequence_text = " → ".join(str(num) for num in sequence) + " → ?"
                draw_text(self.screen, sequence_text, self.question_font, BLUE, 
                         SCREEN_WIDTH // 2, 200, "center")
            
            # Draw options
            options = self.current_question.get("options", [])
            option_buttons = self.player_input.option_buttons
            
            for i, (option, button) in enumerate(zip(options, option_buttons)):
                # Draw button background
                selected = self.player_input.get_selected_option()
                if selected == i:
                    pygame.draw.rect(self.screen, BLUE, button)
                else:
                    pygame.draw.rect(self.screen, WHITE, button)
                
                # Draw button border
                pygame.draw.rect(self.screen, BLACK, button, 2)
                
                # Draw option text
                option_text = str(option)
                draw_text(self.screen, option_text, self.option_font, BLACK, 
                         button.centerx, button.centery, "center")
                
                # Draw option number
                number_text = f"{i + 1}"
                draw_text(self.screen, number_text, self.info_font, BLACK, 
                         button.x + 10, button.y + 10)
                
                # If this is the correct answer, add a subtle indicator in debug mode
                if __debug__:
                    if option == self.current_question.get("answer"):
                        pygame.draw.circle(self.screen, (200, 200, 200), 
                                          (button.x + button.width - 10, button.y + 10), 5)
        
        # Draw feedback message
        if self.feedback_message:
            draw_text(self.screen, self.feedback_message, self.option_font, self.feedback_color, 
                     SCREEN_WIDTH // 2, 350, "center")
    
    def render_game_over(self):
        """Render the game over screen."""
        # Game over text
        draw_text(self.screen, "GAME OVER", self.title_font, RED, 
                 SCREEN_WIDTH // 2, 100, "center")
        
        # Final scores
        if self.game_mode == SOLO_MODE:
            score_text = f"Final Score: {self.scores[1]}"
            draw_text(self.screen, score_text, self.question_font, BLUE, 
                     SCREEN_WIDTH // 2, 200, "center")
            
            stats_text = f"Questions Answered: {self.questions_answered}"
            draw_text(self.screen, stats_text, self.option_font, BLACK, 
                     SCREEN_WIDTH // 2, 250, "center")
            
            correct_text = f"Correct Answers: {self.correct_answers}"
            draw_text(self.screen, correct_text, self.option_font, GREEN, 
                     SCREEN_WIDTH // 2, 290, "center")
            
            accuracy = 0 if self.questions_answered == 0 else (self.correct_answers / self.questions_answered) * 100
            accuracy_text = f"Accuracy: {accuracy:.1f}%"
            draw_text(self.screen, accuracy_text, self.option_font, BLUE, 
                     SCREEN_WIDTH // 2, 330, "center")
        else:
            # Versus mode
            if self.scores[1] > self.scores[2]:
                winner_text = "Player 1 Wins!"
                winner_color = GREEN
            elif self.scores[2] > self.scores[1]:
                winner_text = "Player 2 Wins!"
                winner_color = BLUE
            else:
                winner_text = "It's a Tie!"
                winner_color = BLACK
            
            draw_text(self.screen, winner_text, self.question_font, winner_color, 
                     SCREEN_WIDTH // 2, 200, "center")
            
            p1_score = f"Player 1: {self.scores[1]} points"
            p2_score = f"Player 2: {self.scores[2]} points"
            
            draw_text(self.screen, p1_score, self.option_font, GREEN, 
                     SCREEN_WIDTH // 2, 250, "center")
            draw_text(self.screen, p2_score, self.option_font, BLUE, 
                     SCREEN_WIDTH // 2, 290, "center")
        
        # Click to continue
        draw_text(self.screen, "Click anywhere to return to menu", self.info_font, BLACK, 
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
