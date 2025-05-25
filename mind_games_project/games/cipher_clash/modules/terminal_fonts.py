"""
Terminal Fonts module for Cipher Clash game.
Provides ASCII art fonts and text styling for terminal display.
"""

import os
import sys
import platform
import shutil

# Get terminal size
def get_terminal_size():
    """Get the current terminal size."""
    try:
        columns, rows = shutil.get_terminal_size()
        return columns, rows
    except:
        return 80, 24  # Default fallback size

# ASCII art fonts for titles and headings
ASCII_FONTS = {
    "standard": {
        "C": " ██████╗ \n██╔════╝ \n██║      \n██║      \n╚██████╗ \n ╚═════╝ \n",
        "I": "██╗\n██║\n██║\n██║\n██║\n╚═╝\n",
        "P": "██████╗ \n██╔══██╗\n██████╔╝\n██╔═══╝ \n██║     \n╚═╝     \n",
        "H": "██╗  ██╗\n██║  ██║\n███████║\n██╔══██║\n██║  ██║\n╚═╝  ╚═╝\n",
        "E": "███████╗\n██╔════╝\n█████╗  \n██╔══╝  \n███████╗\n╚══════╝\n",
        "R": "██████╗ \n██╔══██╗\n██████╔╝\n██╔══██╗\n██║  ██║\n╚═╝  ╚═╝\n",
        " ": "  \n  \n  \n  \n  \n  \n",
        "L": "██╗     \n██║     \n██║     \n██║     \n███████╗\n╚══════╝\n",
        "A": " █████╗ \n██╔══██╗\n███████║\n██╔══██║\n██║  ██║\n╚═╝  ╚═╝\n",
        "S": "███████╗\n██╔════╝\n███████╗\n╚════██║\n███████║\n╚══════╝\n",
        "D": "██████╗ \n██╔══██╗\n██║  ██║\n██║  ██║\n██████╔╝\n╚═════╝ \n",
        "F": "███████╗\n██╔════╝\n█████╗  \n██╔══╝  \n██║     \n╚═╝     \n",
        "G": " ██████╗ \n██╔════╝ \n██║  ███╗\n██║   ██║\n╚██████╔╝\n ╚═════╝ \n",
        "J": "     ██╗\n     ██║\n     ██║\n██   ██║\n╚█████╔╝\n ╚════╝ \n",
        "K": "██╗  ██╗\n██║ ██╔╝\n█████╔╝ \n██╔═██╗ \n██║  ██╗\n╚═╝  ╚═╝\n",
        "M": "███╗   ███╗\n████╗ ████║\n██╔████╔██║\n██║╚██╔╝██║\n██║ ╚═╝ ██║\n╚═╝     ╚═╝\n",
        "N": "███╗   ██╗\n████╗  ██║\n██╔██╗ ██║\n██║╚██╗██║\n██║ ╚████║\n╚═╝  ╚═══╝\n",
        "O": " ██████╗ \n██╔═══██╗\n██║   ██║\n██║   ██║\n╚██████╔╝\n ╚═════╝ \n",
        "Q": " ██████╗ \n██╔═══██╗\n██║   ██║\n██║▄▄ ██║\n╚██████╔╝\n ╚══▀▀═╝ \n",
        "T": "████████╗\n╚══██╔══╝\n   ██║   \n   ██║   \n   ██║   \n   ╚═╝   \n",
        "U": "██╗   ██╗\n██║   ██║\n██║   ██║\n██║   ██║\n╚██████╔╝\n ╚═════╝ \n",
        "V": "██╗   ██╗\n██║   ██║\n██║   ██║\n╚██╗ ██╔╝\n ╚████╔╝ \n  ╚═══╝  \n",
        "W": "██╗    ██╗\n██║    ██║\n██║ █╗ ██║\n██║███╗██║\n╚███╔███╔╝\n ╚══╝╚══╝ \n",
        "X": "██╗  ██╗\n╚██╗██╔╝\n ╚███╔╝ \n ██╔██╗ \n██╔╝ ██╗\n╚═╝  ╚═╝\n",
        "Y": "██╗   ██╗\n╚██╗ ██╔╝\n ╚████╔╝ \n  ╚██╔╝  \n   ██║   \n   ╚═╝   \n",
        "Z": "███████╗\n╚══███╔╝\n  ███╔╝ \n ███╔╝  \n███████╗\n╚══════╝\n",
        "0": " ██████╗ \n██╔═████╗\n██║██╔██║\n████╔╝██║\n╚██████╔╝\n ╚═════╝ \n",
        "1": " ██╗\n███║\n╚██║\n ██║\n ██║\n ╚═╝\n",
        "2": "██████╗ \n╚════██╗\n █████╔╝\n██╔═══╝ \n███████╗\n╚══════╝\n",
        "3": "██████╗ \n╚════██╗\n █████╔╝\n ╚═══██╗\n██████╔╝\n╚═════╝ \n",
        "4": "██╗  ██╗\n██║  ██║\n███████║\n╚════██║\n     ██║\n     ╚═╝\n",
        "5": "███████╗\n██╔════╝\n███████╗\n╚════██║\n███████║\n╚══════╝\n",
        "6": " ██████╗ \n██╔════╝ \n███████╗ \n██╔═══██╗\n╚██████╔╝\n ╚═════╝ \n",
        "7": "███████╗\n╚════██║\n    ██╔╝\n   ██╔╝ \n   ██║  \n   ╚═╝  \n",
        "8": " █████╗ \n██╔══██╗\n╚█████╔╝\n██╔══██╗\n╚█████╔╝\n ╚════╝ \n",
        "9": " █████╗ \n██╔══██╗\n╚██████║\n ╚═══██║\n █████╔╝\n ╚════╝ \n",
        ".": "   \n   \n   \n   \n██╗\n╚═╝\n",
        ",": "    \n    \n    \n    \n ██╗\n██╔╝\n",
        "!": "██╗\n██║\n██║\n╚═╝\n██╗\n╚═╝\n",
        "?": "██████╗ \n╚════██╗\n  ▄███╔╝\n  ▀▀══╝ \n  ██╗   \n  ╚═╝   \n",
        ":": "   \n██╗\n╚═╝\n██╗\n╚═╝\n   \n",
        ";": "   \n██╗\n╚═╝\n██╗\n╚█║\n ╚╝\n",
        "-": "      \n      \n█████╗\n╚════╝\n      \n      \n",
        "_": "        \n        \n        \n        \n███████╗\n╚══════╝\n",
        "(": " ██╗\n██╔╝\n██║ \n██║ \n╚██╗\n ╚═╝\n",
        ")": "██╗ \n╚██╗\n ██║\n ██║\n██╔╝\n╚═╝ \n",
        "[": "███╗\n██╔╝\n██║ \n██║ \n███╗\n╚══╝\n",
        "]": "███╗\n╚██║\n ██║\n ██║\n███║\n╚══╝\n",
        "{": " ██╗\n██╔╝\n███╗\n███╗\n╚██╗\n ╚═╝\n",
        "}": "██╗ \n╚██╗\n╚██╗\n╚██╗\n██╔╝\n╚═╝ \n",
        "/": "    ██╗\n   ██╔╝\n  ██╔╝ \n ██╔╝  \n██╔╝   \n╚═╝    \n",
        "\\": "██╗    \n╚██╗   \n ╚██╗  \n  ╚██╗ \n   ╚██╗\n    ╚═╝\n",
        "|": "██╗\n██║\n██║\n██║\n██║\n╚═╝\n",
        "+": "      \n  ██╗ \n█████╗\n╚════╝\n  ╚═╝ \n      \n",
        "=": "      \n█████╗\n╚════╝\n█████╗\n╚════╝\n      \n",
        "*": "      \n██╗██╗\n╚███╔╝\n╚███╔╝\n██╗██╗\n╚═╝╚═╝\n",
        "&": " ████╗  \n██╔═██╗ \n█████╔╝ \n██╔═██╗ \n████╔╝██╗\n╚═══╝ ╚═╝\n",
        "^": " ███╗ \n██╔██╗\n╚═╝╚═╝\n      \n      \n      \n",
        "%": "██╗ ██╗\n╚═╝██╔╝\n  ██╔╝ \n ██╔╝  \n██╔╝██╗\n╚═╝ ╚═╝\n",
        "$": " ██╗ \n█████╗\n╚════╝\n█████╗\n╚════╝\n ╚═╝ \n",
        "#": " ██╗ ██╗ \n████████╗\n╚██╔═██╔╝\n████████╗\n╚██╔═██╔╝\n ╚═╝ ╚═╝ \n",
        "@": " ██████╗ \n██╔═══██╗\n██║██╗██║\n██║██║██║\n╚█║████╔╝\n ╚╝╚═══╝ \n"
    },
    "small": {
        "A": " ▄▄▄· \n▐█ ▀█ \n▄█▀▀█ \n▐█ ▪▐▌\n ▀  ▀ \n",
        "B": "▄▄▄· \n▐█ ▄█\n██▀· \n▐█▪·•\n.▀   \n",
        "C": "▄▄·  \n▐█ ▌▪\n██ ▄▄\n▐███▌\n·▀▀▀ \n",
        "D": "·▄▄▄▄  \n██▪ ██ \n▐█· ▐█▌\n██. ██ \n▀▀▀▀▀• \n",
        "E": "▄▄▄ .\n▀▄.▀·\n▐▀▀▪▄\n▐█▄▄▌\n ▀▀▀ \n",
        "F": "·▄▄▄\n▐▄▄·\n█▀▀█\n▐█ ▪▐▌\n.▀  ▀\n",
        "G": " ▄▄ • \n▐█ ▀ ▪\n▄█ ▀█▄\n▐█▄▪▐█\n·▀▀▀▀ \n",
        "H": "▄ .▄\n██▪▐█\n██▀▐█\n██▌▐▀\n▀▀▀ ·\n",
        "I": "▪  \n██ \n▐█·\n▐█▌\n▀▀▀\n",
        "J": "    ▐▌\n    ▐▌\n▐█·▐█·\n▐█▌▐█▌\n▀▀▀▀▀▀\n",
        "K": "▄ •▄ \n█▌▄▌▪\n▐▀▀▄·\n▐█.█▌\n·▀  ▀\n",
        "L": "▄▄▌  \n██•  \n██▪  \n▐█▌▐▌\n.▀▀▀ \n",
        "M": "▄▄      \n██ ▪     \n▐█· ▄█▀▄ \n▐█▌▐█▌.▐▌\n▀▀▀ ·▀█▀▀ \n",
        "N": "ⁿ ▄▄  \n·██ ▐███\n▐█ ▌▐▌▐█·\n██ ██▌▐█▌\n▀▀  █▪▀▀▀\n",
        "O": " ▄▄▄· \n▐█ ▀█ \n▄█▀▀█ \n▐█ ▪▐▌\n ▀  ▀ \n",
        "P": "▄▄▄· \n▐█ ▄█\n██▀· \n▐█▪·•\n.▀   \n",
        "Q": " ▄▄▄· \n▐█ ▀█ \n▄█▀▀█ \n▐█ ▪▐▌\n ▀  ▀ \n",
        "R": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n",
        "S": "▄▄▄· \n▐█ ▀█\n▄█▀▀█\n▐█ ▪▐▌\n ▀  ▀\n",
        "T": "▄▄▄▄▄\n•██  \n ▐█.▪\n ▐█▌·\n ▀▀▀ \n",
        "U": "▄• ▄▌\n█▪██▌\n█▌▐█▌\n▐█▄█▌\n ▀▀▀ \n",
        "V": "▌ ▐·\n▪█·█▌\n▐█▐█•\n ███ \n. ▀  \n",
        "W": "▌ ▐·▌ ▐·\n▪█·█▪█·█▌\n▐█▐█▐█▐█•\n ███ ███ \n. ▀ . ▀  \n",
        "X": "▐▄• ▄\n █▌█▌▪\n ·██· \n▪▐█·█▌\n•▀▀ ▀▀\n",
        "Y": "▀▄ █·\n ▐▀▀▄ \n▐█•█▌\n▐█▄█▌\n ▀▀▀ \n",
        "Z": "▄▄▄▄▄\n•██  \n ▐█.▪\n ▐█▌·\n ▀▀▀ \n",
        " ": " \n \n \n \n \n",
        "0": " ▄▄▄· \n▐█ ▀█ \n▄█▀▀█ \n▐█ ▪▐▌\n ▀  ▀ \n",
        "1": "▄▄▌  \n██•  \n██▪  \n▐█▌▐▌\n.▀▀▀ \n",
        "2": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n",
        "3": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n",
        "4": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n",
        "5": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n",
        "6": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n",
        "7": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n",
        "8": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n",
        "9": "▄▄▄  \n▀▄ █·\n▐▀▀▄ \n▐█•█▌\n.▀  ▀\n"
    }
}

def render_ascii_text(text, font_name="standard"):
    """
    Render text using ASCII art font.
    
    Args:
        text (str): Text to render
        font_name (str): Name of the font to use
        
    Returns:
        str: ASCII art representation of the text
    """
    if font_name not in ASCII_FONTS:
        return text
        
    font = ASCII_FONTS[font_name]
    
    # Convert text to uppercase since our fonts are uppercase only
    text = text.upper()
    
    # Get the number of lines in each character
    num_lines = len(font.get("A", "").split("\n")) - 1
    
    # Initialize result lines
    result_lines = [""] * num_lines
    
    # Build each line of the result
    for char in text:
        if char in font:
            char_lines = font[char].split("\n")
            for i in range(num_lines):
                if i < len(char_lines):
                    result_lines[i] += char_lines[i]
                else:
                    result_lines[i] += " " * len(char_lines[0])
        else:
            # For characters not in the font, add spaces
            for i in range(num_lines):
                result_lines[i] += " "
    
    # Join the lines with newlines
    return "\n".join(result_lines)

def center_text(text, width=None):
    """
    Center text in the terminal.
    
    Args:
        text (str): Text to center
        width (int): Width to center within (defaults to terminal width)
        
    Returns:
        str: Centered text
    """
    if width is None:
        width, _ = get_terminal_size()
        
    lines = text.split("\n")
    centered_lines = []
    
    for line in lines:
        padding = (width - len(line)) // 2
        centered_lines.append(" " * padding + line)
        
    return "\n".join(centered_lines)

def render_title(title, centered=True):
    """
    Render a title using ASCII art.
    
    Args:
        title (str): Title to render
        centered (bool): Whether to center the title
        
    Returns:
        str: ASCII art title
    """
    ascii_title = render_ascii_text(title)
    
    if centered:
        return center_text(ascii_title)
    else:
        return ascii_title

# Test function
def test_fonts():
    """Test the ASCII fonts."""
    print("\nTesting standard font:")
    print(render_title("CIPHER CLASH"))
    
    print("\nTesting small font:")
    print(render_ascii_text("CIPHER CLASH", "small"))
    
    print("\nCentered text:")
    print(center_text("This text is centered in the terminal"))

if __name__ == "__main__":
    test_fonts()
