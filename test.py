import pygame
import sys
from scripts.UI.UIHandler import UIHandler
from scripts.Grid import Grid
import pygame
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 18)

# Dummy image placeholder
image = pygame.Surface((32, 32))
image.fill((200, 50, 50))

# Create two independent grids
grid1 = Grid(50, 50, 300, 200, 3, 4)
grid2 = Grid(400, 100, 300, 200, 2, 3)

def say_hello():
    print("Grid 1 action")

def other_action():
    print("Grid 2 action")

grid1.fill_cell(0, 0, "Play", font, say_hello)
grid1.fill_cell_with_image(1, 2, image, say_hello)

grid2.fill_cell(0, 0, "Exit", font, other_action)
grid2.fill_cell_with_image(1, 1, image, other_action)

running = True
while running:
    screen.fill((10, 10, 10))

    # Draw all grids
    grid1.draw(screen, font)
    grid2.draw(screen, font)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pass events to each grid
        grid1.handle_event(event)
        grid2.handle_event(event)

    pygame.display.flip()

pygame.quit()
