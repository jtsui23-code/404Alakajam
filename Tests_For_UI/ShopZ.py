import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Jack, if you are reading this. The only important part is 
Line 14, 29, and 38
That shows you how to use the UI module

"""
import pygame
import sys
from scripts.UI.shop import Shop


# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Medieval Dungeon Game")

# Create shop instance with screen parameter
shop = Shop(screen)

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
                # Pass other key events to the shop
                shop.handle_event(event)
    
    # Update shop state
    shop.update()
    
    # Render shop to the screen
    shop.render()
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()