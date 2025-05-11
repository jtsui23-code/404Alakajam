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
from scripts.UI.UIHandler import UIHandler


# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DUNGEON DEPTHS")

# Main game loop
clock = pygame.time.Clock()
running = True

handler = UIHandler(screen)

while running:
    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    
    # Render the main menu - now just passing the screen
    handler.render('character')
    #extra line. ignore. git test 
    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()