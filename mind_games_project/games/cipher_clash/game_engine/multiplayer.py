"""
Multiplayer module for Cipher Clash.
Handles local multiplayer functionality.
"""

class MultiplayerManager:
    """Manages multiplayer functionality for Cipher Clash."""
    
    def __init__(self):
        """Initialize the multiplayer manager."""
        self.player1_state = None
        self.player2_state = None
        self.current_turn = 1  # 1 for player 1, 2 for player 2
        self.game_active = False
        self.winner = None
    
    def start_multiplayer_game(self, player1_state, player2_state=None):
        """
        Start a new multiplayer game.
        
        Args:
            player1_state: The game state for player 1
            player2_state: The game state for player 2 (None for AI opponent)
        """
        self.player1_state = player1_state
        self.player2_state = player2_state
        self.current_turn = 1
        self.game_active = True
        self.winner = None
        
        # Initialize both players with the same question
        question = self.player1_state.question_generator.generate_question(
            self.player1_state.difficulty
        )
        self.player1_state.current_question = question
        
        if self.player2_state:
            self.player2_state.current_question = question
    
    def switch_turn(self):
        """Switch the current turn between players."""
        if self.current_turn == 1:
            self.current_turn = 2
        else:
            self.current_turn = 1
    
    def submit_answer(self, player_num, answer):
        """
        Submit an answer for the specified player.
        
        Args:
            player_num (int): The player number (1 or 2)
            answer (str): The player's answer
            
        Returns:
            bool: True if the answer is correct
        """
        if not self.game_active:
            return False
        
        player_state = self.player1_state if player_num == 1 else self.player2_state
        
        if player_state:
            is_correct, score = player_state.question_generator.verify_answer(
                player_state.current_question, answer
            )
            
            # Update player state
            player_state.questions_answered += 1
            if is_correct:
                player_state.correct_answers += 1
                player_state.total_score += score
                
                # Generate a new question for both players
                self.generate_new_question()
            
            # Play appropriate sound
            if is_correct:
                player_state.play_sound("correct")
            else:
                player_state.play_sound("wrong")
            
            return is_correct
        
        return False
    
    def generate_new_question(self):
        """Generate a new question for both players."""
        if not self.game_active:
            return
        
        # Generate the same question for both players
        question = self.player1_state.question_generator.generate_question(
            self.player1_state.difficulty
        )
        
        self.player1_state.current_question = question
        self.player1_state.current_input = ""
        self.player1_state.hint_revealed = False
        
        if self.player2_state:
            self.player2_state.current_question = question
            self.player2_state.current_input = ""
            self.player2_state.hint_revealed = False
    
    def update_game(self):
        """Update the multiplayer game state."""
        if not self.game_active:
            return
        
        # Update timers for both players
        self.player1_state.update_timer()
        if self.player2_state:
            self.player2_state.update_timer()
        
        # Check if either player has run out of time
        if self.player1_state.game_over:
            if self.player2_state and not self.player2_state.game_over:
                self.winner = 2
            self.end_game()
        elif self.player2_state and self.player2_state.game_over:
            self.winner = 1
            self.end_game()
    
    def end_game(self):
        """End the multiplayer game."""
        self.game_active = False
        
        # Determine the winner if not already set
        if self.winner is None:
            if not self.player2_state:
                # Single player mode
                self.winner = 1
            else:
                # Compare scores
                if self.player1_state.total_score > self.player2_state.total_score:
                    self.winner = 1
                elif self.player2_state.total_score > self.player1_state.total_score:
                    self.winner = 2
                else:
                    # Tie - compare accuracy
                    p1_accuracy = self.player1_state.correct_answers / max(1, self.player1_state.questions_answered)
                    p2_accuracy = self.player2_state.correct_answers / max(1, self.player2_state.questions_answered)
                    
                    if p1_accuracy > p2_accuracy:
                        self.winner = 1
                    elif p2_accuracy > p1_accuracy:
                        self.winner = 2
                    else:
                        # Still tied - it's a draw
                        self.winner = 0  # 0 indicates a draw
        
        # Play victory music
        self.player1_state.play_music("victory")
    
    def get_results(self):
        """
        Get the multiplayer game results.
        
        Returns:
            dict: The game results
        """
        results = {
            "winner": self.winner,
            "player1": self.player1_state.get_results() if self.player1_state else None,
            "player2": self.player2_state.get_results() if self.player2_state else None
        }
        
        return results
