import pygame
import random
from Item import Item  # Assuming Item.py exists in the same directory

pygame.init()

class Grid:
    def __init__(self, rows: int, cols: int, width: int, height: int):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cell_width = width // cols
        self.cell_height = height // rows
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def render_grid_lines(self, surface: pygame.Surface, color: tuple = (255, 255, 255)):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_width
                y = row * self.cell_height
                pygame.draw.rect(surface, color, (x, y, self.cell_width, self.cell_height), 1)

    def render_grid_assets(self, surface: pygame.Surface, assets: dict):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_width
                y = row * self.cell_height
                cell_value = self.grid[row][col]
                if cell_value != 0 and cell_value in assets:
                    asset = assets[cell_value]
                    surface.blit(asset, (x, y))

    def set_cell(self, row: int, col: int, value: int):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = value
        else:
            raise IndexError("Grid index out of range")

    def get_cell_value(self, row: int, col: int) -> int:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        else:
            raise IndexError("Grid index out of range")

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_grid_size(self) -> tuple[int, int]:
        return self.rows, self.cols

    def get_cell_dimensions(self) -> tuple[int, int]:
        return self.cell_width, self.cell_height

    def get_cell_center_position(self, row: int, col: int) -> tuple[int, int]:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            x = col * self.cell_width + self.cell_width // 2
            y = row * self.cell_height + self.cell_height // 2
            return x, y
        else:
            raise IndexError("Grid index out of range")

# Example usage (add this to the end of Grid.py)
if __name__ == "__main__":
    WIDTH, HEIGHT = 600, 400
    ROWS, COLS = 30, 20
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid")

    grid = Grid(ROWS, COLS, WIDTH, HEIGHT)

    # Example of setting a cell value
    grid.set_cell(5, 10, 1)

    # Example of loading an asset (assuming you have a 'red_square.png' and Item class works)
    assets = {1: pygame.Surface((grid.cell_width, grid.cell_height))}
    assets[1].fill((100, 100, 100))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        SCREEN.fill((255, 255, 255))
        grid.render_grid_lines(SCREEN)
        grid.render_grid_assets(SCREEN, assets)
        pygame.display.flip()

    pygame.quit()