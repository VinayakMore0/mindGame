"""
Helper utilities for Mind Meld game.
"""
import pygame
import os
import time
from config import IMAGES_DIR, SOUNDS_DIR, FONTS_DIR

def load_image(filename):
    """Load an image and convert it for optimal display."""
    try:
        path = os.path.join(IMAGES_DIR, filename)
        image = pygame.image.load(path)
        return image.convert_alpha()  # For images with transparency
    except pygame.error:
        print(f"Error loading image: {filename}")
        return None

def load_sound(filename):
    """Load a sound effect."""
    try:
        path = os.path.join(SOUNDS_DIR, filename)
        return pygame.mixer.Sound(path)
    except pygame.error:
        print(f"Error loading sound: {filename}")
        return None

def load_font(filename, size):
    """Load a font with the specified size."""
    try:
        path = os.path.join(FONTS_DIR, filename)
        return pygame.font.Font(path, size)
    except pygame.error:
        print(f"Error loading font: {filename}")
        return pygame.font.SysFont('arial', size)  # Fallback to system font

def draw_text(surface, text, font, color, x, y, align="topleft"):
    """Draw text on a surface with alignment options."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "topleft":
        text_rect.topleft = (x, y)
    elif align == "center":
        text_rect.center = (x, y)
    elif align == "topright":
        text_rect.topright = (x, y)
    
    surface.blit(text_surface, text_rect)
    return text_rect

class Timer:
    """Simple timer class for game events."""
    def __init__(self):
        self.start_time = 0
        self.duration = 0
        self.running = False
        self.completed = False
    
    def start(self, duration):
        """Start the timer with a specified duration in milliseconds."""
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.running = True
        self.completed = False
    
    def check(self):
        """Check if the timer has completed."""
        if not self.running:
            return False
        
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.running = False
            self.completed = True
            return True
        return False
    
    def get_elapsed(self):
        """Get elapsed time in milliseconds."""
        if not self.running:
            return 0
        return pygame.time.get_ticks() - self.start_time
    
    def get_remaining(self):
        """Get remaining time in milliseconds."""
        if not self.running:
            return 0
        elapsed = pygame.time.get_ticks() - self.start_time
        remaining = self.duration - elapsed
        return max(0, remaining)
    
    def stop(self):
        """Stop the timer."""
        self.running = False
