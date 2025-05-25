"""
Animation module for Cipher Clash game.
Contains functions for creating visual effects and animations.
"""

import os
import time
import random
import sys

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typing_effect(text, speed=0.05, flicker_chance=0.1, color="green"):
    """
    Display text with a typing effect and random flickering.
    
    Args:
        text (str): The text to display
        speed (float): Typing speed (seconds per character)
        flicker_chance (float): Probability of flickering (0.0 to 1.0)
        color (str): Text color ("green", "red", "blue", "cyan", "yellow", "magenta")
    """
    # ANSI color codes
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "yellow": "\033[93m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }
    
    # Use the selected color or default to green
    color_code = colors.get(color.lower(), colors["green"])
    
    # Type out each character with potential flicker
    for char in text:
        # Print the character with color
        sys.stdout.write(f"{color_code}{char}{colors['reset']}")
        sys.stdout.flush()
        
        # Random delay to simulate variable typing speed
        char_delay = speed * random.uniform(0.5, 1.5)
        time.sleep(char_delay)
        
        # Random flicker effect
        if random.random() < flicker_chance:
            # Briefly turn off the last character
            sys.stdout.write("\b ")
            sys.stdout.flush()
            time.sleep(0.05)
            # Turn it back on
            sys.stdout.write(f"\b{color_code}{char}{colors['reset']}")
            sys.stdout.flush()
            time.sleep(0.05)

def title_animation():
    """Display the Cipher Clash title with a typing and flickering effect."""
    clear_screen()
    
    # Create a terminal-style border
    width = 60
    print("\n" + "=" * width)
    
    # Center position for the title
    title = "CIPHER CLASH"
    padding = (width - len(title)) // 2
    
    # Print spaces to center the title
    sys.stdout.write(" " * padding)
    
    # Type out the title with flickering effect
    typing_effect(title, speed=0.1, flicker_chance=0.15, color="green")
    
    print("\n" + "=" * width)
    
    # Add a subtitle with a different effect
    subtitle = "DECRYPT. SOLVE. SURVIVE."
    subtitle_padding = (width - len(subtitle)) // 2
    
    # Small pause before subtitle
    time.sleep(0.5)
    
    # Print spaces to center the subtitle
    sys.stdout.write(" " * subtitle_padding)
    
    # Type out the subtitle with a different color and less flickering
    typing_effect(subtitle, speed=0.05, flicker_chance=0.05, color="cyan")
    
    # Final pause to appreciate the title
    print("\n")
    time.sleep(1)

def countdown_animation(seconds=3):
    """
    Display a countdown animation.
    
    Args:
        seconds (int): Number of seconds to count down from
    """
    for i in range(seconds, 0, -1):
        clear_screen()
        print("\n\n")
        print(f"{i}".center(60))
        time.sleep(1)
    
    clear_screen()
    print("\n\n")
    print("GO!".center(60))
    time.sleep(0.5)

def success_animation():
    """Display an animation for successfully solving a cipher."""
    # Define the success message frames
    frames = [
        "  ✓  ",
        " ✓✓✓ ",
        "✓✓✓✓✓"
    ]
    
    # Display each frame
    for frame in frames:
        clear_screen()
        print("\n\n")
        print(frame.center(60))
        time.sleep(0.2)
    
    # Display success message
    clear_screen()
    print("\n\n")
    print("DECRYPTED!".center(60))
    time.sleep(1)

def failure_animation():
    """Display an animation for failing to solve a cipher."""
    # Define the failure message frames
    frames = [
        "  ×  ",
        " ××× ",
        "×××××"
    ]
    
    # Display each frame
    for frame in frames:
        clear_screen()
        print("\n\n")
        print(frame.center(60))
        time.sleep(0.2)
    
    # Display failure message
    clear_screen()
    print("\n\n")
    print("ENCRYPTION FAILED!".center(60))
    time.sleep(1)

def matrix_rain(duration=3, density=0.2):
    """
    Display a Matrix-style digital rain animation.
    
    Args:
        duration (float): Duration in seconds
        density (float): Character density (0.0 to 1.0)
    """
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines
    
    # Matrix characters (katakana and other symbols)
    chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890!@#$%^&*()_+-=[]{}|;':,./<>?"
    
    # Green color for Matrix effect
    green = "\033[92m"
    bright_green = "\033[1;92m"
    reset = "\033[0m"
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        # Create a screen buffer
        screen = [[" " for _ in range(width)] for _ in range(height)]
        
        # Fill with random characters based on density
        for y in range(height):
            for x in range(width):
                if random.random() < density:
                    # Randomly choose between normal and bright green
                    color = bright_green if random.random() < 0.3 else green
                    screen[y][x] = f"{color}{random.choice(chars)}{reset}"
        
        # Clear screen and display the buffer
        clear_screen()
        for row in screen:
            print("".join(row))
        
        # Short delay
        time.sleep(0.1)

if __name__ == "__main__":
    # Test the animations
    title_animation()
    time.sleep(1)
    countdown_animation()
    success_animation()
    time.sleep(1)
    failure_animation()
    time.sleep(1)
    matrix_rain(duration=3)
