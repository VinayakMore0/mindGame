"""
Player input handler for Logic Arena game.
Captures and verifies answers from user.
"""
import pygame
from config import OPTION_BUTTON_WIDTH, OPTION_BUTTON_HEIGHT

class PlayerInput:
    def __init__(self):
        """Initialize the player input handler."""
        self.current_player = 1  # Player 1 by default
        self.input_enabled = True
        self.option_buttons = []
        self.selected_option = None
    
    def enable_input(self):
        """Enable player input."""
        self.input_enabled = True
        self.selected_option = None
    
    def disable_input(self):
        """Disable player input."""
        self.input_enabled = False
    
    def is_input_enabled(self):
        """Check if input is enabled."""
        return self.input_enabled
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 2 if self.current_player == 1 else 1
    
    def get_current_player(self):
        """Get the current player."""
        return self.current_player
    
    def set_option_buttons(self, buttons):
        """Set the option buttons for the current question."""
        self.option_buttons = buttons
        self.selected_option = None
    
    def handle_click(self, mouse_pos):
        """Handle mouse click on option buttons."""
        if not self.input_enabled:
            return None
        
        for i, button in enumerate(self.option_buttons):
            if button.collidepoint(mouse_pos):
                self.selected_option = i
                return i
        
        return None
    
    def get_selected_option(self):
        """Get the currently selected option."""
        return self.selected_option
    
    def clear_selection(self):
        """Clear the current selection."""
        self.selected_option = None
    
    def handle_keyboard_input(self, key):
        """Handle keyboard input for answering questions."""
        if not self.input_enabled:
            return None
        
        # Number keys 1-4 for options
        if pygame.K_1 <= key <= pygame.K_4:
            option = key - pygame.K_1  # Convert to 0-based index
            if option < len(self.option_buttons):
                self.selected_option = option
                return option
        
        return None
