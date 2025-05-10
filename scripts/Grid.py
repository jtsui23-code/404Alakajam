import pygame
import random
# from Item import Item

pygame.init()

class Grid:
    def __init__(self, width: int, height: int, x: int, y: int, upgrade_available: bool = False):
        self.rows = 3
        self.cols = 3
        self.width = width
        self.height = height
        self.cell_width = width // self.cols
        self.cell_height = height // self.rows
        self.x = x
        self.y = y
        self.upgrade_available = upgrade_available
        self.grid = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.assets = {}
        self._initialize_grid()
        self.font = pygame.font.Font(None, 24)

    def _initialize_grid(self):
        """Initializes the battle grid with fixed and random elements."""
        # Middle cell is always 'X' (miss)
        self.grid[1][1] = 'X'
        # Corner cells
        self.grid[0][0] = 'U' if self.upgrade_available else 'B' # Potential to be upgraded, if not just basic
        self.grid[0][2] = 'S' # Always special
        self.grid[2][0] = 'B' # Always attack
        self.grid[2][2] = 'B' # Always attack

        # Remaining four cells have a random chance (66% 'X', 33% 'BASIC')
        for r in [0, 1, 2]:
            for c in [0, 1, 2]:
                if (r, c) not in [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2)]:
                    if random.random() < 0.33:
                        self.grid[r][c] = 'B'
                    else:
                        self.grid[r][c] = 'X'

    def load_assets(self, asset_map: dict):
        self.assets = asset_map # For terminal testing, just store the map

    def get_random_cell_coordinates(self):
        """Returns random row and column indices within the grid."""
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)
        return row, col

    def get_action_at(self, row: int, col: int) -> str:
        """Returns the action type at the specified grid cell."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        else:
            raise IndexError("Grid index out of range")

# Part of the testing process
    def __str__(self):
        """String representation of the grid for terminal output."""
        output = "Grid:\n"
        for row in self.grid:
            output += "| " + " | ".join(cell.ljust(14) for cell in row) + " |\n"
            output += "-" * (17 * self.cols + 1) + "\n"
        output += f"Position: (x={self.x}, y={self.y})\n"
        output += f"Cell Dimensions: {self.cell_width}x{self.cell_height}\n"
        output += f"Assets Loaded: {self.assets}\n"
        return output


# Just testing from Gemini to see if Grid works in terminal
if __name__ == "__main__":
    test_grid_no_upgrade = Grid(200, 200, 50, 50)
    print("Grid without upgrade:")
    print(test_grid_no_upgrade)
    print("-" * 30)

    test_grid_with_upgrade = Grid(200, 200, 300, 50, upgrade_available=True)
    print("Grid with upgrade:")
    print(test_grid_with_upgrade)
    print("-" * 30)

    asset_map = {
        'B': 'assets/basic.png',
        'U': 'assets/upgrade.png',
        'S': 'assets/special.png',
        'X': 'assets/miss.png'
    }
    test_grid_with_assets = Grid(200, 200, 50, 300)
    test_grid_with_assets.load_assets(asset_map)
    print("Grid with assets loaded:")
    print(test_grid_with_assets)
    print("-" * 30)

    # Test random cell selection
    print("Testing random cell selection:")
    for _ in range(5):
        row, col = test_grid_no_upgrade.get_random_cell_coordinates()
        action = test_grid_no_upgrade.get_action_at(row, col)
        print(f"Randomly selected cell ({row}, {col}): Action = {action}")