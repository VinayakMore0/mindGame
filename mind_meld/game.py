"""
Game module for Mind Meld game.
Contains the core game loop and logic.
"""
import pygame
import sys
import json
import os
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, GRAY, BLUE, GREEN, RED,
    GRID_SIZE, CELL_SIZE, GRID_MARGIN, GRID_OFFSET_X, GRID_OFFSET_Y,
    DISPLAY_TIME_BASE, DISPLAY_TIME_DECREMENT, MIN_DISPLAY_TIME, FLASH_DURATION,
    STARTING_PATTERN_LENGTH, MAX_PATTERN_LENGTH, SCORE_PER_CORRECT, BONUS_MULTIPLIER,
    SINGLE_PLAYER, TWO_PLAYER
)
from pattern_generator import PatternGenerator
from player_input import PlayerInput
from utils.helpers import draw_text, Timer, load_sound

class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mind Meld")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.title_font = pygame.font.SysFont('Arial', 48)
        self.info_font = pygame.font.SysFont('Arial', 24)
        self.score_font = pygame.font.SysFont('Arial', 36)
        
        # Load sounds
        try:
            self.success_sound = load_sound("success.wav")
            self.fail_sound = load_sound("fail.wav")
            self.click_sound = load_sound("click.wav")
        except:
            print("Sound files not found. Continuing without sound.")
            self.success_sound = None
            self.fail_sound = None
            self.click_sound = None
        
        # Game components
        self.pattern_generator = PatternGenerator()
        self.player_input = PlayerInput()
        self.timer = Timer()
        
        # Game state
        self.running = True
        self.game_state = "menu"  # menu, show_pattern, wait_input, game_over
        self.current_pattern = []
        self.current_level = 1
        self.pattern_length = STARTING_PATTERN_LENGTH
        self.display_time = DISPLAY_TIME_BASE
        self.scores = {1: 0, 2: 0}  # Player scores
        self.game_mode = SINGLE_PLAYER
        self.flashing_cell = None
        self.flash_timer = Timer()
    
    def start_game(self, mode):
        """Start a new game with the specified mode."""
        self.game_mode = mode
        self.current_level = 1
        self.pattern_length = STARTING_PATTERN_LENGTH
        self.display_time = DISPLAY_TIME_BASE
        self.scores = {1: 0, 2: 0}
        self.player_input.current_player = 1
        self.game_state = "show_pattern"
        self.generate_new_pattern()
    
    def generate_new_pattern(self):
        """Generate a new pattern for the current level."""
        pattern_type = "position"  # Can be expanded to other types
        self.current_pattern = self.pattern_generator.generate_pattern(
            pattern_type, self.pattern_length
        )
        
        # Debug info
        print(f"Generated pattern: {self.current_pattern}")
        
        self.timer.start(self.display_time)
        self.game_state = "show_pattern"
    
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
                    
                    elif self.game_state == "wait_input":
                        # Handle grid clicks during input phase
                        if self.player_input.is_input_enabled():
                            clicked_pos = self.player_input.handle_click(event.pos)
                            if clicked_pos:
                                if self.click_sound:
                                    self.click_sound.play()
                                self.flashing_cell = clicked_pos
                                self.flash_timer.start(FLASH_DURATION)
                                
                                # Check if player has input the full pattern
                                if len(self.player_input.get_player_pattern()) == len(self.current_pattern):
                                    self.check_pattern()
                    
                    elif self.game_state == "game_over":
                        # Return to menu on click after game over
                        self.game_state = "menu"
    
    def check_pattern(self):
        """Check if the player's pattern matches the target pattern."""
        player_pattern = self.player_input.get_player_pattern()
        
        # Debug info
        print(f"Player pattern: {player_pattern}")
        print(f"Target pattern: {self.current_pattern}")
        
        if self.player_input.check_pattern_match(self.current_pattern):
            # Pattern matched
            if self.success_sound:
                self.success_sound.play()
            
            # Calculate score
            time_bonus = 1.0
            if self.timer.running:
                remaining = self.timer.get_remaining()
                if remaining > 0:
                    time_bonus = min(BONUS_MULTIPLIER, 1.0 + (remaining / self.display_time))
            
            score_gain = int(SCORE_PER_CORRECT * self.pattern_length * time_bonus)
            current_player = self.player_input.get_current_player()
            self.scores[current_player] += score_gain
            
            # Handle player switching in two-player mode
            if self.game_mode == TWO_PLAYER:
                if self.player_input.get_current_player() == 2:
                    # Both players have gone, advance to next level
                    self.advance_level()
                else:
                    # Switch to player 2
                    self.player_input.switch_player()
                    self.game_state = "show_pattern"
                    self.generate_new_pattern()
            else:
                # Single player mode, advance to next level
                self.advance_level()
        else:
            # Pattern didn't match
            if self.fail_sound:
                self.fail_sound.play()
            self.game_state = "game_over"
    
    def advance_level(self):
        """Advance to the next level."""
        self.current_level += 1
        
        # Increase pattern length every 2 levels
        if self.current_level % 2 == 0 and self.pattern_length < MAX_PATTERN_LENGTH:
            self.pattern_length += 1
        
        # Decrease display time
        self.display_time = max(MIN_DISPLAY_TIME, 
                               DISPLAY_TIME_BASE - (self.current_level - 1) * DISPLAY_TIME_DECREMENT)
        
        # Generate new pattern
        self.generate_new_pattern()
    
    def update(self):
        """Update game state."""
        if self.game_state == "show_pattern":
            # Check if pattern display time is over
            if self.timer.check():
                self.game_state = "wait_input"
                self.player_input.enable_input()
                self.timer.start(self.display_time * 2)  # Double time for input
        
        elif self.game_state == "wait_input":
            # Check if input time is over
            if self.timer.check():
                if self.fail_sound:
                    self.fail_sound.play()
                self.game_state = "game_over"
        
        # Update flash timer
        if self.flash_timer.running:
            self.flash_timer.check()
    
    def render(self):
        """Render the game."""
        self.screen.fill(BLACK)
        
        if self.game_state == "menu":
            self.render_menu()
        elif self.game_state in ["show_pattern", "wait_input"]:
            self.render_game()
        elif self.game_state == "game_over":
            self.render_game_over()
        
        pygame.display.flip()
    
    def render_menu(self):
        """Render the main menu."""
        # Title
        draw_text(self.screen, "MIND MELD", self.title_font, WHITE, 
                 SCREEN_WIDTH // 2, 100, "center")
        
        # Game mode buttons
        button_width = 300
        button_height = 60
        button_y = 250
        
        # Single player button
        single_player_rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2, 
            button_y, 
            button_width, 
            button_height
        )
        pygame.draw.rect(self.screen, BLUE, single_player_rect)
        draw_text(self.screen, "Single Player", self.info_font, WHITE, 
                 SCREEN_WIDTH // 2, button_y + button_height // 2, "center")
        self.single_player_button = single_player_rect
        
        # Two player button
        two_player_rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2, 
            button_y + button_height + 30, 
            button_width, 
            button_height
        )
        pygame.draw.rect(self.screen, GREEN, two_player_rect)
        draw_text(self.screen, "Two Player", self.info_font, WHITE, 
                 SCREEN_WIDTH // 2, button_y + button_height + 30 + button_height // 2, "center")
        self.two_player_button = two_player_rect
        
        # Instructions
        instructions = [
            "Remember the pattern and recreate it!",
            "Each level gets harder with longer patterns and less time.",
            "Click to select grid cells in the correct order."
        ]
        
        for i, line in enumerate(instructions):
            draw_text(self.screen, line, self.info_font, GRAY, 
                     SCREEN_WIDTH // 2, 400 + i * 30, "center")
    
    def render_game(self):
        """Render the game screen."""
        # Draw header info
        current_player = self.player_input.get_current_player()
        
        # Level and player info
        level_text = f"Level: {self.current_level}"
        draw_text(self.screen, level_text, self.info_font, WHITE, 20, 20)
        
        if self.game_mode == TWO_PLAYER:
            player_text = f"Player {current_player}'s Turn"
            draw_text(self.screen, player_text, self.info_font, 
                     GREEN if current_player == 1 else BLUE, 
                     SCREEN_WIDTH // 2, 20, "center")
        
        # Scores
        score_text = f"Score: {self.scores[current_player]}"
        draw_text(self.screen, score_text, self.info_font, WHITE, 
                 SCREEN_WIDTH - 20, 20, "topright")
        
        # Draw timer if active
        if self.timer.running:
            remaining = self.timer.get_remaining() / 1000  # Convert to seconds
            timer_text = f"Time: {remaining:.1f}s"
            timer_color = GREEN if remaining > 3 else RED
            draw_text(self.screen, timer_text, self.info_font, timer_color, 
                     SCREEN_WIDTH // 2, 50, "center")
        
        # Draw game state info
        if self.game_state == "show_pattern":
            state_text = "Memorize the pattern!"
        else:
            state_text = "Recreate the pattern!"
        
        draw_text(self.screen, state_text, self.info_font, WHITE, 
                 SCREEN_WIDTH // 2, 80, "center")
        
        # Draw the grid
        self.render_grid()
    
    def render_grid(self):
        """Render the game grid."""
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(
                    GRID_OFFSET_X + x * (CELL_SIZE + GRID_MARGIN),
                    GRID_OFFSET_Y + y * (CELL_SIZE + GRID_MARGIN),
                    CELL_SIZE,
                    CELL_SIZE
                )
                
                # Default cell color
                cell_color = GRAY
                
                # Highlight cells in the pattern during show_pattern phase
                if self.game_state == "show_pattern":
                    if (x, y) in self.current_pattern:
                        index = self.current_pattern.index((x, y))
                        # Use different colors for sequential patterns
                        cell_color = GREEN
                
                # Highlight flashing cell
                if self.flashing_cell == (x, y) and not self.flash_timer.completed:
                    cell_color = BLUE
                
                pygame.draw.rect(self.screen, cell_color, rect)
                
                # Draw cell border
                pygame.draw.rect(self.screen, BLACK, rect, 2)
                
                # Draw sequence numbers during input phase
                if self.game_state == "wait_input":
                    player_pattern = self.player_input.get_player_pattern()
                    if (x, y) in player_pattern:
                        index = player_pattern.index((x, y))
                        # Add 1 to convert from 0-based to 1-based indexing for display
                        draw_text(self.screen, str(index + 1), self.info_font, BLACK,
                                 rect.centerx, rect.centery, "center")
                
                # Draw cell border
                pygame.draw.rect(self.screen, BLACK, rect, 2)
                
                # Draw sequence numbers during input phase
                if self.game_state == "wait_input":
                    player_pattern = self.player_input.get_player_pattern()
                    if (x, y) in player_pattern:
                        index = player_pattern.index((x, y)) + 1
                        draw_text(self.screen, str(index), self.info_font, BLACK,
                                 rect.centerx, rect.centery, "center")
    
    def render_game_over(self):
        """Render the game over screen."""
        # Game over text
        draw_text(self.screen, "GAME OVER", self.title_font, RED, 
                 SCREEN_WIDTH // 2, 150, "center")
        
        # Final scores
        if self.game_mode == SINGLE_PLAYER:
            score_text = f"Final Score: {self.scores[1]}"
            draw_text(self.screen, score_text, self.score_font, WHITE, 
                     SCREEN_WIDTH // 2, 250, "center")
            
            level_text = f"You reached Level {self.current_level}"
            draw_text(self.screen, level_text, self.info_font, WHITE, 
                     SCREEN_WIDTH // 2, 300, "center")
        else:
            # Two player mode
            if self.scores[1] > self.scores[2]:
                winner_text = "Player 1 Wins!"
                winner_color = GREEN
            elif self.scores[2] > self.scores[1]:
                winner_text = "Player 2 Wins!"
                winner_color = BLUE
            else:
                winner_text = "It's a Tie!"
                winner_color = WHITE
            
            draw_text(self.screen, winner_text, self.score_font, winner_color, 
                     SCREEN_WIDTH // 2, 250, "center")
            
            p1_score = f"Player 1: {self.scores[1]}"
            p2_score = f"Player 2: {self.scores[2]}"
            
            draw_text(self.screen, p1_score, self.info_font, GREEN, 
                     SCREEN_WIDTH // 2, 300, "center")
            draw_text(self.screen, p2_score, self.info_font, BLUE, 
                     SCREEN_WIDTH // 2, 330, "center")
        
        # Click to continue
        draw_text(self.screen, "Click anywhere to return to menu", self.info_font, GRAY, 
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
