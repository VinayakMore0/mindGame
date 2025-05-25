"""
Helper utilities for Quantum Maze game.
"""
import pygame
import os
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
