import pygame
from scripts.Grid import Grid, GridLogic

class BattleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Colors
        self.colors = {
            'background': (20, 20, 40),
            'panel': (30, 30, 60),
            'button': (70, 70, 120),
            'button_hover': (100, 100, 150),
            'text': (255, 255, 255),
            'heart': (255, 50, 50)
        }
        
        # Layout
        self.screen_width, self.screen_height = screen.get_size()
        self.left_width = self.screen_width * 0.35
        self.right_width = self.screen_width * 0.35
        self.center_width = self.screen_width * 0.3
        
        # Stats
        self.player_hearts = 5
        self.enemy_hearts = 3
        
        # UI Elements
        self.create_grids()
        self.create_buttons()
    
    def create_grids(self):
        """Initialize player and enemy grids"""
        grid_size = min(self.left_width * 0.8, self.screen_height * 0.2)
        grid_margin = 20
        start_y = 100
        
        # Player grids (left side)
        self.player_grids = []
        for i in range(3):
            grid = Grid(
                self.left_width * 0.1, 
                start_y + i * (grid_size + grid_margin), 
                grid_size, 
                grid_size, 
                3, 3
            )
            GridLogic.displayGrid(grid, GridLogic.generateGrid(), self.font)
            self.player_grids.append(grid)
        
        # Enemy grids (right side)
        self.enemy_grids = []
        for i in range(3):
            grid = Grid(
                self.screen_width - self.right_width * 0.1 - grid_size, 
                start_y + i * (grid_size + grid_margin), 
                grid_size, 
                grid_size, 
                3, 3
            )
            GridLogic.displayGrid(grid, GridLogic.generateGrid(), self.font)
            self.enemy_grids.append(grid)
    
    def create_buttons(self):
        """Create action buttons"""
        button_width = self.center_width * 0.6
        button_height = 50
        center_x = self.left_width + self.center_width / 2
        
        self.buttons = [
            {"rect": pygame.Rect(center_x - button_width/2, self.screen_height/2 - 70, button_width, button_height),
             "text": "Attack", "callback": lambda: print("Attacking!")},
            {"rect": pygame.Rect(center_x - button_width/2, self.screen_height/2, button_width, button_height),
             "text": "Bag", "callback": lambda: print("Opening bag...")},
            {"rect": pygame.Rect(center_x - button_width/2, self.screen_height/2 + 70, button_width, button_height),
             "text": "Run", "callback": lambda: print("Running away...")}
        ]
    
    def draw_hearts(self, count, is_player=True):
        """Draw heart indicators"""
        radius = 15
        spacing = radius * 2 + 5
        start_x = self.left_width * 0.1 if is_player else self.screen_width - self.right_width * 0.1 - count * spacing
        
        for i in range(count):
            pos_x = start_x + i * spacing
            pygame.draw.circle(self.screen, self.colors['heart'], (int(pos_x), 40), radius)
    
    def handle_events(self, event):
        """Handle UI interactions"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check buttons
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    button["callback"]()
            
            # Check grids
            for grid in self.player_grids + self.enemy_grids:
                grid.handle_event(event)
    
    def draw(self):
        """Draw all UI elements"""
        # Draw panels
        pygame.draw.rect(self.screen, self.colors['panel'], (0, 0, self.left_width, self.screen_height))
        pygame.draw.rect(self.screen, self.colors['panel'], (self.screen_width - self.right_width, 0, self.right_width, self.screen_height))
        pygame.draw.rect(self.screen, self.colors['panel'], (self.left_width, 0, self.center_width, self.screen_height))
        
        # Draw hearts
        self.draw_hearts(self.player_hearts, is_player=True)
        self.draw_hearts(self.enemy_hearts, is_player=False)
        
        # Draw grids
        for grid in self.player_grids:
            grid.draw(self.screen, self.font)
        for grid in self.enemy_grids:
            grid.draw(self.screen, self.font)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            color = self.colors['button_hover'] if is_hover else self.colors['button']
            
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, (100, 100, 100), button["rect"], 2)
            
            text_surf = self.font.render(button["text"], True, self.colors['text'])
            text_rect = text_surf.get_rect(center=button["rect"].center)
            self.screen.blit(text_surf, text_rect)
