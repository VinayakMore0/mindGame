"""
Maze module for Quantum Maze game.
Handles maze layout and rendering.
"""
import pygame
from config import TILE_SIZE, WALL_COLOR, FLOOR_COLOR

class Maze:
    def __init__(self, level_file):
        """Initialize the maze from a level file."""
        self.walls = []
        self.floor_tiles = []
        self.player_start = None
        self.exit_pos = None
        self.width = 0
        self.height = 0
        
        self.load_level(level_file)
    
    def load_level(self, level_file):
        """Load maze layout from a text file."""
        try:
            with open(level_file, 'r') as f:
                lines = f.readlines()
                
            self.height = len(lines)
            for y, line in enumerate(lines):
                line = line.strip()
                self.width = max(self.width, len(line))
                for x, char in enumerate(line):
                    if char == '#':
                        self.walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    elif char == '.':
                        self.floor_tiles.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    elif char == 'P':
                        self.player_start = (x * TILE_SIZE, y * TILE_SIZE)
                        self.floor_tiles.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    elif char == 'E':
                        self.exit_pos = (x * TILE_SIZE, y * TILE_SIZE)
                        self.floor_tiles.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        except FileNotFoundError:
            print(f"Error: Level file '{level_file}' not found.")
            raise
    
    def render(self, screen):
        """Draw the maze on the screen."""
        # Draw floor tiles
        for tile in self.floor_tiles:
            pygame.draw.rect(screen, FLOOR_COLOR, tile)
        
        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        
        # Draw exit if exists
        if self.exit_pos:
            exit_rect = pygame.Rect(self.exit_pos[0], self.exit_pos[1], TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), exit_rect)  # Green exit
    
    def is_wall(self, x, y):
        """Check if the given position contains a wall."""
        rect = pygame.Rect(x, y, 1, 1)
        for wall in self.walls:
            if wall.colliderect(rect):
                return True
        return False
