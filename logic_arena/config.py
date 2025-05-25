"""
Configuration settings for Logic Arena game.
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Game settings
EASY_TIME_LIMIT = 30  # seconds
MEDIUM_TIME_LIMIT = 20  # seconds
HARD_TIME_LIMIT = 15  # seconds

# Scoring
EASY_SCORE = 10
MEDIUM_SCORE = 20
HARD_SCORE = 30
TIME_BONUS_FACTOR = 0.5  # Bonus points per second remaining

# Wrong answer penalty (in seconds)
WRONG_ANSWER_PENALTY = 5

# File paths
ASSETS_DIR = "assets/"
IMAGES_DIR = ASSETS_DIR + "images/"
SHAPES_DIR = IMAGES_DIR + "shapes/"
BACKGROUNDS_DIR = IMAGES_DIR + "backgrounds/"
SOUNDS_DIR = ASSETS_DIR + "sounds/"
FONTS_DIR = ASSETS_DIR + "fonts/"
QUESTIONS_DIR = "questions/"

# Game modes
SOLO_MODE = 1
VERSUS_MODE = 2

# Question types
SEQUENCE_COMPLETION = "sequence"
NUMBER_PATTERN = "number"
ODD_ONE_OUT = "odd_one"
GRID_DEDUCTION = "grid"

# UI settings
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
OPTION_BUTTON_WIDTH = 150
OPTION_BUTTON_HEIGHT = 150
