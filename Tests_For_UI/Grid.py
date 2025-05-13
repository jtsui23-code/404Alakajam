import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Ignore lines above ^^^^

"""
from scripts.Grid import Grid

import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont(None, 18)


grid = Grid(x=50, y=50, width=500, height=300, rows=3, cols=3)

def say_hello():
    print("Clicked button!")

# Load and scale your pixel image (replace with actual file path)
#image = pygame.image.load("skull.png").convert_alpha()  # Example: 32x32 pixel sprite

grid.fill_cell(0, 0, "Start", font, say_hello)
#grid.fill_cell_with_image(1, 1, image, say_hello)

running = True
while running:
    screen.fill((10, 10, 10))
    grid.draw(screen, font)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        grid.handle_event(event)

    pygame.display.flip()

pygame.quit()
