"""
Player input handler for Cipher Clash game.
Collects and verifies input from player.
"""
import pygame
from config import INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT

class PlayerInput:
    def __init__(self):
        """Initialize the player input handler."""
        self.current_player = 1  # Player 1 by default
        self.input_enabled = True
        self.input_text = ""
        self.input_rect = None
        self.active = False
        self.max_length = 20  # Maximum input length
    
    def enable_input(self):
        """Enable player input."""
        self.input_enabled = True
        self.input_text = ""
    
    def disable_input(self):
        """Disable player input."""
        self.input_enabled = False
    
    def is_input_enabled(self):
        """Check if input is enabled."""
        return self.input_enabled
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 2 if self.current_player == 1 else 1
        self.input_text = ""
    
    def get_current_player(self):
        """Get the current player."""
        return self.current_player
    
    def set_input_rect(self, rect):
        """Set the input box rectangle."""
        self.input_rect = rect
    
    def handle_click(self, mouse_pos):
        """Handle mouse click on input box."""
        if not self.input_enabled or not self.input_rect:
            return
        
        # Check if click is within input box
        if self.input_rect.collidepoint(mouse_pos):
            self.active = True
        else:
            self.active = False
    
    def handle_key_event(self, event):
        """Handle keyboard input events."""
        if not self.input_enabled or not self.active:
            return
        
        if event.key == pygame.K_RETURN:
            # Return the current input text but don't clear it yet
            return self.input_text
        elif event.key == pygame.K_BACKSPACE:
            # Remove last character
            self.input_text = self.input_text[:-1]
        else:
            # Add character if it's printable and within max length
            if event.unicode.isprintable() and len(self.input_text) < self.max_length:
                self.input_text += event.unicode
        
        return None
    
    def get_input_text(self):
        """Get the current input text."""
        return self.input_text
    
    def clear_input(self):
        """Clear the input text."""
        self.input_text = ""
    
    def render(self, screen, font, text_color, active_color, inactive_color):
        """Render the input box and text."""
        if not self.input_rect:
            return
        
        # Draw the input box
        color = active_color if self.active else inactive_color
        pygame.draw.rect(screen, color, self.input_rect, 2)
        
        # Render the input text
        text_surface = font.render(self.input_text, True, text_color)
        
        # Ensure text fits within the box
        text_width = text_surface.get_width()
        if text_width >= self.input_rect.width - 10:
            # Show only the end of the text if it's too long
            visible_text = self.input_text[-(self.input_rect.width // 10):]
            text_surface = font.render(visible_text, True, text_color)
        
        # Position text within the box
        screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + (self.input_rect.height - text_surface.get_height()) // 2))
        
        # Draw cursor when active
        if self.active:
            cursor_pos = self.input_rect.x + 5 + text_surface.get_width()
            cursor_height = text_surface.get_height()
            if cursor_height == 0:  # Fallback if text is empty
                cursor_height = font.get_height()
            
            cursor_y = self.input_rect.y + (self.input_rect.height - cursor_height) // 2
            pygame.draw.line(screen, text_color, (cursor_pos, cursor_y), (cursor_pos, cursor_y + cursor_height), 2)
