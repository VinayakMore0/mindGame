"""
Animations module for Cipher Clash.
Contains animation effects for UI elements.
"""
import pygame
import math
import random
from mind_games_project.games.cipher_clash.config import GameColors, ANIMATION_SPEEDS, SCREEN_WIDTH, SCREEN_HEIGHT

def ensure_rgba(color):
    """Convert RGB color to RGBA if needed."""
    color_list = list(color)
    if len(color_list) == 3:
        return color_list + [255]
    return color_list

def ensure_rgba(color):
    """Convert RGB color to RGBA if needed."""
    color_list = list(color)
    if len(color_list) == 3:
        return color_list + [255]
    return color_list

class TextAnimation:
    """Animated text effects."""
    
    @staticmethod
    def type_writer(surface, text, font, color, pos, speed=0.5, delay=0):
        """
        Create a typewriter animation effect.
        
        Args:
            surface: The pygame surface to draw on
            text (str): The text to animate
            font: The pygame font
            color: The text color
            pos (tuple): The position (x, y)
            speed (float): The typing speed (characters per frame)
            delay (float): The delay before starting
            
        Returns:
            bool: True if the animation is complete
        """
        if delay > 0:
            delay -= 0.1
            return False
        
        # Calculate how many characters to show
        visible_chars = min(len(text), int(pygame.time.get_ticks() * speed / 1000))
        
        # Render visible text
        visible_text = text[:visible_chars]
        text_surf = font.render(visible_text, True, color)
        text_rect = text_surf.get_rect(topleft=pos)
        surface.blit(text_surf, text_rect)
        
        # Add blinking cursor at the end
        if visible_chars < len(text):
            cursor_x = text_rect.left + font.size(visible_text)[0]
            cursor_height = font.get_linesize() - 4
            
            # Blink cursor
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                pygame.draw.line(
                    surface, 
                    color, 
                    (cursor_x, text_rect.top + 2),
                    (cursor_x, text_rect.top + cursor_height),
                    2
                )
        
        return visible_chars >= len(text)
    
    @staticmethod
    def flicker(surface, text, font, color, pos, intensity=0.5):
        """
        Create a flickering text effect.
        
        Args:
            surface: The pygame surface to draw on
            text (str): The text to animate
            font: The pygame font
            color: The text color
            pos (tuple): The position (x, y)
            intensity (float): The flicker intensity
        """
        # Base text
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)
        
        # Apply random flicker to color
        flicker_color = ensure_rgba(color)
        for i in range(3):
            flicker_color[i] = min(255, max(0, flicker_color[i] + 
                                random.randint(-int(50 * intensity), int(50 * intensity))))
        
        # Render with flickered color
        flicker_surf = font.render(text, True, flicker_color)
        surface.blit(flicker_surf, text_rect)

class GlowEffect:
    """Glow effects for UI elements."""
    
    @staticmethod
    def draw_glow_rect(surface, rect, color, intensity=1.0, pulse=True):
        """
        Draw a rectangle with a glowing effect.
        
        Args:
            surface: The pygame surface to draw on
            rect (pygame.Rect): The rectangle
            color: The glow color
            intensity (float): The glow intensity
            pulse (bool): Whether to pulse the glow
        """

        # Base rectangle
        pygame.draw.rect(surface, color, rect, border_radius=5)
        
        # Glow layers
        glow_color = ensure_rgba(color)
        
        # Pulse effect
        if pulse:
            pulse_factor = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 500)
            intensity *= pulse_factor
        
        # Draw multiple layers with decreasing alpha
        for i in range(1, 6):
            alpha = int(200 * intensity / i)
            if alpha <= 0:
                break
                
            glow_color[3] = alpha
            glow_rect = rect.inflate(i * 2, i * 2)
            pygame.draw.rect(surface, glow_color, glow_rect, border_radius=5 + i)
    
    @staticmethod
    def draw_glow_text(surface, text, font, color, pos, intensity=1.0, pulse=True):
        """
        Draw text with a glowing effect.
        
        Args:
            surface: The pygame surface to draw on
            text (str): The text to draw
            font: The pygame font
            color: The text color
            pos (tuple): The position (x, y)
            intensity (float): The glow intensity
            pulse (bool): Whether to pulse the glow
        """
        # Base text
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)
        
        # Pulse effect
        if pulse:
            pulse_factor = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 500)
            intensity *= pulse_factor
        
        # Glow layers
        glow_color = ensure_rgba(color)
        
        for i in range(1, 6):
            alpha = int(200 * intensity / i)
            if alpha <= 0:
                break

            glow_color[3] = alpha
            glow_surf = font.render(text, True, glow_color)
            glow_rect = glow_surf.get_rect(center=pos)
            glow_rect.inflate_ip(i * 2, i * 2)
            surface.blit(glow_surf, glow_rect)
        
        # Draw the main text on top
        surface.blit(text_surf, text_rect)

class ParticleEffect:
    """Particle effects for visual feedback."""
    
    def __init__(self, pos, color=GameColors.NEON_GREEN, count=20, speed=2.0, 
                 size_range=(2, 5), lifetime=1.0):
        """
        Initialize a particle effect.
        
        Args:
            pos (tuple): The position (x, y)
            color: The particle color
            count (int): The number of particles
            speed (float): The particle speed
            size_range (tuple): The min and max particle size
            lifetime (float): The effect lifetime in seconds
        """
        self.particles = []
        self.lifetime = lifetime
        self.start_time = pygame.time.get_ticks()
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_val = random.uniform(0.5, speed)
            size = random.uniform(size_range[0], size_range[1])
            
            self.particles.append({
                'pos': list(pos),
                'vel': [math.cos(angle) * speed_val, math.sin(angle) * speed_val],
                'size': size,
                'color': color,
                'alpha': 255
            })
    
    def update(self):
        """
        Update the particle effect.
        
        Returns:
            bool: True if the effect is still active
        """
        # Check if lifetime expired
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed > self.lifetime:
            return False
        
        # Update particles
        for p in self.particles:
            # Move particle
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]
            
            # Apply gravity
            p['vel'][1] += 0.1
            
            # Fade out
            fade_factor = 1.0 - (elapsed / self.lifetime)
            p['alpha'] = int(255 * fade_factor)
        
        return True
    
    def draw(self, surface):
        """
        Draw the particle effect.
        
        Args:
            surface: The pygame surface to draw on
        """
        for p in self.particles:
            # Skip if fully transparent
            if p['alpha'] <= 0:
                continue
                
            # Create particle color with alpha
            color = ensure_rgba(p['color'])
            color[3] = p['alpha']

            # Draw particle
            pygame.draw.circle(
                surface,
                color,
                (int(p['pos'][0]), int(p['pos'][1])),
                int(p['size'])
            )

class ScreenTransition:
    """Screen transition effects."""
    
    @staticmethod
    def fade(surface, next_surface, duration=0.5):
        """
        Create a fade transition between screens.
        
        Args:
            surface: The current pygame surface
            next_surface: The next pygame surface
            duration (float): The transition duration in seconds
            
        Returns:
            bool: True if the transition is complete
        """
        start_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        
        while True:
            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            progress = min(1.0, elapsed / duration)
            
            # Draw current surface with decreasing alpha
            current_alpha = int(255 * (1.0 - progress))
            current_surf = surface.copy()
            current_surf.set_alpha(current_alpha)
            
            # Draw next surface with increasing alpha
            next_alpha = int(255 * progress)
            next_surf = next_surface.copy()
            next_surf.set_alpha(next_alpha)
            
            # Draw to screen
            surface.fill((0, 0, 0))
            surface.blit(next_surf, (0, 0))
            surface.blit(current_surf, (0, 0))
            
            pygame.display.flip()
            clock.tick(60)
            
            if progress >= 1.0:
                break
        
        return True
    
    @staticmethod
    def slide(surface, next_surface, direction="left", duration=0.5):
        """
        Create a slide transition between screens.
        
        Args:
            surface: The current pygame surface
            next_surface: The next pygame surface
            direction (str): The slide direction ('left', 'right', 'up', 'down')
            duration (float): The transition duration in seconds
            
        Returns:
            bool: True if the transition is complete
        """
        start_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        
        # Set up slide parameters
        if direction == "left":
            start_pos = (SCREEN_WIDTH, 0)
            end_pos = (0, 0)
            current_start = (0, 0)
            current_end = (-SCREEN_WIDTH, 0)
        elif direction == "right":
            start_pos = (-SCREEN_WIDTH, 0)
            end_pos = (0, 0)
            current_start = (0, 0)
            current_end = (SCREEN_WIDTH, 0)
        elif direction == "up":
            start_pos = (0, SCREEN_HEIGHT)
            end_pos = (0, 0)
            current_start = (0, 0)
            current_end = (0, -SCREEN_HEIGHT)
        else:  # down
            start_pos = (0, -SCREEN_HEIGHT)
            end_pos = (0, 0)
            current_start = (0, 0)
            current_end = (0, SCREEN_HEIGHT)
        
        while True:
            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            progress = min(1.0, elapsed / duration)
            
            # Calculate positions
            current_x = current_start[0] + (current_end[0] - current_start[0]) * progress
            current_y = current_start[1] + (current_end[1] - current_start[1]) * progress
            
            next_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
            next_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
            
            # Draw to screen
            surface.fill((0, 0, 0))
            surface.blit(surface, (current_x, current_y))
            surface.blit(next_surface, (next_x, next_y))
            
            pygame.display.flip()
            clock.tick(60)
            
            if progress >= 1.0:
                break
        
        return True
