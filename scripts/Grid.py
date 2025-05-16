import pygame
import random

class Grid:
    def __init__(self, x, y, width, height, rows, cols):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.cell_width = width // cols
        self.cell_height = height // rows
        self.cells = [[None for _ in range(cols)] for _ in range(rows)]

    def fill_cell(self, row, col, text, font, callback):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            rect = pygame.Rect(
                self.x + col * self.cell_width + 2,
                self.y + row * self.cell_height + 2,
                self.cell_width - 4,
                self.cell_height - 4
            )
            self.cells[row][col] = {
                "rect": rect,
                "text": text,
                "image": None,
                "callback": callback
            }

    def fill_cell_with_image(self, row, col, image_surface, callback):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            rect = pygame.Rect(
                self.x + col * self.cell_width + 2,
                self.y + row * self.cell_height + 2,
                self.cell_width - 4,
                self.cell_height - 4
            )
            self.cells[row][col] = {
                "rect": rect,
                "text": None,
                "image": image_surface,
                "callback": callback
            }

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        dungeon_color = (30, 30, 30)
        border_color = (70, 70, 70)
        hover_color = (90, 0, 0)
        button_color = (60, 0, 0)
        text_color = (220, 220, 220)

        for row in range(self.rows):
            for col in range(self.cols):
                base_rect = pygame.Rect(
                    self.x + col * self.cell_width,
                    self.y + row * self.cell_height,
                    self.cell_width,
                    self.cell_height
                )
                pygame.draw.rect(surface, dungeon_color, base_rect)
                pygame.draw.rect(surface, border_color, base_rect, 2)

                cell = self.cells[row][col]
                if cell:
                    is_hover = cell["rect"].collidepoint(mouse_pos)
                    color = hover_color if is_hover else button_color
                    pygame.draw.rect(surface, color, cell["rect"])
                    pygame.draw.rect(surface, border_color, cell["rect"], 2)

                    if cell["image"]:
                        img = pygame.transform.scale(cell["image"], cell["rect"].size)
                        surface.blit(img, cell["rect"].topleft)
                    elif cell["text"]:
                        text_surf = font.render(cell["text"], True, text_color)
                        text_rect = text_surf.get_rect(center=cell["rect"].center)
                        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for row in range(self.rows):
                for col in range(self.cols):
                    cell = self.cells[row][col]
                    if cell and cell["rect"].collidepoint(pos):
                        cell["callback"]()


class GridLogic:
    @staticmethod
    def generateGrid():
        arr = [['B', 'R', 'S'],[ 'R', 'X', 'R'], ['B' , 'R', 'U']]
        arr[0][1] = 'B' if random.randint(1,100) > 66 else 'X'
        arr[1][0] = 'B' if random.randint(1,100) > 66 else 'X'
        arr[1][2] = 'B' if random.randint(1,100) > 66 else 'X'
        arr[2][1] = 'B' if random.randint(1,100) > 66 else 'X'

        return arr

    

    @staticmethod
    def displayGrid(grid, arr, font):
        for i in range(3):
            for j in range(3):
                grid.fill_cell(i,j,arr[i][j],font, lambda: print("Hello"))

    @staticmethod
    def setGridCallback(grid, row, col, callback):
        grid.cells[row][col]["callback"] = callback
            
