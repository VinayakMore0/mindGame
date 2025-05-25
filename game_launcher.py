"""
Game Launcher for Mind Games Collection.
Provides an interface to select and launch any of the four games.
"""
import pygame
import sys
import os
import subprocess

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
NEON_BLUE = (0, 128, 255)
NEON_PINK = (255, 0, 128)
MATRIX_GREEN = (0, 255, 0)

# Game paths
CIPHER_CLASH_PATH = os.path.join("cipher_clash", "main.py")
QUANTUM_MAZE_PATH = os.path.join("quantum_maze", "main.py")
MIND_MELD_PATH = os.path.join("mind_meld", "main.py")
LOGIC_ARENA_PATH = os.path.join("logic_arena", "main.py")

class GameLauncher:
    def __init__(self):
        """Initialize the game launcher."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mind Games Launcher")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.title_font = pygame.font.SysFont('Arial', 48)
        self.game_font = pygame.font.SysFont('Arial', 32)
        self.info_font = pygame.font.SysFont('Arial', 20)
        
        # Game state
        self.running = True
        
        # Game buttons
        self.buttons = []
        self.create_buttons()
    
    def create_buttons(self):
        """Create buttons for each game."""
        button_width = 350
        button_height = 80
        button_margin = 30
        start_y = 150
        
        # Cipher Clash button
        cipher_clash_rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            start_y,
            button_width,
            button_height
        )
        self.buttons.append({
            "rect": cipher_clash_rect,
            "text": "Cipher Clash",
            "color": NEON_BLUE,
            "hover_color": BLUE,
            "path": CIPHER_CLASH_PATH,
            "description": "Decode ciphers and encrypted messages"
        })
        
        # Quantum Maze button
        quantum_maze_rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + button_height + button_margin,
            button_width,
            button_height
        )
        self.buttons.append({
            "rect": quantum_maze_rect,
            "text": "Quantum Maze",
            "color": MATRIX_GREEN,
            "hover_color": GREEN,
            "path": QUANTUM_MAZE_PATH,
            "description": "Navigate mazes with quantum teleportation"
        })
        
        # Mind Meld button
        mind_meld_rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + 2 * (button_height + button_margin),
            button_width,
            button_height
        )
        self.buttons.append({
            "rect": mind_meld_rect,
            "text": "Mind Meld",
            "color": PURPLE,
            "hover_color": (180, 0, 180),
            "path": MIND_MELD_PATH,
            "description": "Memorize and recreate patterns"
        })
        
        # Logic Arena button
        logic_arena_rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + 3 * (button_height + button_margin),
            button_width,
            button_height
        )
        self.buttons.append({
            "rect": logic_arena_rect,
            "text": "Logic Arena",
            "color": ORANGE,
            "hover_color": (255, 140, 0),
            "path": LOGIC_ARENA_PATH,
            "description": "Solve logic puzzles and brain teasers"
        })
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if any game button was clicked
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            self.launch_game(button["path"])
    
    def launch_game(self, game_path):
        """Launch the selected game."""
        try:
            # Get the current directory
            current_dir = os.getcwd()
            
            # Construct the full path to the game
            full_path = os.path.join(current_dir, game_path)
            
            # Launch the game using Python
            print(f"Launching game: {full_path}")
            
            # Use subprocess to run the game
            subprocess.Popen([sys.executable, full_path])
            
            # Exit the launcher
            self.running = False
            
        except Exception as e:
            print(f"Error launching game: {e}")
    
    def update(self):
        """Update game state."""
        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                button["current_color"] = button["hover_color"]
            else:
                button["current_color"] = button["color"]
    
    def render(self):
        """Render the launcher interface."""
        # Fill background
        self.screen.fill(DARK_GRAY)
        
        # Draw title
        self.draw_text("MIND GAMES", self.title_font, WHITE, 
                      SCREEN_WIDTH // 2, 60, "center")
        
        # Draw buttons
        for button in self.buttons:
            # Draw button background
            pygame.draw.rect(self.screen, button.get("current_color", button["color"]), button["rect"])
            pygame.draw.rect(self.screen, WHITE, button["rect"], 2)  # Border
            
            # Draw button text
            self.draw_text(button["text"], self.game_font, WHITE, 
                          button["rect"].centerx, button["rect"].centery - 10, "center")
            
            # Draw description
            self.draw_text(button["description"], self.info_font, WHITE, 
                          button["rect"].centerx, button["rect"].centery + 20, "center")
        
        # Draw footer
        self.draw_text("Select a game to play", self.info_font, WHITE, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40, "center")
        
        pygame.display.flip()
    
    def draw_text(self, text, font, color, x, y, align="topleft"):
        """Draw text on the screen with alignment options."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if align == "topleft":
            text_rect.topleft = (x, y)
        elif align == "center":
            text_rect.center = (x, y)
        elif align == "topright":
            text_rect.topright = (x, y)
        
        self.screen.blit(text_surface, text_rect)
    
    def run(self):
        """Main loop for the launcher."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()
