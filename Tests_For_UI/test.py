import pygame
import sys
from scripts.UI.UIHandler import UIHandler
from scripts.Grid import Grid
from scripts.Grid import GridLogic
import pygame
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont(None, 18)

# Dummy image placeholder
image = pygame.Surface((32, 32))
image.fill((200, 50, 50))

# Create two independent grids
grid1 = Grid(50, 50, 300, 200, 3, 3)
grid2 = Grid(500, 50, 300, 200, 3, 3)
grid3 = Grid(50, 500, 300, 200, 3, 3)
grid4 = Grid(500, 500, 300, 200, 3, 3)



def say_hello():
    print("Grid 1 action")

def other_action():
    print("Grid 2 action")

grid1.fill_cell(0, 0, "Play", font, say_hello)
grid1.fill_cell_with_image(1, 2, image, say_hello)

grid2.fill_cell(0, 0, "Exit", font, other_action)
grid2.fill_cell_with_image(1, 1, image, other_action)

GridLogic.displayGrid(grid1, GridLogic.generateGrid(), font)
GridLogic.displayGrid(grid2, GridLogic.generateGrid(), font)
GridLogic.displayGrid(grid3, GridLogic.generateGrid(), font)
GridLogic.displayGrid(grid4, GridLogic.generateGrid(), font)

GridLogic.setGridCallback(grid1, 0,0,lambda: print("This callback has been changed!"))


running = True
while running:

    screen.fill((10, 10, 10))

    # Draw all grids
    grid1.draw(screen, font)
    grid2.draw(screen, font)
    grid3.draw(screen, font)
    grid4.draw(screen, font)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pass events to each grid
        grid1.handle_event(event)
        grid2.handle_event(event)

    pygame.display.flip()

pygame.quit()
