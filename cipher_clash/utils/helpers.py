"""
Helper utilities for Cipher Clash game.
"""
import pygame
import os
import json
import random
from config import IMAGES_DIR, SOUNDS_DIR, FONTS_DIR, CIPHERS_DIR

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
    elif align == "midleft":
        text_rect.midleft = (x, y)
    
    surface.blit(text_surface, text_rect)
    return text_rect

def load_word_bank():
    """Load words from the word bank file."""
    try:
        path = os.path.join(CIPHERS_DIR, "word_bank.txt")
        with open(path, 'r') as file:
            words = [word.strip().lower() for word in file.readlines() if word.strip()]
        return words
    except FileNotFoundError:
        print(f"Error: Word bank file not found at {path}")
        # Return a small default word list if file not found
        return ["python", "cipher", "puzzle", "cryptic", "decode", "secret", 
                "enigma", "mystery", "hidden", "scramble", "encrypt"]

def load_sample_ciphers():
    """Load pre-made cipher puzzles from JSON file."""
    try:
        path = os.path.join(CIPHERS_DIR, "samples.json")
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Sample ciphers file not found at {path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {path}")
        return []

def format_time(seconds):
    """Format time in seconds to MM:SS format."""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

class Timer:
    """Simple timer class for game events."""
    def __init__(self):
        self.start_time = 0
        self.duration = 0
        self.paused_time = 0
        self.paused = False
        self.running = False
    
    def start(self, duration):
        """Start the timer with a specified duration in seconds."""
        self.start_time = pygame.time.get_ticks()
        self.duration = duration * 1000  # Convert to milliseconds
        self.running = True
        self.paused = False
    
    def pause(self):
        """Pause the timer."""
        if self.running and not self.paused:
            self.paused_time = pygame.time.get_ticks()
            self.paused = True
    
    def resume(self):
        """Resume the timer."""
        if self.running and self.paused:
            # Adjust start time to account for pause duration
            pause_duration = pygame.time.get_ticks() - self.paused_time
            self.start_time += pause_duration
            self.paused = False
    
    def get_elapsed(self):
        """Get elapsed time in seconds."""
        if not self.running:
            return 0
        
        if self.paused:
            elapsed = (self.paused_time - self.start_time) / 1000
        else:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        
        return elapsed
    
    def get_remaining(self):
        """Get remaining time in seconds."""
        if not self.running:
            return 0
        
        elapsed = self.get_elapsed()
        remaining = self.duration / 1000 - elapsed
        return max(0, remaining)
    
    def is_expired(self):
        """Check if the timer has expired."""
        return self.get_remaining() <= 0
    
    def stop(self):
        """Stop the timer."""
        self.running = False
