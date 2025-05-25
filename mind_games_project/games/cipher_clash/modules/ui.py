"""
UI module for Cipher Clash game.
Handles user interface elements and interactions.
"""

import os
import sys
import time
from mind_games_project.games.cipher_clash.modules.font_manager import font_manager
from mind_games_project.games.cipher_clash.modules.terminal_fonts import render_title, center_text

class CipherUI:
    """User interface class for Cipher Clash game."""
    
    def __init__(self):
        """Initialize the UI."""
        self.width = 80  # Terminal width for formatting
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_intro(self):
        """Display the game introduction."""
        self.clear_screen()
        
        # Display ASCII art title
        title_art = render_title("CIPHER CLASH")
        print(title_art)
        
        # Display styled subtitle
        subtitle = font_manager.style_text("DECRYPT. SOLVE. SURVIVE.", "subtitle")
        print(center_text(subtitle))
        
        print("\n" + "=" * self.width)
        print(font_manager.style_text("Welcome to Cipher Clash, a game of cryptographic puzzles!", "info"))
        print("\nIn this game, you'll be presented with encrypted messages.")
        print("Your task is to decrypt them and enter the correct solution.")
        print("Solve as many ciphers as you can before time runs out!")
        print("\n" + font_manager.style_text("Commands:", "heading"))
        print("  - Enter your solution to solve the cipher")
        print("  - Type 'hint' to get a hint (costs 50 points, max 3 per cipher)")
        print("  - Type 'skip' to skip the current cipher (costs 100 points)")
        print("  - Type 'help' to see available commands")
        print("  - Type 'quit' to exit the game")
        print("\n" + "=" * self.width)
        input("\nPress Enter to start the game...")
        
    def display_game_state(self, cipher, score, ciphers_solved, attempts_remaining, time_remaining, hints_used=0, max_hints=3):
        """
        Display the current game state.
        
        Args:
            cipher (str): The current cipher puzzle
            score (int): Current score
            ciphers_solved (int): Number of ciphers solved
            attempts_remaining (int): Remaining attempts
            time_remaining (float): Remaining time in seconds
            hints_used (int): Number of hints used for current cipher
            max_hints (int): Maximum hints allowed per cipher
        """
        self.clear_screen()
        
        # Display header
        print("=" * self.width)
        print(font_manager.style_text("CIPHER CLASH", "title").center(self.width))
        print("=" * self.width)
        
        # Display game stats with styled text
        stats = font_manager.format_game_stats(
            score, ciphers_solved, attempts_remaining, 
            time_remaining, time_remaining * 2  # Double for time limit comparison
        )
        print(stats)
        
        # Display hints info
        hints_info = font_manager.style_text(f"Hints: {hints_used}/{max_hints}", "info")
        print(hints_info)
        
        print("-" * self.width)
        
        # Parse cipher text to separate type and content
        cipher_parts = cipher.split('\n', 1)
        if len(cipher_parts) == 2:
            cipher_type = cipher_parts[0]
            cipher_content = cipher_parts[1]
        else:
            cipher_type = "Unknown Cipher"
            cipher_content = cipher
        
        # Display the cipher with styled text
        print("\n" + font_manager.style_text("DECRYPT THIS MESSAGE:", "heading"))
        print("\n" + font_manager.style_text(cipher_type, "cipher_type"))
        print(font_manager.style_text(cipher_content, "cipher_text"))
        print("\n" + "-" * self.width)
        
    def get_player_input(self):
        """
        Get the player's solution attempt.
        
        Returns:
            str: The player's input
        """
        prompt = font_manager.format_input_prompt("\nYour solution: ")
        return input(prompt).strip()
        
    def show_success_message(self, points):
        """
        Display a success message when the player solves a cipher.
        
        Args:
            points (int): Points earned for this solution
        """
        print("\n" + "=" * self.width)
        success_message = font_manager.format_success_message("CORRECT!")
        print(success_message.center(self.width))
        points_message = font_manager.style_text(f"You earned {points} points!", "score")
        print(points_message.center(self.width))
        print("=" * self.width)
        input("\nPress Enter to continue to the next cipher...")
        
    def show_incorrect_message(self, attempts_remaining):
        """
        Display a message when the player's solution is incorrect.
        
        Args:
            attempts_remaining (int): Number of attempts remaining
        """
        error_message = font_manager.format_error_message("Incorrect solution!")
        print("\n" + error_message)
        attempts_message = font_manager.style_text(f"You have {attempts_remaining} attempts remaining.", "warning")
        print(attempts_message)
        input("\nPress Enter to try again...")
        
    def show_hint(self, hint, cost):
        """
        Display a hint to the player.
        
        Args:
            hint (str): The hint to display
            cost (int): The point cost of the hint
        """
        print("\n" + "-" * self.width)
        hint_display = font_manager.format_hint(hint, cost)
        print(hint_display)
        print("-" * self.width)
        input("\nPress Enter to continue...")
        
    def show_message(self, message):
        """
        Display a general message to the player.
        
        Args:
            message (str): The message to display
        """
        print("\n" + font_manager.style_text(message, "info"))
        input("\nPress Enter to continue...")
        
    def show_game_over(self, message, score, ciphers_solved, time_taken, high_scores=None):
        """
        Display the game over screen.
        
        Args:
            message (str): Game over message
            score (int): Final score
            ciphers_solved (int): Total ciphers solved
            time_taken (str): Time taken in MM:SS format
            high_scores (list): List of high scores for comparison
        """
        self.clear_screen()
        
        # Display game over title
        game_over_title = render_title("GAME OVER")
        print(game_over_title)
        
        print("=" * self.width)
        message_styled = font_manager.style_text(message, "warning")
        print(f"\n{message_styled}".center(self.width))
        print("\n" + "-" * self.width)
        
        # Display results with styled text
        print(font_manager.style_text("FINAL RESULTS:", "heading").center(self.width))
        print(font_manager.style_text(f"Score: {score}", "score").center(self.width))
        print(font_manager.style_text(f"Ciphers Solved: {ciphers_solved}", "info").center(self.width))
        print(font_manager.style_text(f"Time: {time_taken}", "info").center(self.width))
        print("-" * self.width)
        
        # Show high score comparison if available
        if high_scores:
            if not high_scores:
                print("\n" + font_manager.style_text("You're the first to set a high score!", "success"))
            else:
                top_score = high_scores[0]['score'] if high_scores else 0
                if score > top_score:
                    print("\n" + font_manager.style_text("Congratulations! You've set a new high score!", "success"))
                elif score > 0:
                    # Find where this score would rank
                    rank = 1
                    for hs in high_scores:
                        if score <= hs['score']:
                            rank += 1
                        else:
                            break
                    print(f"\n" + font_manager.style_text(f"Your score ranks #{rank} on the leaderboard!", "info"))
        
    def get_player_name(self):
        """
        Get the player's name for high score.
        
        Returns:
            str: The player's name
        """
        print("\n" + font_manager.style_text("You achieved a high score!", "success"))
        name_prompt = font_manager.format_input_prompt("Enter your name: ")
        name = input(name_prompt).strip()
        return name if name else "Anonymous"
