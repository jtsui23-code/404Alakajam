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
        
        # Add selection tracking
        self.selected_cell = None  # Will store (row, col) of selected cell
        self.glow_animation_time = 0  # For animated glow effect

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

    def set_selected_cell(self, row, col):
        """Set which cell is currently selected"""
        self.selected_cell = (row, col)

    def clear_selection(self):
        """Clear the current selection"""
        self.selected_cell = None

    def update_glow_animation(self, dt):
        """Update the glow animation timer"""
        self.glow_animation_time += dt

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        dungeon_color = (30, 30, 30)
        border_color = (70, 70, 70)
        hover_color = (90, 0, 0)
        button_color = (60, 0, 0)
        text_color = (220, 220, 220)
        
        # Selection glow colors
        glow_base_color = (255, 215, 0)  # Gold color
        glow_intensity = abs(pygame.math.Vector2(1, 0).rotate(self.glow_animation_time * 180).x)
        glow_alpha = int(128 + 100 * glow_intensity)  # Animate between 128-228

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
                    is_selected = self.selected_cell == (row, col)
                    
                    color = hover_color if is_hover else button_color
                    pygame.draw.rect(surface, color, cell["rect"])
                    pygame.draw.rect(surface, border_color, cell["rect"], 2)

                    # Draw selection glow effect
                    if is_selected:
                        # Create multiple glow layers for better effect
                        glow_rect = cell["rect"].inflate(8, 8)
                        
                        # Outer glow (thicker, more transparent)
                        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                        glow_color_outer = (*glow_base_color, max(50, glow_alpha // 3))
                        pygame.draw.rect(glow_surface, glow_color_outer, glow_surface.get_rect(), 4)
                        surface.blit(glow_surface, glow_rect.topleft)
                        
                        # Inner glow (thinner, more opaque)
                        glow_rect_inner = cell["rect"].inflate(4, 4)
                        glow_surface_inner = pygame.Surface((glow_rect_inner.width, glow_rect_inner.height), pygame.SRCALPHA)
                        glow_color_inner = (*glow_base_color, min(255, glow_alpha))
                        pygame.draw.rect(glow_surface_inner, glow_color_inner, glow_surface_inner.get_rect(), 3)
                        surface.blit(glow_surface_inner, glow_rect_inner.topleft)

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
                        # Set this cell as selected when clicked
                        self.set_selected_cell(row, col)
                        cell["callback"]()


class GridLogic:

    @staticmethod
    def generateGrid():
        # Initialize with default values
        grid = [['B', 'R', 'S'], ['R', 'X', 'R'], ['B', 'R', 'U']]

        # Flatten the grid to 1D to easily access by index
        flat_grid = [cell for row in grid for cell in row]

        # Indices to randomize: 1, 3, 5, 7
        indices_to_randomize = [1, 3, 5, 7]
        for i in indices_to_randomize:
            flat_grid[i] = 'X' if random.random() < 0.66 else 'B'

        # Convert back to 3x3 grid
        randomized_grid = [flat_grid[i:i + 3] for i in range(0, 9, 3)]
        return randomized_grid

   
    @staticmethod
    def chooseCell(grid):
        row = random.randint(0,2)
        col = random.randint(0,2)
        return grid[row][col]
   
    @staticmethod
    def displayGrid(grid, arr, font):
        for i in range(3):
            for j in range(3):
                grid.fill_cell(i,j,arr[i][j],font, lambda r=i, c=j: grid.set_selected_cell(r, c))

    @staticmethod
    def setGridCallback(grid, row, col, callback):
        grid.cells[row][col]["callback"] = callback