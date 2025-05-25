"""
Screens module for Cipher Clash.
Contains the different game screens (menu, game, results).
"""
import pygame
from pygame.locals import *
import os
import time

from mind_games_project.games.cipher_clash.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GameColors, CIPHER_TYPES,
    DIFFICULTY_LEVELS, FONT_SIZE_SMALL, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE,
    FONT_SIZE_TITLE
)
from mind_games_project.games.cipher_clash.ui.layout import (
    Button, InputBox, TerminalBox, ProgressBar, draw_text, draw_title
)

# Fallback definition in case import fails
if 'FONT_SIZE_TITLE' not in globals():
    FONT_SIZE_TITLE = 72

class BaseScreen:
    """Base class for all game screens."""
    
    def __init__(self, surface, game_state):
        """
        Initialize the base screen.
        
        Args:
            surface: The pygame surface to draw on
            game_state: The game state object
        """
        self.surface = surface
        self.game_state = game_state
        self.next_screen = None
    
    def handle_event(self, event):
        """
        Handle pygame events.
        
        Args:
            event: The pygame event
        """
        pass
    
    def update(self):
        """
        Update the screen state.
        
        Returns:
            str or None: The next screen to switch to, or None
        """
        result = self.next_screen
        self.next_screen = None
        return result
    
    def draw(self):
        """Draw the screen."""
        # Clear the screen
        self.surface.fill(GameColors.BACKGROUND)

class MenuScreen(BaseScreen):
    """Menu screen for Cipher Clash."""
    
    def __init__(self, surface, game_state):
        """Initialize the menu screen."""
        super().__init__(surface, game_state)
        
        # Create buttons
        button_width = 250
        button_height = 60
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 50
        
        self.buttons = [
            Button(
                (SCREEN_WIDTH // 2 - button_width // 2, start_y),
                (button_width, button_height),
                "Play Solo",
                self._start_solo_game
            ),
            Button(
                (SCREEN_WIDTH // 2 - button_width // 2, start_y + button_height + button_spacing),
                (button_width, button_height),
                "1v1 Battle",
                self._start_versus_game
            ),
            Button(
                (SCREEN_WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing)),
                (button_width, button_height),
                "How to Play",
                self._show_tutorial
            ),
            Button(
                (SCREEN_WIDTH // 2 - button_width // 2, start_y + 3 * (button_height + button_spacing)),
                (button_width, button_height),
                "Exit",
                self._exit_game
            )
        ]
        
        # Difficulty selector
        self.difficulty_buttons = [
            Button(
                (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT - 100),
                (100, 40),
                "Easy",
                lambda: self._set_difficulty("easy"),
                color=GameColors.BUTTON_NORMAL if game_state.difficulty != "easy" else GameColors.NEON_GREEN
            ),
            Button(
                (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100),
                (100, 40),
                "Medium",
                lambda: self._set_difficulty("medium"),
                color=GameColors.BUTTON_NORMAL if game_state.difficulty != "medium" else GameColors.NEON_GREEN
            ),
            Button(
                (SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT - 100),
                (100, 40),
                "Hard",
                lambda: self._set_difficulty("hard"),
                color=GameColors.BUTTON_NORMAL if game_state.difficulty != "hard" else GameColors.NEON_GREEN
            )
        ]
        
        # Cipher type selector
        self.cipher_buttons = []
        cipher_x = 100
        cipher_y = SCREEN_HEIGHT - 180
        for cipher_id, cipher_info in CIPHER_TYPES.items():
            self.cipher_buttons.append(
                Button(
                    (cipher_x, cipher_y),
                    (120, 40),
                    cipher_info["name"],
                    lambda c=cipher_id: self._set_cipher_type(c),
                    color=GameColors.BUTTON_NORMAL,
                    font_size=FONT_SIZE_SMALL
                )
            )
            cipher_x += 140
            if cipher_x > SCREEN_WIDTH - 100:
                cipher_x = 100
                cipher_y += 50
        
        # Add "Random" cipher option
        self.cipher_buttons.append(
            Button(
                (cipher_x, cipher_y),
                (120, 40),
                "Random",
                lambda: self._set_cipher_type(None),
                color=GameColors.NEON_PURPLE,
                font_size=FONT_SIZE_SMALL
            )
        )
        
        # Title animation timer
        self.title_timer = 0
        
        # Play menu music
        self.game_state.play_music("menu")
    
    def _start_solo_game(self):
        """Start a solo game."""
        self.game_state.game_mode = "solo"
        self.game_state.start_game(self.game_state.difficulty, self.game_state.selected_cipher_type)
        self.next_screen = "game"
        self.game_state.play_sound("menu_click")
    
    def _start_versus_game(self):
        """Start a versus game."""
        self.game_state.game_mode = "versus"
        self.game_state.start_game(self.game_state.difficulty, self.game_state.selected_cipher_type)
        self.next_screen = "game"
        self.game_state.play_sound("menu_click")
    
    def _show_tutorial(self):
        """Show the tutorial."""
        # For now, just print to console
        print("Tutorial would be shown here")
        self.game_state.play_sound("menu_click")
    
    def _exit_game(self):
        """Exit the game."""
        pygame.quit()
        exit()
    
    def _set_difficulty(self, difficulty):
        """Set the game difficulty."""
        self.game_state.difficulty = difficulty
        
        # Update button colors
        for button in self.difficulty_buttons:
            if button.text.lower() == difficulty:
                button.color = GameColors.NEON_GREEN
            else:
                button.color = GameColors.BUTTON_NORMAL
        
        self.game_state.play_sound("menu_click")
    
    def _set_cipher_type(self, cipher_type):
        """Set the cipher type."""
        self.game_state.selected_cipher_type = cipher_type
        
        # Update button colors
        for button in self.cipher_buttons:
            if (cipher_type is None and button.text == "Random") or \
               (cipher_type is not None and button.text == CIPHER_TYPES.get(cipher_type, {}).get("name")):
                button.color = GameColors.NEON_PURPLE
            else:
                button.color = GameColors.BUTTON_NORMAL
        
        self.game_state.play_sound("menu_click")
    
    def handle_event(self, event):
        """Handle pygame events."""
        # Pass events to buttons
        events = [event]
        for button in self.buttons:
            button.update(events)
        
        for button in self.difficulty_buttons:
            button.update(events)
        
        for button in self.cipher_buttons:
            button.update(events)
    
    def update(self):
        """Update the menu screen."""
        # Update title animation
        self.title_timer += 0.05
        
        return super().update()
    
    def draw(self):
        """Draw the menu screen."""
        super().draw()
        
        # Draw title
        title_y = 100
        title_text = "CIPHER CLASH"
        font = pygame.font.SysFont(None, FONT_SIZE_LARGE * 2)
        
        # Animated title effect
        for i, char in enumerate(title_text):
            char_x = SCREEN_WIDTH // 2 - len(title_text) * 20 + i * 40
            char_y = title_y + 10 * (0.5 + 0.5 * pygame.math.sin(self.title_timer * 2 + i * 0.3))
            
            # Flicker effect
            flicker = 1.0 + 0.3 * pygame.math.sin(self.title_timer * 10 + i)
            color = (
                min(255, int(GameColors.NEON_BLUE[0] * flicker)),
                min(255, int(GameColors.NEON_BLUE[1] * flicker)),
                min(255, int(GameColors.NEON_BLUE[2] * flicker))
            )
            
            char_surf = font.render(char, True, color)
            char_rect = char_surf.get_rect(center=(char_x, char_y))
            self.surface.blit(char_surf, char_rect)
        
        # Draw subtitle
        subtitle = "Decrypt the code before time runs out!"
        draw_text(
            self.surface,
            subtitle,
            (SCREEN_WIDTH // 2, title_y + 80),
            GameColors.NEON_GREEN,
            FONT_SIZE_MEDIUM,
            align="center"
        )
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.surface)
        
        # Draw difficulty section
        draw_text(
            self.surface,
            "Difficulty:",
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130),
            GameColors.TEXT_NORMAL,
            FONT_SIZE_MEDIUM,
            align="center"
        )
        
        for button in self.difficulty_buttons:
            button.draw(self.surface)
        
        # Draw cipher type section
        draw_text(
            self.surface,
            "Cipher Type:",
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 210),
            GameColors.TEXT_NORMAL,
            FONT_SIZE_MEDIUM,
            align="center"
        )
        
        for button in self.cipher_buttons:
            button.draw(self.surface)

class GameScreen(BaseScreen):
    """Game screen for Cipher Clash."""
    
    def __init__(self, surface, game_state):
        """Initialize the game screen."""
        super().__init__(surface, game_state)
        
        # Create UI elements
        self.terminal_box = TerminalBox(
            (SCREEN_WIDTH // 2 - 350, 150, 700, 200),
            "Encrypted message will appear here...",
            font_size=FONT_SIZE_MEDIUM
        )
        
        self.input_box = InputBox(
            (SCREEN_WIDTH // 2 - 300, 400, 600, 50),
            font_size=FONT_SIZE_MEDIUM,
            text="",
            max_length=100
        )
        
        self.hint_button = Button(
            (SCREEN_WIDTH - 150, 200),
            (120, 40),
            "Hint",
            self._use_hint,
            font_size=FONT_SIZE_SMALL
        )
        
        self.submit_button = Button(
            (SCREEN_WIDTH // 2 - 60, 470),
            (120, 40),
            "Submit",
            self._submit_answer,
            font_size=FONT_SIZE_MEDIUM
        )
        
        self.timer_bar = ProgressBar(
            (50, 50, SCREEN_WIDTH - 100, 30)
        )
        
        # Game state
        self.hint_text = None
        self.hint_display_time = 0
        self.result_message = None
        self.result_display_time = 0
    
    def reset(self):
        """Reset the game screen for a new game."""
        self.input_box.text = ""
        self.hint_text = None
        self.result_message = None
        
        # Update terminal box with the encrypted message
        if self.game_state.current_question:
            self.terminal_box.set_text(self.game_state.current_question["encrypted_text"])
    
    def _use_hint(self):
        """Use a hint."""
        hint = self.game_state.use_hint()
        if hint:
            self.hint_text = hint
            self.hint_display_time = time.time()
    
    def _submit_answer(self):
        """Submit the current answer."""
        answer = self.input_box.text
        if answer:
            is_correct = self.game_state.submit_answer(answer)
            
            # Display result message
            if is_correct:
                self.result_message = "Correct! +100 points"
                self.result_display_time = time.time()
                
                # Update terminal box with new encrypted message
                if self.game_state.current_question:
                    self.terminal_box.set_text(self.game_state.current_question["encrypted_text"])
            else:
                self.result_message = "Incorrect! Try again"
                self.result_display_time = time.time()
            
            # Clear input box
            self.input_box.text = ""
    
    def handle_event(self, event):
        """Handle pygame events."""
        # Check for Enter key to submit answer
        if event.type == KEYDOWN and event.key == K_RETURN:
            self._submit_answer()
        
        # Pass events to UI elements
        events = [event]
        self.hint_button.update(events)
        self.submit_button.update(events)
        
        # Handle input box events
        if self.input_box.handle_event(event):
            self._submit_answer()
    
    def update(self):
        """Update the game screen."""
        # Update game state
        self.game_state.update_timer()
        
        # Update UI elements
        self.input_box.update()
        self.terminal_box.update()
        
        # Update timer bar
        progress = 1.0 - self.game_state.get_progress_percentage()
        self.timer_bar.set_progress(progress)
        
        # Change timer bar color based on time remaining
        if progress < 0.2:
            self.timer_bar.color = GameColors.NEON_RED
        elif progress < 0.5:
            self.timer_bar.color = GameColors.NEON_YELLOW
        else:
            self.timer_bar.color = GameColors.NEON_GREEN
        
        # Check if hint should be hidden
        if self.hint_text and time.time() - self.hint_display_time > 5:
            self.hint_text = None
        
        # Check if result message should be hidden
        if self.result_message and time.time() - self.result_display_time > 2:
            self.result_message = None
        
        # Check if game is over
        if self.game_state.game_over:
            self.next_screen = "result"
        
        return super().update()
    
    def draw(self):
        """Draw the game screen."""
        super().draw()
        
        # Draw cipher type
        cipher_type = self.game_state.current_question["cipher_type"] if self.game_state.current_question else "Unknown"
        cipher_name = CIPHER_TYPES.get(cipher_type, {}).get("name", cipher_type.capitalize())
        
        draw_text(
            self.surface,
            f"Cipher: {cipher_name}",
            (50, 100),
            GameColors.NEON_BLUE,
            FONT_SIZE_MEDIUM
        )
        
        # Draw timer
        time_text = self.game_state.get_time_remaining_formatted()
        draw_text(
            self.surface,
            f"Time: {time_text}",
            (SCREEN_WIDTH - 50, 100),
            GameColors.NEON_BLUE,
            FONT_SIZE_MEDIUM,
            align="right"
        )
        
        # Draw score
        draw_text(
            self.surface,
            f"Score: {self.game_state.total_score}",
            (SCREEN_WIDTH // 2, 100),
            GameColors.NEON_GREEN,
            FONT_SIZE_MEDIUM,
            align="center"
        )
        
        # Draw timer bar
        self.timer_bar.draw(self.surface)
        
        # Draw terminal box with encrypted message
        self.terminal_box.draw(self.surface)
        
        # Draw input box
        draw_text(
            self.surface,
            "Your decryption:",
            (SCREEN_WIDTH // 2 - 300, 370),
            GameColors.TEXT_NORMAL,
            FONT_SIZE_SMALL
        )
        self.input_box.draw(self.surface)
        
        # Draw buttons
        self.hint_button.draw(self.surface)
        self.submit_button.draw(self.surface)
        
        # Draw hint count
        draw_text(
            self.surface,
            f"Hints: {self.game_state.hints_available}",
            (SCREEN_WIDTH - 150, 180),
            GameColors.TEXT_NORMAL,
            FONT_SIZE_SMALL
        )
        
        # Draw hint text if active
        if self.hint_text:
            # Draw hint background
            hint_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, 250, 600, 40)
            pygame.draw.rect(self.surface, (30, 30, 30), hint_rect, border_radius=5)  # Using direct color value instead of GameColors.DARK_GRAY
            pygame.draw.rect(self.surface, GameColors.NEON_BLUE, hint_rect, width=2, border_radius=5)
            
            # Draw hint text
            draw_text(
                self.surface,
                f"Hint: {self.hint_text}",
                (SCREEN_WIDTH // 2, 270),
                GameColors.NEON_GREEN,
                FONT_SIZE_SMALL,
                align="center"
            )
        
        # Draw result message if active
        if self.result_message:
            # Determine color based on message
            color = GameColors.NEON_GREEN if "Correct" in self.result_message else GameColors.NEON_RED
            
            draw_text(
                self.surface,
                self.result_message,
                (SCREEN_WIDTH // 2, 530),
                color,
                FONT_SIZE_MEDIUM,
                align="center"
            )

class ResultScreen(BaseScreen):
    """Result screen for Cipher Clash."""
    
    def __init__(self, surface, game_state):
        """Initialize the result screen."""
        super().__init__(surface, game_state)
        
        # Create buttons
        self.buttons = [
            Button(
                (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 150),
                (140, 50),
                "Play Again",
                self._play_again
            ),
            Button(
                (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 150),
                (140, 50),
                "Main Menu",
                self._return_to_menu
            )
        ]
        
        # Results data
        self.results = None
    
    def update_results(self):
        """Update the results data."""
        self.results = self.game_state.get_results()
    
    def _play_again(self):
        """Start a new game with the same settings."""
        self.game_state.start_game(self.game_state.difficulty, self.game_state.selected_cipher_type)
        self.next_screen = "game"
        self.game_state.play_sound("menu_click")
    
    def _return_to_menu(self):
        """Return to the main menu."""
        self.next_screen = "menu"
        self.game_state.play_sound("menu_click")
    
    def handle_event(self, event):
        """Handle pygame events."""
        # Pass events to buttons
        events = [event]
        for button in self.buttons:
            button.update(events)
    
    def update(self):
        """Update the result screen."""
        return super().update()
    
    def draw(self):
        """Draw the result screen."""
        super().draw()
        
        # Draw title
        draw_title(
            self.surface,
            "Game Over!",
            100,
            GameColors.NEON_PURPLE,
            FONT_SIZE_LARGE
        )
        
        if self.results:
            # Draw score
            draw_text(
                self.surface,
                f"Final Score: {self.results['total_score']}",
                (SCREEN_WIDTH // 2, 180),
                GameColors.NEON_GREEN,
                FONT_SIZE_LARGE,
                align="center"
            )
            
            # Draw statistics
            stats_y = 250
            stats_spacing = 40
            
            draw_text(
                self.surface,
                f"Questions Answered: {self.results['questions_answered']}",
                (SCREEN_WIDTH // 2, stats_y),
                GameColors.TEXT_NORMAL,
                FONT_SIZE_MEDIUM,
                align="center"
            )
            
            draw_text(
                self.surface,
                f"Correct Answers: {self.results['correct_answers']}",
                (SCREEN_WIDTH // 2, stats_y + stats_spacing),
                GameColors.TEXT_NORMAL,
                FONT_SIZE_MEDIUM,
                align="center"
            )
            
            accuracy = int(self.results['accuracy'] * 100)
            draw_text(
                self.surface,
                f"Accuracy: {accuracy}%",
                (SCREEN_WIDTH // 2, stats_y + 2 * stats_spacing),
                GameColors.TEXT_NORMAL,
                FONT_SIZE_MEDIUM,
                align="center"
            )
            
            minutes = int(self.results['time_taken']) // 60
            seconds = int(self.results['time_taken']) % 60
            draw_text(
                self.surface,
                f"Time Taken: {minutes:02d}:{seconds:02d}",
                (SCREEN_WIDTH // 2, stats_y + 3 * stats_spacing),
                GameColors.TEXT_NORMAL,
                FONT_SIZE_MEDIUM,
                align="center"
            )
            
            draw_text(
                self.surface,
                f"Difficulty: {self.results['difficulty'].capitalize()}",
                (SCREEN_WIDTH // 2, stats_y + 4 * stats_spacing),
                GameColors.TEXT_NORMAL,
                FONT_SIZE_MEDIUM,
                align="center"
            )
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.surface)
