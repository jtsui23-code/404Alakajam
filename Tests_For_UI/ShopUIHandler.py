import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Jack, if you are reading this. The only important part is 
Line 12, 22, and 42
That shows you how to use the UI module

"""
import pygame
import sys
from scripts.UI.UIHandler import UIHandler

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Medieval Dungeon Game")

handler = UIHandler(screen)

# Create shop instance with screen parameter

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                pass
    
    # Update shop state
    handler.render('shop')

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()