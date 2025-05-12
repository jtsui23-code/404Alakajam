import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Ignore lines above ^^^^

"""

## In your main game file
import pygame

from scripts.UI.shop import Shop
# main.py - Demonstrates how to use the Shop class

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Medieval Dungeon Shop Demo")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)

# Set up the font
font = pygame.font.SysFont('Arial', 24)

# Game state
shop_visible = False
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Toggle shop visibility with SPACE key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shop_visible = not shop_visible
                if not shop_visible:
                    Shop.clear(screen)
        
        # If shop is visible, let it handle events
        if shop_visible:
            Shop.handle_event(event)
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Draw game elements
    if shop_visible:
        # Render the shop UI
        Shop.render(screen)
    else:
        # Draw instructions when shop is not visible
        instructions = [
            "Medieval Dungeon Shop Demo",
            "",
            "Press SPACE to toggle shop visibility",
            "When shop is open:",
            "- UP/DOWN arrows to select items",
            "- ENTER to purchase selected item",
            "- ESC to close the shop"
        ]
        
        for i, line in enumerate(instructions):
            text = font.render(line, True, WHITE if i == 0 else GOLD if i > 2 else WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, 150 + i * 40))
            screen.blit(text, text_rect)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()