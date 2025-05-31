import pygame

from scripts.Grid import GridLogic

screen = pygame.display.set_mode((1280, 720))
grid = GridLogic.generateEncounterGrid(1,1)
running = True
while running:
    screen.blit(grid, (0,0))
    pygame.display.flip()