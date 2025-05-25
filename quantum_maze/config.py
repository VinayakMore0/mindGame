"""
Configuration settings for Quantum Maze game.
"""

# Screen settings
TILE_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WALL_COLOR = (50, 50, 50)
FLOOR_COLOR = (200, 200, 200)
PLAYER_COLOR = (0, 0, 255)

# File paths
LEVEL_DIR = "levels/"
ASSETS_DIR = "assets/"
IMAGES_DIR = ASSETS_DIR + "images/"
SOUNDS_DIR = ASSETS_DIR + "sounds/"
FONTS_DIR = ASSETS_DIR + "fonts/"

# Game settings
FPS = 60
PLAYER_SPEED = 4  # Reduced from 5 for more precise movement
