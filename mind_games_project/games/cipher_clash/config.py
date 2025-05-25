"""
Configuration settings for the Cipher Clash game.
"""
import os
import pygame
from mind_games_project.shared.settings import Colors

# Game information
GAME_TITLE = "Cipher Clash"
GAME_VERSION = "0.1.0"
GAME_DESCRIPTION = "A fast-paced, competitive game where players must decrypt coded messages using different types of classic ciphers."

# Game-specific paths
GAME_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(GAME_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
ICONS_DIR = os.path.join(IMAGES_DIR, "icons")
BACKGROUNDS_DIR = os.path.join(IMAGES_DIR, "backgrounds")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
DATA_DIR = os.path.join(GAME_DIR, "data")

# Game settings
FPS = 60
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Game-specific colors
class GameColors:
    BACKGROUND = (10, 10, 20, 255)  # Deep black with a hint of blue
    NEON_BLUE = (0, 195, 255, 255)
    NEON_GREEN = (57, 255, 20, 255)
    NEON_RED = (255, 41, 55, 255)
    NEON_PURPLE = (200, 50, 255, 255)
    NEON_YELLOW = (255, 255, 0, 255)  # Added missing NEON_YELLOW
    TERMINAL_GREEN = (0, 255, 0, 255)
    TERMINAL_TEXT = (200, 255, 200, 255)
    BUTTON_NORMAL = (30, 30, 50, 255)
    BUTTON_HOVER = (50, 50, 80, 255)
    BUTTON_ACTIVE = (70, 70, 100, 255)
    TEXT_NORMAL = (255, 255, 255, 255)  # Colors.WHITE
    TEXT_HIGHLIGHT = (255, 255, 150, 255)
    DARK_GRAY = (30, 30, 30, 255)  # Added missing DARK_GRAY

# Font settings
FONT_MONOSPACE = "Source Code Pro"
FONT_DISPLAY = "Orbitron"
FONT_SIZE_SMALL = 16
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 36
FONT_SIZE_TITLE = 72

# Game mechanics
DIFFICULTY_LEVELS = {
    "easy": {
        "time_limit": 120,  # seconds
        "hint_count": 3,
        "cipher_complexity": 0.3,  # 0.0 to 1.0
        "score_multiplier": 1.0
    },
    "medium": {
        "time_limit": 90,
        "hint_count": 2,
        "cipher_complexity": 0.6,
        "score_multiplier": 1.5
    },
    "hard": {
        "time_limit": 60,
        "hint_count": 1,
        "cipher_complexity": 0.9,
        "score_multiplier": 2.0
    }
}

# Cipher types
CIPHER_TYPES = {
    "caesar": {
        "name": "Caesar Cipher",
        "icon": "caesar.png",
        "description": "A substitution cipher where each letter is shifted by a fixed number of positions.",
        "difficulty": 1
    },
    "vigenere": {
        "name": "Vigenère Cipher",
        "icon": "vigenere.png",
        "description": "A method of encrypting text using a series of interwoven Caesar ciphers based on a keyword.",
        "difficulty": 2
    },
    "morse": {
        "name": "Morse Code",
        "icon": "morse.png",
        "description": "A code that uses dots and dashes to represent letters and numbers.",
        "difficulty": 1
    },
    "substitution": {
        "name": "Substitution Cipher",
        "icon": "substitution.png",
        "description": "A cipher that replaces each letter with another letter or symbol.",
        "difficulty": 3
    },
    "transposition": {
        "name": "Transposition Cipher",
        "icon": "transposition.png",
        "description": "A cipher that rearranges the positions of characters without changing them.",
        "difficulty": 2
    }
}

# Sound settings
SOUND_EFFECTS = {
    "typing": "typing.wav",
    "correct": "correct.wav",
    "wrong": "wrong.wav",
    "time_warning": "time_warning.wav",
    "game_over": "game_over.wav",
    "menu_click": "menu_click.wav",
    "menu_hover": "menu_hover.wav"
}

MUSIC_TRACKS = {
    "menu": "menu_music.mp3",
    "gameplay_calm": "gameplay_calm.mp3",
    "gameplay_intense": "gameplay_intense.mp3",
    "victory": "victory.mp3"
}

# Animation settings
ANIMATION_SPEEDS = {
    "fast": 0.1,
    "normal": 0.3,
    "slow": 0.5
}

# UI settings
BUTTON_SIZE = (200, 50)
INPUT_BOX_SIZE = (600, 40)
TERMINAL_PADDING = 20
GLOW_INTENSITY = 0.7
