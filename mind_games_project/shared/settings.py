"""
Shared settings for the Mind Games project.
Contains global configuration variables used across all games.
"""

# Application information
TITLE = "Mind Games"
VERSION = "0.1.0"

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
DEFAULT_FONT = "Arial"

# Audio settings
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.8

# File paths
import os

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Shared assets directory
SHARED_ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SHARED_IMAGES_DIR = os.path.join(SHARED_ASSETS_DIR, "images")
SHARED_SOUNDS_DIR = os.path.join(SHARED_ASSETS_DIR, "sounds")
SHARED_FONTS_DIR = os.path.join(SHARED_ASSETS_DIR, "fonts")

# Game-specific asset path function
def get_game_asset_path(game_id, asset_type, filename):
    """
    Get the path to a game-specific asset.
    
    Args:
        game_id (str): The ID of the game (e.g., 'cipher_clash')
        asset_type (str): The type of asset ('images', 'sounds', 'fonts')
        filename (str): The name of the asset file
        
    Returns:
        str: The full path to the asset
    """
    return os.path.join(BASE_DIR, "games", game_id, "assets", asset_type, filename)

# Color definitions (RGB)
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)

# Difficulty levels
DIFFICULTY_EASY = "easy"
DIFFICULTY_MEDIUM = "medium"
DIFFICULTY_HARD = "hard"

# Default game settings
DEFAULT_DIFFICULTY = DIFFICULTY_MEDIUM
DEFAULT_TIME_LIMIT = 300  # seconds
DEFAULT_SCORE_MULTIPLIER = 1.0

# User preferences (can be overridden by user settings)
USER_PREFERENCES = {
    "fullscreen": False,
    "show_tutorial": True,
    "difficulty": DEFAULT_DIFFICULTY,
    "music_enabled": True,
    "sfx_enabled": True
}
