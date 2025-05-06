import pygame

class Grid(object):
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cell_width = width // cols
        self.cell_height = height // rows
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def renderGrid(self, surface):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_width
                y = row * self.cell_height
                pygame.draw.rect(surface, (255, 255, 255), (x, y, self.cell_width, self.cell_height), 1)

    def renderGridAssets(self, surface, assets):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_width
                y = row * self.cell_height
                if self.grid[row][col] != 0:
                    asset = assets[self.grid[row][col]]
                    surface.blit(asset, (x, y))
    
    def setCell(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = value
        else:
            raise IndexError("Grid index out of range")
        
    def clearGrid(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]