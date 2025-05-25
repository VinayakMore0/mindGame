"""
Main entry point for the Cipher Clash game.
"""
import os
import sys
import pygame
from pygame.locals import *

# Add the parent directory to sys.path to allow importing shared modules
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from mind_games_project.games.cipher_clash.config import *
from mind_games_project.games.cipher_clash.ui.screens import MenuScreen, GameScreen, ResultScreen
from mind_games_project.games.cipher_clash.game_engine.game_logic import GameState

class CipherClashGame:
    """Main game class for Cipher Clash."""
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        pygame.mixer.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"{GAME_TITLE} v{GAME_VERSION}")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Initialize game state
        self.game_state = GameState()
        
        # Initialize screens
        self.menu_screen = MenuScreen(self.screen, self.game_state)
        self.game_screen = GameScreen(self.screen, self.game_state)
        self.result_screen = ResultScreen(self.screen, self.game_state)
        
        # Set current screen to menu
        self.current_screen = self.menu_screen
        
        # Load fonts
        self.load_fonts()
        
        # Load sounds
        self.load_sounds()
    
    def load_fonts(self):
        """Load game fonts."""
        try:
            # Try to load custom fonts if available
            pygame.font.init()
            
            # Check if custom fonts exist in the assets directory
            monospace_path = os.path.join(FONTS_DIR, "SourceCodePro-Regular.ttf")
            display_path = os.path.join(FONTS_DIR, "Orbitron-Bold.ttf")
            
            if os.path.exists(monospace_path):
                pygame.font.Font(monospace_path, FONT_SIZE_MEDIUM)
            
            if os.path.exists(display_path):
                pygame.font.Font(display_path, FONT_SIZE_MEDIUM)
                
        except Exception as e:
            print(f"Error loading fonts: {e}")
            print("Using system fonts instead.")
    
    def load_sounds(self):
        """Load game sounds."""
        try:
            pygame.mixer.init()
            
            # Load sound effects if they exist
            for sound_name, sound_file in SOUND_EFFECTS.items():
                sound_path = os.path.join(SOUNDS_DIR, sound_file)
                if os.path.exists(sound_path):
                    self.game_state.sounds[sound_name] = pygame.mixer.Sound(sound_path)
            
            # Load music tracks if they exist
            for track_name, track_file in MUSIC_TRACKS.items():
                track_path = os.path.join(SOUNDS_DIR, track_file)
                if os.path.exists(track_path):
                    self.game_state.music_tracks[track_name] = track_path
                    
        except Exception as e:
            print(f"Error loading sounds: {e}")
            print("Continuing without sound.")
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        # ESC key returns to menu from any screen
                        if self.current_screen != self.menu_screen:
                            self.current_screen = self.menu_screen
                        else:
                            running = False
                
                # Pass event to current screen
                self.current_screen.handle_event(event)
            
            # Update current screen
            next_screen = self.current_screen.update()
            
            # Change screen if needed
            if next_screen == "menu":
                self.current_screen = self.menu_screen
            elif next_screen == "game":
                self.game_screen.reset()
                self.current_screen = self.game_screen
            elif next_screen == "result":
                self.result_screen.update_results()
                self.current_screen = self.result_screen
            
            # Draw current screen
            self.current_screen.draw()
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        # Clean up
        pygame.quit()

# This is the main function that will be imported by the launcher
def main():
    """Entry point for the game."""
    game = CipherClashGame()
    game.run()

if __name__ == "__main__":
    main()
