#!/usr/bin/env python3
import pygame
import sys
import traceback

def test_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Test")
    
    # Test drawing with RGB and RGBA colors
    rgb_color = (255, 0, 0)
    rgba_color = (0, 255, 0, 128)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        
        # Test RGB color
        pygame.draw.rect(screen, rgb_color, pygame.Rect(100, 100, 200, 200))
        
        # Test RGBA color
        pygame.draw.rect(screen, rgba_color, pygame.Rect(400, 100, 200, 200))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    try:
        test_pygame()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
