"""
Font Manager module for Cipher Clash game.
Handles loading and using fonts for text display.
"""

import os
import sys
import platform

# Check if running in a terminal that supports ANSI escape codes
def supports_ansi():
    """Check if the terminal supports ANSI escape codes."""
    if platform.system() == 'Windows':
        # On Windows, check if running in a modern terminal
        return os.environ.get('WT_SESSION') or 'TERM' in os.environ
    else:
        # Most Unix-like systems support ANSI
        return True

# ANSI escape codes for text styling
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_ITALIC = "\033[3m"
ANSI_UNDERLINE = "\033[4m"
ANSI_BLINK = "\033[5m"
ANSI_REVERSE = "\033[7m"

# ANSI color codes
ANSI_COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
}

# Font styles for different game elements
FONT_STYLES = {
    "title": {
        "color": "bright_green",
        "bold": True,
        "blink": False
    },
    "subtitle": {
        "color": "bright_cyan",
        "bold": True,
        "blink": False
    },
    "heading": {
        "color": "bright_white",
        "bold": True,
        "blink": False
    },
    "cipher_text": {
        "color": "bright_green",
        "bold": False,
        "blink": False
    },
    "cipher_type": {
        "color": "bright_yellow",
        "bold": True,
        "blink": False
    },
    "solution": {
        "color": "bright_white",
        "bold": False,
        "blink": False
    },
    "hint": {
        "color": "bright_magenta",
        "bold": True,
        "blink": False
    },
    "error": {
        "color": "bright_red",
        "bold": True,
        "blink": False
    },
    "success": {
        "color": "bright_green",
        "bold": True,
        "blink": False
    },
    "warning": {
        "color": "bright_yellow",
        "bold": True,
        "blink": False
    },
    "info": {
        "color": "bright_cyan",
        "bold": False,
        "blink": False
    },
    "score": {
        "color": "bright_yellow",
        "bold": True,
        "blink": False
    },
    "time": {
        "color": "bright_white",
        "bold": True,
        "blink": False
    },
    "time_low": {
        "color": "bright_red",
        "bold": True,
        "blink": True
    },
    "input_prompt": {
        "color": "bright_green",
        "bold": True,
        "blink": False
    },
    "menu_option": {
        "color": "bright_white",
        "bold": False,
        "blink": False
    },
    "menu_selected": {
        "color": "bright_green",
        "bold": True,
        "blink": False
    }
}

class FontManager:
    """Manages fonts and text styling for the game."""
    
    def __init__(self):
        """Initialize the font manager."""
        self.ansi_supported = supports_ansi()
        self.use_styling = True
        
    def toggle_styling(self):
        """Toggle text styling on/off."""
        self.use_styling = not self.use_styling
        return self.use_styling
        
    def style_text(self, text, style_name):
        """
        Apply a predefined style to text.
        
        Args:
            text (str): The text to style
            style_name (str): Name of the style to apply
            
        Returns:
            str: The styled text
        """
        if not self.ansi_supported or not self.use_styling:
            return text
            
        if style_name not in FONT_STYLES:
            return text
            
        style = FONT_STYLES[style_name]
        result = ""
        
        # Apply color
        if "color" in style and style["color"] in ANSI_COLORS:
            result += ANSI_COLORS[style["color"]]
            
        # Apply bold
        if style.get("bold", False):
            result += ANSI_BOLD
            
        # Apply blink
        if style.get("blink", False):
            result += ANSI_BLINK
            
        # Add the text and reset
        result += text + ANSI_RESET
        return result
        
    def format_cipher_text(self, cipher_text, cipher_type):
        """
        Format cipher text with appropriate styling.
        
        Args:
            cipher_text (str): The encrypted text
            cipher_type (str): The type of cipher
            
        Returns:
            str: The formatted text
        """
        # Style the cipher type
        styled_type = self.style_text(cipher_type, "cipher_type")
        
        # Style the cipher text
        styled_text = self.style_text(cipher_text, "cipher_text")
        
        return f"{styled_type}:\n{styled_text}"
        
    def format_game_stats(self, score, ciphers_solved, attempts, time_remaining, time_limit):
        """
        Format game statistics with appropriate styling.
        
        Args:
            score (int): Current score
            ciphers_solved (int): Number of ciphers solved
            attempts (int): Remaining attempts
            time_remaining (float): Remaining time in seconds
            time_limit (float): Total time limit in seconds
            
        Returns:
            str: The formatted stats
        """
        # Style the score
        styled_score = self.style_text(f"Score: {score}", "score")
        
        # Style the ciphers solved
        styled_ciphers = self.style_text(f"Ciphers: {ciphers_solved}", "info")
        
        # Style the attempts
        styled_attempts = self.style_text(f"Attempts: {attempts}", "info")
        
        # Style the time (changes color when low)
        minutes = int(time_remaining // 60)
        seconds = int(time_remaining % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        
        time_style = "time_low" if time_remaining < (time_limit * 0.3) else "time"
        styled_time = self.style_text(time_text, time_style)
        
        return f"{styled_score}  |  {styled_ciphers}  |  {styled_attempts}  |  {styled_time}"
        
    def format_hint(self, hint_text, cost):
        """
        Format a hint with appropriate styling.
        
        Args:
            hint_text (str): The hint text
            cost (int): The point cost of the hint
            
        Returns:
            str: The formatted hint
        """
        # Style the hint header
        styled_header = self.style_text(f"HINT (Cost: {cost} points):", "hint")
        
        # Style the hint text
        styled_hint = self.style_text(hint_text, "info")
        
        return f"{styled_header}\n{styled_hint}"
        
    def format_success_message(self, points):
        """
        Format a success message with appropriate styling.
        
        Args:
            points (int): Points earned
            
        Returns:
            str: The formatted message
        """
        # Style the success header
        styled_header = self.style_text("CORRECT!", "success")
        
        # Style the points message
        styled_points = self.style_text(f"You earned {points} points!", "score")
        
        return f"{styled_header}\n{styled_points}"
        
    def format_error_message(self, message):
        """
        Format an error message with appropriate styling.
        
        Args:
            message (str): The error message
            
        Returns:
            str: The formatted message
        """
        return self.style_text(message, "error")
        
    def format_title(self, title):
        """
        Format a title with appropriate styling.
        
        Args:
            title (str): The title text
            
        Returns:
            str: The formatted title
        """
        return self.style_text(title, "title")
        
    def format_menu_option(self, option, selected=False):
        """
        Format a menu option with appropriate styling.
        
        Args:
            option (str): The menu option text
            selected (bool): Whether this option is selected
            
        Returns:
            str: The formatted option
        """
        style = "menu_selected" if selected else "menu_option"
        return self.style_text(option, style)
        
    def format_input_prompt(self, prompt):
        """
        Format an input prompt with appropriate styling.
        
        Args:
            prompt (str): The prompt text
            
        Returns:
            str: The formatted prompt
        """
        return self.style_text(prompt, "input_prompt")

# Create a global instance
font_manager = FontManager()
