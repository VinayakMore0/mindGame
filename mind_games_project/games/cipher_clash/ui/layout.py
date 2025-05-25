"""
Layout module for Cipher Clash.
Contains reusable UI components and layout helpers.
"""
import pygame
import math
from mind_games_project.games.cipher_clash.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GameColors, 
    FONT_SIZE_SMALL, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE,
    BUTTON_SIZE, ANIMATION_SPEEDS, GLOW_INTENSITY
)

def ensure_rgba(color):
    """Convert RGB color to RGBA if needed."""
    color_list = list(color)
    if len(color_list) == 3:
        return color_list + [255]
    return color_list

# Define FONT_SIZE_TITLE if it's not imported from config
FONT_SIZE_TITLE = 72

class Button:
    """A button UI element with hover and click effects."""
    
    def __init__(self, rect, text, action=None, color=None, 
                 hover_color=None, text_color=None,
                 font_size=None, glow=None):
        """
        Initialize a button.
        
        Args:
            rect (pygame.Rect or tuple): The button rectangle or position
            text (str): The button text
            action: The function to call when clicked
            color: The button color
            hover_color: The button color when hovered
            text_color: The text color
            font_size (int): The font size
            glow (bool): Whether to apply a glow effect
        """
        # Set default values
        _color = GameColors.BUTTON_NORMAL if color is None else color
        _hover_color = GameColors.BUTTON_HOVER if hover_color is None else hover_color
        _text_color = GameColors.TEXT_NORMAL if text_color is None else text_color
        _font_size = FONT_SIZE_MEDIUM if font_size is None else font_size
        _glow = True if glow is None else glow
        
        # Handle different rect formats
        if isinstance(rect, tuple) and len(rect) == 2 and isinstance(text, tuple) and len(text) == 2:
            # If rect is position (x,y) and text is size (width,height)
            x, y = rect
            width, height = text
            self.rect = pygame.Rect(x, y, width, height)
            # Update text to be actual text (3rd argument)
            self.text = action
            # Update action to be actual action (4th argument)
            self.action = _color
            # Update other parameters
            self.color = _hover_color
            self.hover_color = _text_color
            self.text_color = _font_size
            self.font_size = _glow
            self.hovered = False
            self.clicked = False
            self.glow = True
        else:
            # Normal initialization
            self.rect = pygame.Rect(rect)
            self.text = text
            self.action = action
            self.color = _color
            self.hover_color = _hover_color
            self.text_color = _text_color
            self.font_size = _font_size
            self.hovered = False
            self.clicked = False
            self.glow = _glow
            
        # Initialize font and glow timer
        self.glow_timer = 0
        self.font = pygame.font.SysFont(None, self.font_size)
        self.glow_timer = 0
    
    def update(self, events):
        """
        Update the button state.
        
        Args:
            events (list): The pygame events
            
        Returns:
            bool: True if the button was clicked
        """
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Update glow timer
        self.glow_timer = (self.glow_timer + 0.05) % (2 * math.pi)
        
        # Check for click events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                    self.clicked = True
                    if self.action:
                        self.action()
                    return True
        
        return False
    
    def draw(self, surface):
        """
        Draw the button.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw glow effect if enabled and hovered
        if self.glow and self.hovered:
            glow_size = int(4 + 2 * math.sin(self.glow_timer))
            glow_rect = self.rect.inflate(glow_size, glow_size)
            
            glow_color = ensure_rgba(GameColors.NEON_BLUE)
            glow_color[3] = int(128 + 64 * math.sin(self.glow_timer))
            pygame.draw.rect(surface, glow_color, glow_rect, border_radius=10)
        
        # Draw button background
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        
        # Draw button border
        border_color = GameColors.NEON_BLUE if self.hovered else GameColors.DARK_GRAY
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=5)
        
        # Draw button text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class InputBox:
    """An input box UI element for text entry."""
    
    def __init__(self, rect, font_size=FONT_SIZE_MEDIUM, text='', 
                 color=GameColors.DARK_GRAY, active_color=GameColors.NEON_BLUE,
                 text_color=GameColors.TERMINAL_TEXT, max_length=None):
        """
        Initialize an input box.
        
        Args:
            rect (pygame.Rect): The input box rectangle
            font_size (int): The font size
            text (str): The initial text
            color: The box color
            active_color: The box color when active
            text_color: The text color
            max_length (int): The maximum text length
        """
        self.rect = pygame.Rect(rect)
        self.color = color
        self.active_color = active_color
        self.text_color = text_color
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = max_length
    
    def handle_event(self, event):
        """
        Handle events for the input box.
        
        Args:
            event: The pygame event
            
        Returns:
            bool: True if the text was changed
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state
            self.active = self.rect.collidepoint(event.pos)
            return False
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                # Return key submits the input
                return True
            elif event.key == pygame.K_BACKSPACE:
                # Backspace removes the last character
                self.text = self.text[:-1]
            else:
                # Add character if not at max length
                if self.max_length is None or len(self.text) < self.max_length:
                    self.text += event.unicode
            return False
        
        return False
    
    def update(self):
        """Update the input box state."""
        # Blink the cursor
        self.cursor_timer += 0.1
        if self.cursor_timer >= 1.0:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, surface):
        """
        Draw the input box.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw the box
        color = self.active_color if self.active else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, GameColors.NEON_BLUE, self.rect, width=2, border_radius=5)
        
        # Draw the text
        text_surf = self.font.render(self.text, True, self.text_color)
        
        # Ensure text fits within the box
        text_width = text_surf.get_width()
        if text_width > self.rect.width - 20:
            # Show only the end of the text if it's too long
            visible_text = self.text
            while text_width > self.rect.width - 20:
                visible_text = visible_text[1:]
                text_surf = self.font.render(visible_text, True, self.text_color)
                text_width = text_surf.get_width()
        
        # Position text within the box
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)
        
        # Draw cursor if active
        if self.active and self.cursor_visible:
            cursor_pos = text_rect.right + 2
            cursor_height = text_rect.height - 4
            pygame.draw.line(
                surface, 
                self.text_color, 
                (cursor_pos, text_rect.top + 2),
                (cursor_pos, text_rect.top + cursor_height),
                2
            )

class TerminalBox:
    """A terminal-style text box for displaying cipher text."""
    
    def __init__(self, rect, text='', font_size=FONT_SIZE_MEDIUM, 
                 bg_color=GameColors.BACKGROUND, text_color=GameColors.TERMINAL_GREEN,
                 border_color=GameColors.NEON_BLUE, flicker=True):
        """
        Initialize a terminal box.
        
        Args:
            rect (pygame.Rect): The terminal box rectangle
            text (str): The initial text
            font_size (int): The font size
            bg_color: The background color
            text_color: The text color
            border_color: The border color
            flicker (bool): Whether to apply a flickering effect
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.font = pygame.font.SysFont("monospace", font_size)
        self.flicker = flicker
        self.flicker_timer = 0
        self.flicker_intensity = 0
    
    def set_text(self, text):
        """Set the terminal text."""
        self.text = text
    
    def update(self):
        """Update the terminal box state."""
        if self.flicker:
            self.flicker_timer += 0.05
            self.flicker_intensity = 0.05 * math.sin(self.flicker_timer * 5)
    
    def draw(self, surface):
        """
        Draw the terminal box.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=5)
        
        # Draw border with glow effect
        border_color = list(self.border_color)
        if self.flicker:
            # Adjust color intensity for flicker effect
            for i in range(3):
                border_color[i] = min(255, max(0, border_color[i] + int(20 * self.flicker_intensity)))
        
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=5)
        
        # Draw text with word wrapping
        text_color = list(self.text_color)
        if self.flicker:
            # Adjust color intensity for flicker effect
            for i in range(3):
                text_color[i] = min(255, max(0, text_color[i] + int(20 * self.flicker_intensity)))
        
        self._draw_wrapped_text(surface, text_color)
    
    def _draw_wrapped_text(self, surface, text_color):
        """Draw text with word wrapping."""
        words = self.text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Test if adding this word exceeds the width
            test_line = ' '.join(current_line + [word])
            test_width = self.font.size(test_line)[0]
            
            if test_width < self.rect.width - 20:
                current_line.append(word)
            else:
                # Start a new line
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw each line
        y_offset = 10
        for line in lines:
            text_surf = self.font.render(line, True, text_color)
            text_rect = text_surf.get_rect(topleft=(self.rect.left + 10, self.rect.top + y_offset))
            surface.blit(text_surf, text_rect)
            y_offset += self.font.get_linesize()

class ProgressBar:
    """A progress bar UI element."""
    
    def __init__(self, rect, progress=0.0, color=GameColors.NEON_GREEN, 
                 bg_color=GameColors.DARK_GRAY, border_color=GameColors.NEON_BLUE):
        """
        Initialize a progress bar.
        
        Args:
            rect (pygame.Rect): The progress bar rectangle
            progress (float): The initial progress (0.0 to 1.0)
            color: The progress bar color
            bg_color: The background color
            border_color: The border color
        """
        self.rect = pygame.Rect(rect)
        self.progress = max(0.0, min(1.0, progress))
        self.color = color
        self.bg_color = bg_color
        self.border_color = border_color
    
    def set_progress(self, progress):
        """Set the progress value (0.0 to 1.0)."""
        self.progress = max(0.0, min(1.0, progress))
    
    def draw(self, surface):
        """
        Draw the progress bar.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=5)
        
        # Draw progress
        progress_rect = pygame.Rect(
            self.rect.left,
            self.rect.top,
            int(self.rect.width * self.progress),
            self.rect.height
        )
        if progress_rect.width > 0:
            pygame.draw.rect(surface, self.color, progress_rect, border_radius=5)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, width=2, border_radius=5)

def draw_text(surface, text, pos, color=GameColors.TEXT_NORMAL, font_size=FONT_SIZE_MEDIUM, 
              align="left", font_name=None):
    """
    Draw text on a surface.
    
    Args:
        surface: The pygame surface to draw on
        text (str): The text to draw
        pos (tuple): The position (x, y)
        color: The text color
        font_size (int): The font size
        align (str): The text alignment ('left', 'center', 'right')
        font_name (str): The font name (None for default)
    """
    font = pygame.font.SysFont(font_name, font_size)
    text_surf = font.render(text, True, color)
    
    if align == "center":
        text_rect = text_surf.get_rect(center=pos)
    elif align == "right":
        text_rect = text_surf.get_rect(midright=pos)
    else:  # left
        text_rect = text_surf.get_rect(midleft=pos)
    
    surface.blit(text_surf, text_rect)

def draw_title(surface, text, y_pos, color=GameColors.NEON_BLUE, font_size=FONT_SIZE_TITLE, 
               glow=True):
    """
    Draw a title with optional glow effect.
    
    Args:
        surface: The pygame surface to draw on
        text (str): The title text
        y_pos (int): The y position
        color: The title color
        font_size (int): The font size
        glow (bool): Whether to apply a glow effect
    """
    font = pygame.font.SysFont(None, font_size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
    
    if glow:
        # Draw glow effect
        glow_surf = pygame.Surface((text_surf.get_width() + 10, text_surf.get_height() + 10), 
                                  pygame.SRCALPHA)
        
        glow_color = ensure_rgba(color)
        
        for i in range(5):
            alpha = 50 - i * 10
            glow_color[3] = alpha
            glow_rect = pygame.Rect(5 - i, 5 - i, 
                                   text_surf.get_width() + i * 2, 
                                   text_surf.get_height() + i * 2)
            pygame.draw.rect(glow_surf, glow_color, glow_rect, border_radius=5)
        
        glow_rect = glow_surf.get_rect(center=text_rect.center)
        surface.blit(glow_surf, glow_rect)
    
    surface.blit(text_surf, text_rect)
