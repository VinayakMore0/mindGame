"""
Game module for Quantum Maze game.
Contains the core game loop and logic.
"""
import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from maze import Maze
from player import Player
from utils.helpers import draw_text

class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Maze")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.running = True
        self.current_level = 1
        self.load_level()
    
    def load_level(self):
        """Load the current level."""
        # Get the absolute path to the level file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        level_file = os.path.join(current_dir, "levels", f"level{self.current_level}.txt")
        try:
            self.maze = Maze(level_file)
            if self.maze.player_start:
                self.player = Player(self.maze.player_start[0], self.maze.player_start[1])
            else:
                # Default position if not specified in level
                self.player = Player(TILE_SIZE, TILE_SIZE)
        except FileNotFoundError:
            print(f"Level {self.current_level} not found. Game completed!")
            self.running = False
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle key presses for quantum abilities
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.player.store_quantum_position()
                elif event.key == pygame.K_e:
                    self.player.quantum_teleport()
    
    def update(self):
        """Update game state."""
        keys = pygame.key.get_pressed()
        
        # Handle movement
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        
        self.player.move(dx, dy, self.maze)
        self.player.recharge_energy()
        
        # Check if player reached the exit
        if self.maze.exit_pos:
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            exit_rect = pygame.Rect(self.maze.exit_pos[0], self.maze.exit_pos[1], 
                                   self.player.width, self.player.height)
            
            if player_rect.colliderect(exit_rect):
                self.current_level += 1
                self.load_level()
    
    def render(self):
        """Render the game."""
        self.screen.fill(BLACK)
        
        # Draw maze
        self.maze.render(self.screen)
        
        # Draw player
        self.player.render(self.screen)
        
        # Draw UI
        energy_text = f"Quantum Energy: {int(self.player.quantum_energy)}"
        draw_text(self.screen, energy_text, self.font, WHITE, 10, 10)
        
        level_text = f"Level: {self.current_level}"
        draw_text(self.screen, level_text, self.font, WHITE, SCREEN_WIDTH - 10, 10, "topright")
        
        # Draw controls help
        controls_text = "Q: Store Position | E: Quantum Teleport"
        draw_text(self.screen, controls_text, self.font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, "center")
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
