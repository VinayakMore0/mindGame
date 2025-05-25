"""
Player module for Quantum Maze game.
Handles player movement and quantum actions.
"""
import pygame
import random
from config import TILE_SIZE, PLAYER_COLOR, PLAYER_SPEED

class Player:
    def __init__(self, x, y):
        """Initialize the player at the given position."""
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.speed = PLAYER_SPEED
        self.quantum_energy = 100  # Energy for quantum abilities
        
        # For quantum teleportation
        self.quantum_positions = []
        self.max_quantum_positions = 3
    
    def move(self, dx, dy, maze):
        """Move the player if there's no wall in the way."""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Check for collisions with walls
        if not self.check_collision(new_x, new_y, maze):
            self.x = new_x
            self.y = new_y
    
    def check_collision(self, x, y, maze):
        """Check if the player would collide with a wall."""
        # Create a smaller hitbox for the player (80% of original size)
        hitbox_reduction = int(self.width * 0.1)  # 10% reduction on each side
        
        # Calculate the reduced hitbox coordinates
        hitbox_x = x + hitbox_reduction
        hitbox_y = y + hitbox_reduction
        hitbox_width = self.width - (hitbox_reduction * 2)
        hitbox_height = self.height - (hitbox_reduction * 2)
        
        # Check corners of the reduced hitbox
        corners = [
            (hitbox_x, hitbox_y),  # Top-left
            (hitbox_x + hitbox_width, hitbox_y),  # Top-right
            (hitbox_x, hitbox_y + hitbox_height),  # Bottom-left
            (hitbox_x + hitbox_width, hitbox_y + hitbox_height)  # Bottom-right
        ]
        
        # Check center points of each edge for better collision detection
        edges = [
            (hitbox_x + hitbox_width // 2, hitbox_y),  # Top center
            (hitbox_x + hitbox_width, hitbox_y + hitbox_height // 2),  # Right center
            (hitbox_x + hitbox_width // 2, hitbox_y + hitbox_height),  # Bottom center
            (hitbox_x, hitbox_y + hitbox_height // 2)  # Left center
        ]
        
        # Check all points for collision
        for point_x, point_y in corners + edges:
            if maze.is_wall(point_x, point_y):
                return True
        return False
    
    def store_quantum_position(self):
        """Store current position for quantum teleportation."""
        if len(self.quantum_positions) >= self.max_quantum_positions:
            self.quantum_positions.pop(0)  # Remove oldest position
        
        self.quantum_positions.append((self.x, self.y))
        self.quantum_energy -= 20  # Use energy to store position
    
    def quantum_teleport(self):
        """Teleport to a previously stored quantum position."""
        if not self.quantum_positions or self.quantum_energy < 30:
            return False
        
        # Teleport to a random stored position
        position = random.choice(self.quantum_positions)
        self.x, self.y = position
        self.quantum_energy -= 30  # Use energy to teleport
        return True
    
    def render(self, screen):
        """Draw the player on the screen."""
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    
    def recharge_energy(self):
        """Slowly recharge quantum energy."""
        if self.quantum_energy < 100:
            self.quantum_energy += 0.1  # Slow recharge rate
