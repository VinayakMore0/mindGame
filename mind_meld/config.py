"""
Configuration settings for Mind Meld game.
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Grid settings
GRID_SIZE = 4  # 4x4 grid
CELL_SIZE = 100
GRID_MARGIN = 10
GRID_OFFSET_X = (SCREEN_WIDTH - (GRID_SIZE * (CELL_SIZE + GRID_MARGIN))) // 2
GRID_OFFSET_Y = 150

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game colors for patterns
PATTERN_COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE]

# Timing settings (in milliseconds)
DISPLAY_TIME_BASE = 2000  # Base time to display pattern
DISPLAY_TIME_DECREMENT = 100  # Reduce display time each level
MIN_DISPLAY_TIME = 500  # Minimum display time
FLASH_DURATION = 500  # Duration of highlight flash

# Game settings
STARTING_PATTERN_LENGTH = 3
MAX_PATTERN_LENGTH = 20
SCORE_PER_CORRECT = 10
BONUS_MULTIPLIER = 1.5  # Score multiplier for quick responses

# File paths
ASSETS_DIR = "assets/"
IMAGES_DIR = ASSETS_DIR + "images/"
SOUNDS_DIR = ASSETS_DIR + "sounds/"
FONTS_DIR = ASSETS_DIR + "fonts/"
LEVELS_DIR = "levels/"

# Player modes
SINGLE_PLAYER = 1
TWO_PLAYER = 2
