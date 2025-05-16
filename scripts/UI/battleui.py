import pygame
from scripts.Grid import Grid, GridLogic

class BattleScreen:
    screen = None
    font = None  # Will be initialized in init()
    
    # Colors
    colors = {
        'background': (20, 20, 40),
        'panel': (30, 30, 60),
        'button': (70, 70, 120),
        'button_hover': (100, 100, 150),
        'text': (255, 255, 255),
        'heart': (255, 50, 50)
    }
    
    # Layout
    screen_width = 0
    screen_height = 0
    left_width = 0
    right_width = 0
    center_width = 0
    
    # Stats
    player_hearts = 5
    enemy_hearts = 3
    
    # UI Elements
    player_grids = []
    enemy_grids = []
    buttons = []

    @classmethod
    def init(cls, screen):
        """Initialize the static class with screen information"""
        cls.screen = screen
        cls.font = pygame.font.SysFont('Arial', 24)  # Default font initialization
        cls.screen_width, cls.screen_height = screen.get_size()
        cls.left_width = cls.screen_width * 0.35
        cls.right_width = cls.screen_width * 0.35
        cls.center_width = cls.screen_width * 0.3
        
        cls.create_grids()
        cls.create_buttons()

    @classmethod
    def create_grids(cls):
        """Initialize player and enemy grids with default font"""
        grid_size = min(cls.left_width * 0.8, cls.screen_height * 0.2)
        grid_margin = 20
        start_y = 100
        
        # Player grids (left side)
        cls.player_grids = []
        for i in range(3):
            grid = Grid(
                cls.left_width * 0.1, 
                start_y + i * (grid_size + grid_margin), 
                grid_size, 
                grid_size, 
                3, 3
            )
            GridLogic.displayGrid(grid, GridLogic.generateGrid(), cls.font)
            cls.player_grids.append(grid)
        
        # Enemy grids (right side)
        cls.enemy_grids = []
        for i in range(3):
            grid = Grid(
                cls.screen_width - cls.right_width * 0.1 - grid_size, 
                start_y + i * (grid_size + grid_margin), 
                grid_size, 
                grid_size, 
                3, 3
            )
            GridLogic.displayGrid(grid, GridLogic.generateGrid(), cls.font)
            cls.enemy_grids.append(grid)

    @classmethod
    def create_buttons(cls):
        """Create action buttons with default font"""
        button_width = cls.center_width * 0.6
        button_height = 50
        center_x = cls.left_width + cls.center_width / 2
        
        cls.buttons = [
            {"rect": pygame.Rect(center_x - button_width/2, cls.screen_height/2 - 70, button_width, button_height),
             "text": "Attack", "callback": lambda: print("Attacking!")},
            {"rect": pygame.Rect(center_x - button_width/2, cls.screen_height/2, button_width, button_height),
             "text": "Bag", "callback": lambda: print("Opening bag...")},
            {"rect": pygame.Rect(center_x - button_width/2, cls.screen_height/2 + 70, button_width, button_height),
             "text": "Run", "callback": lambda: print("Running away...")}
        ]

    @classmethod
    def draw_hearts(cls, count, is_player=True):
        """Draw heart indicators"""
        radius = 15
        spacing = radius * 2 + 5
        start_x = cls.left_width * 0.1 if is_player else cls.screen_width - cls.right_width * 0.1 - count * spacing
        
        for i in range(count):
            pos_x = start_x + i * spacing
            pygame.draw.circle(cls.screen, cls.colors['heart'], (int(pos_x), 40), radius)

    @classmethod
    def handle_events(cls, event):
        """Handle UI interactions"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check buttons
            for button in cls.buttons:
                if button["rect"].collidepoint(event.pos):
                    button["callback"]()
            
            # Check grids
            for grid in cls.player_grids + cls.enemy_grids:
                grid.handle_event(event)

    @classmethod
    def draw(cls):
        """Draw all UI elements"""
        # Draw panels
        pygame.draw.rect(cls.screen, cls.colors['panel'], (0, 0, cls.left_width, cls.screen_height))
        pygame.draw.rect(cls.screen, cls.colors['panel'], (cls.screen_width - cls.right_width, 0, cls.right_width, cls.screen_height))
        pygame.draw.rect(cls.screen, cls.colors['panel'], (cls.left_width, 0, cls.center_width, cls.screen_height))
        
        # Draw hearts
        cls.draw_hearts(cls.player_hearts, is_player=True)
        cls.draw_hearts(cls.enemy_hearts, is_player=False)
        
        # Draw grids
        for grid in cls.player_grids:
            grid.draw(cls.screen, cls.font)
        for grid in cls.enemy_grids:
            grid.draw(cls.screen, cls.font)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in cls.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            color = cls.colors['button_hover'] if is_hover else cls.colors['button']
            
            pygame.draw.rect(cls.screen, color, button["rect"])
            pygame.draw.rect(cls.screen, (100, 100, 100), button["rect"], 2)
            
            text_surf = cls.font.render(button["text"], True, cls.colors['text'])
            text_rect = text_surf.get_rect(center=button["rect"].center)
            cls.screen.blit(text_surf, text_rect)