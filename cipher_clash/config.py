"""
Configuration settings for Cipher Clash game.
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
MATRIX_GREEN = (0, 255, 0)
NEON_BLUE = (0, 128, 255)
NEON_PINK = (255, 0, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game settings
EASY_TIME_LIMIT = 60  # seconds
MEDIUM_TIME_LIMIT = 45  # seconds
HARD_TIME_LIMIT = 30  # seconds

# Scoring
BASE_SCORE = 100
TIME_BONUS_FACTOR = 10  # Points per second remaining
STREAK_BONUS = 50  # Additional points for consecutive correct answers
MAX_STREAK_BONUS = 500

# Cipher settings
MAX_WORD_LENGTH = 12
MIN_WORD_LENGTH = 3
MAX_ATTEMPTS = 3  # Maximum wrong guesses per cipher

# File paths
ASSETS_DIR = "assets/"
IMAGES_DIR = ASSETS_DIR + "images/"
SOUNDS_DIR = ASSETS_DIR + "sounds/"
FONTS_DIR = ASSETS_DIR + "fonts/"
CIPHERS_DIR = "ciphers/"

# Game modes
SINGLE_PLAYER = 1
TWO_PLAYER = 2

# Cipher types
CAESAR_CIPHER = "caesar"
SUBSTITUTION_CIPHER = "substitution"
JUMBLE_CIPHER = "jumble"
MORSE_CIPHER = "morse"
BINARY_CIPHER = "binary"

# Difficulty levels
DIFFICULTY_EASY = "easy"
DIFFICULTY_MEDIUM = "medium"
DIFFICULTY_HARD = "hard"

# UI settings
INPUT_BOX_WIDTH = 400
INPUT_BOX_HEIGHT = 50
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
