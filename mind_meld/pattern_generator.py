"""
Pattern generator for Mind Meld game.
Creates patterns for players to memorize.
"""
import random
from config import GRID_SIZE, PATTERN_COLORS

class PatternGenerator:
    def __init__(self):
        """Initialize the pattern generator."""
        self.current_pattern = []
        self.pattern_type = "position"  # Default pattern type
    
    def generate_position_pattern(self, length):
        """Generate a pattern of grid positions."""
        pattern = []
        used_positions = set()  # Track used positions to avoid duplicates
        
        for _ in range(length):
            # Try to find a unique position
            attempts = 0
            while attempts < 20:  # Limit attempts to prevent infinite loop
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                pos = (x, y)
                
                if pos not in used_positions:
                    pattern.append(pos)
                    used_positions.add(pos)
                    break
                
                attempts += 1
            
            # If we couldn't find a unique position after max attempts, just use any position
            if attempts >= 20 and len(pattern) < length:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                pattern.append((x, y))
        
        return pattern
    
    def generate_color_pattern(self, length):
        """Generate a pattern of colors."""
        return [random.choice(PATTERN_COLORS) for _ in range(length)]
    
    def generate_combined_pattern(self, length):
        """Generate a pattern combining positions and colors."""
        pattern = []
        for _ in range(length):
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            color = random.choice(PATTERN_COLORS)
            pattern.append(((x, y), color))
        return pattern
    
    def generate_sequence_pattern(self, length):
        """Generate a sequential pattern (e.g., 1-2-3-4)."""
        positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        random.shuffle(positions)
        return positions[:length]
    
    def generate_pattern(self, pattern_type, length):
        """Generate a pattern of the specified type and length."""
        self.pattern_type = pattern_type
        
        if pattern_type == "position":
            self.current_pattern = self.generate_position_pattern(length)
        elif pattern_type == "color":
            self.current_pattern = self.generate_color_pattern(length)
        elif pattern_type == "combined":
            self.current_pattern = self.generate_combined_pattern(length)
        elif pattern_type == "sequence":
            self.current_pattern = self.generate_sequence_pattern(length)
        else:
            # Default to position pattern
            self.current_pattern = self.generate_position_pattern(length)
        
        return self.current_pattern
    
    def get_current_pattern(self):
        """Return the current pattern."""
        return self.current_pattern
    
    def get_pattern_type(self):
        """Return the current pattern type."""
        return self.pattern_type
