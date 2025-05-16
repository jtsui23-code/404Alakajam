import pygame
from scripts.Grid import Grid, GridLogic

class Room:
    # Screen state
    running = False
    initialized = False
    frame = 0
    selected_cell = None  # Track selected cell (row, col)
    
    # Screen dimensions
    WIDTH = 1280
    HEIGHT = 720
    
    # Colors
    BLACK = (0, 0, 0)
    GRID_BG = (30, 30, 40)
    BUTTON_COLOR = (70, 70, 90)
    BUTTON_HOVER = (100, 100, 120)
    BUTTON_TEXT = (255, 255, 255)
    SELECTED_TEXT = (200, 200, 0)
    
    # Fonts
    default_font = None
    small_font = None
    
    # UI Elements
    room_grid = None
    play_button_rect = None
    back_button_rect = None

    @classmethod
    def initialize(cls, screen):
        """Initialize the room screen"""
        cls.WIDTH, cls.HEIGHT = screen.get_size()
        
        # Initialize fonts
        pygame.font.init()
        cls.default_font = pygame.font.SysFont('Arial', 24)
        cls.small_font = pygame.font.SysFont('Arial', 20)
        
        # Create centered grid
        grid_width = 600
        grid_height = 400
        cls.room_grid = Grid(
            (cls.WIDTH - grid_width) // 2,
            (cls.HEIGHT - grid_height) // 2 - 50,  # Move up to make space for UI
            grid_width,
            grid_height,
            3, 3
        )
        
        # Initialize grid data
        grid_data = GridLogic.generateGrid()
        GridLogic.displayGrid(cls.room_grid, grid_data, cls.default_font)
        
        # Create button rectangles
        button_width, button_height = 200, 50
        button_y = cls.room_grid.y + cls.room_grid.height + 30
        
        cls.play_button_rect = pygame.Rect(
            cls.WIDTH//2 - button_width - 20,
            button_y,
            button_width,
            button_height
        )
        
        cls.back_button_rect = pygame.Rect(
            cls.WIDTH//2 + 20,
            button_y,
            button_width,
            button_height
        )
        
        cls.initialized = True
    
    @classmethod
    def draw_selected_cell_text(cls, screen):
        """Draw the 'Selected Cell' text below buttons"""
        if cls.selected_cell:
            row, col = cls.selected_cell
            text = f"Selected Cell: {row},{col}"
        else:
            text = "Selected Cell: None"
            
        text_surface = cls.small_font.render(text, True, cls.SELECTED_TEXT)
        text_y = cls.back_button_rect.bottom + 20
        screen.blit(text_surface, (
            cls.WIDTH//2 - text_surface.get_width()//2,
            text_y
        ))

    @classmethod
    def draw_buttons(cls, screen):
        """Draw the Play and Go Back buttons"""
        # Draw Play button
        play_color = cls.BUTTON_HOVER if cls.play_button_rect.collidepoint(pygame.mouse.get_pos()) else cls.BUTTON_COLOR
        pygame.draw.rect(screen, play_color, cls.play_button_rect, border_radius=5)
        pygame.draw.rect(screen, cls.BUTTON_TEXT, cls.play_button_rect, 2, border_radius=5)
        
        play_text = cls.default_font.render("Play", True, cls.BUTTON_TEXT)
        screen.blit(play_text, (
            cls.play_button_rect.centerx - play_text.get_width()//2,
            cls.play_button_rect.centery - play_text.get_height()//2
        ))
        
        # Draw Back button
        back_color = cls.BUTTON_HOVER if cls.back_button_rect.collidepoint(pygame.mouse.get_pos()) else cls.BUTTON_COLOR
        pygame.draw.rect(screen, back_color, cls.back_button_rect, border_radius=5)
        pygame.draw.rect(screen, cls.BUTTON_TEXT, cls.back_button_rect, 2, border_radius=5)
        
        back_text = cls.default_font.render("Go Back", True, cls.BUTTON_TEXT)
        screen.blit(back_text, (
            cls.back_button_rect.centerx - back_text.get_width()//2,
            cls.back_button_rect.centery - back_text.get_height()//2
        ))
    
    @classmethod
    def handle_button_click(cls, pos):
        """Handle button clicks"""
        if cls.play_button_rect.collidepoint(pos):
            print("Play button clicked")
            if cls.selected_cell:
                print(f"Playing with selected cell: {cls.selected_cell}")
            return True
            
        if cls.back_button_rect.collidepoint(pos):
            print("Go Back button clicked")
            cls.running = False
            return True
            
        return False
    
    @classmethod
    def draw_background(cls, screen):
        """Draw the screen background"""
        screen.fill(cls.BLACK)
        
        # Draw grid background
        if cls.room_grid:
            pygame.draw.rect(
                screen,
                cls.GRID_BG,
                (
                    cls.room_grid.x - 10,
                    cls.room_grid.y - 10,
                    cls.room_grid.width + 20,
                    cls.room_grid.height + 20
                ),
                border_radius=5
            )
    
    @classmethod
    def draw(cls, screen):
        """Draw the entire room screen"""
        if not cls.initialized:
            cls.initialize(screen)
            
        cls.frame += 1
        
        # Draw all elements
        cls.draw_background(screen)
        
        if cls.room_grid:
            cls.room_grid.draw(screen, cls.default_font)
            
        cls.draw_buttons(screen)
        cls.draw_selected_cell_text(screen)
    
    @classmethod
    def update(cls, event):
        """Handle screen events"""
        if not cls.initialized:
            return False
            
        if event.type == pygame.QUIT:
            cls.running = False
            return True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cls.running = False
                return True
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check buttons first
                if cls.handle_button_click(event.pos):
                    return True
                
                # Then check grid cells
                if cls.room_grid:
                    cell = cls.room_grid.get_cell_at_pos(event.pos)
                    if cell:
                        cls.selected_cell = cell
                        return True
                
        return False
    
    @classmethod
    def clear(cls):
        """Reset screen state"""
        cls.running = False
        cls.initialized = False
        cls.frame = 0
        cls.selected_cell = None
        cls.room_grid = None
        cls.play_button_rect = None
        cls.back_button_rect = None