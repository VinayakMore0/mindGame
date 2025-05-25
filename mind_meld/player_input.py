"""
Player input handler for Mind Meld game.
Handles and validates player input for pattern recreation.
"""
import pygame
from config import GRID_SIZE, CELL_SIZE, GRID_MARGIN, GRID_OFFSET_X, GRID_OFFSET_Y

class PlayerInput:
    def __init__(self):
        """Initialize the player input handler."""
        self.player_pattern = []
        self.current_player = 1  # Player 1 by default
        self.input_enabled = False
    
    def enable_input(self):
        """Enable player input."""
        self.input_enabled = True
        self.player_pattern = []
    
    def disable_input(self):
        """Disable player input."""
        self.input_enabled = False
    
    def is_input_enabled(self):
        """Check if input is enabled."""
        return self.input_enabled
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 2 if self.current_player == 1 else 1
        self.player_pattern = []
    
    def get_current_player(self):
        """Get the current player."""
        return self.current_player
    
    def handle_click(self, mouse_pos):
        """Handle mouse click and convert to grid position."""
        if not self.input_enabled:
            return None
        
        # Convert mouse position to grid coordinates
        x = (mouse_pos[0] - GRID_OFFSET_X) // (CELL_SIZE + GRID_MARGIN)
        y = (mouse_pos[1] - GRID_OFFSET_Y) // (CELL_SIZE + GRID_MARGIN)
        
        # Check if click is within grid bounds
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            self.player_pattern.append((x, y))
            return (x, y)
        
        return None
    
    def get_grid_position(self, mouse_pos):
        """Convert mouse position to grid position without recording it."""
        x = (mouse_pos[0] - GRID_OFFSET_X) // (CELL_SIZE + GRID_MARGIN)
        y = (mouse_pos[1] - GRID_OFFSET_Y) // (CELL_SIZE + GRID_MARGIN)
        
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            return (x, y)
        
        return None
    
    def get_player_pattern(self):
        """Get the pattern input by the player."""
        return self.player_pattern
    
    def clear_pattern(self):
        """Clear the player's input pattern."""
        self.player_pattern = []
    
    def check_pattern_match(self, target_pattern):
        """Check if player's pattern matches the target pattern."""
        if len(self.player_pattern) != len(target_pattern):
            return False
        
        for i in range(len(target_pattern)):
            if self.player_pattern[i] != target_pattern[i]:
                return False
        
        return True
