#!/usr/bin/env python3
"""
Mind Games Project Launcher
---------------------------
Main entry point for the Mind Games application.
Presents a menu to select and launch different mind games.
"""

import os
import sys
import importlib
from mind_games_project.shared.settings import TITLE, VERSION

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the application header."""
    print("=" * 50)
    print(f"{TITLE} v{VERSION}".center(50))
    print("=" * 50)
    print("A collection of mind-bending puzzle games")
    print("=" * 50)
    print()

def list_available_games():
    """Return a list of available games."""
    games_dir = os.path.join(os.path.dirname(__file__), 'games')
    # Exclude __init__.py and __pycache__ directories
    games = [d for d in os.listdir(games_dir) 
             if os.path.isdir(os.path.join(games_dir, d)) 
             and not d.startswith('__')]
    return games

def format_game_name(game_id):
    """Convert game_id to a readable name."""
    return ' '.join(word.capitalize() for word in game_id.split('_'))

def display_menu(games):
    """Display the game selection menu."""
    print("Available Games:")
    print("-" * 20)
    for i, game in enumerate(games, 1):
        print(f"{i}. {format_game_name(game)}")
    print("-" * 20)
    print("0. Exit")
    print()

def launch_game(game_id):
    """Import and launch the selected game."""
    try:
        # Import the game's main module
        game_module = importlib.import_module(f"mind_games_project.games.{game_id}.main")
        
        # Launch the game
        clear_screen()
        print(f"Launching {format_game_name(game_id)}...")
        print()
        
        # Call the game's main function
        game_module.main()
        
    except ImportError as e:
        print(f"Error: Could not load game '{game_id}'.")
        print(f"Details: {e}")
    except AttributeError:
        print(f"Error: Game '{game_id}' does not have a main() function.")
    except Exception as e:
        print(f"An error occurred while running the game: {e}")
    
    input("\nPress Enter to return to the main menu...")

def main():
    """Main function to run the launcher."""
    while True:
        clear_screen()
        display_header()
        
        games = list_available_games()
        display_menu(games)
        
        choice = input("Select a game (0-{}): ".format(len(games)))
        
        if choice == '0':
            clear_screen()
            print("Thank you for playing Mind Games!")
            sys.exit(0)
        
        try:
            choice = int(choice)
            if 1 <= choice <= len(games):
                game_id = games[choice - 1]
                launch_game(game_id)
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except ValueError:
            print("Please enter a number.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
