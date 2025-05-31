import pygame
import random
from scripts.Grid import Grid, GridLogic
from scripts.UI.level import LevelSelectionScreen

class Room:
    # Screen state
    selected_encounter_data = None
    running = False
    initialized = False
    frame = 0
    selected_cell = None  # Track selected cell (row, col)
    encounter_grid_data = None  # Store encounter data for the room
    
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
    INFO_TEXT = (180, 180, 180)
    
    # Fonts
    default_font = None
    small_font = None
    large_font = None
    
    # UI Elements
    room_grid = None
    play_button_rect = None
    back_button_rect = None
    roll_button_rect = None
    
    # Animation state
    rolling_animation = False
    roll_timer = 0
    roll_duration = 2.0  # 2 seconds of rolling animation

    @classmethod
    def initialize(cls, screen):
        """Initialize the room screen"""
        cls.WIDTH, cls.HEIGHT = screen.get_size()
        
        # Initialize fonts
        pygame.font.init()
        cls.default_font = pygame.font.SysFont('Arial', 24)
        cls.small_font = pygame.font.SysFont('Arial', 20)
        cls.large_font = pygame.font.SysFont('Arial', 32)
        
        # Create centered grid
        grid_width = 600
        grid_height = 400
        cls.room_grid = Grid(
            (cls.WIDTH - grid_width) // 2,
            (cls.HEIGHT - grid_height) // 2 - 50,
            grid_width,
            grid_height,
            3, 3
        )
        
        # Generate encounter data for this room
        cls.encounter_grid_data = GridLogic.generateEncounterGrid(3, 3)
        
        # Display the encounter grid
        GridLogic.displayGrid(cls.room_grid, cls.encounter_grid_data, cls.default_font)
        
        # If there was a selected cell from level selection, use it
        if LevelSelectionScreen.selected_cell:
            row, col = LevelSelectionScreen.selected_cell
            cls.room_grid.set_selected_cell(row, col)
            cls.selected_cell = (row, col)

        # Create button rectangles
        button_width, button_height = 180, 50
        button_y = cls.room_grid.y + cls.room_grid.height + 30
        
        # Three buttons: Roll, Play, Back
        cls.roll_button_rect = pygame.Rect(
            cls.WIDTH//2 - button_width - 100,
            button_y,
            button_width,
            button_height
        )
        
        cls.play_button_rect = pygame.Rect(
            cls.WIDTH//2 - button_width//2,
            button_y,
            button_width,
            button_height
        )
        
        cls.back_button_rect = pygame.Rect(
            cls.WIDTH//2 + 100,
            button_y,
            button_width,
            button_height
        )
        
        cls.initialized = True
        print("Room initialized with encounter grid")

    @classmethod
    def select_random_encounter(cls):
        """Randomly select an encounter from the current room grid"""
        if not cls.encounter_grid_data:
            print("Warning: No encounter grid data available")
            return None
        
        # Start rolling animation
        cls.rolling_animation = True
        cls.roll_timer = 0
        
        # Randomly select a cell
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        
        # Get the encounter data
        selected_encounter = cls.encounter_grid_data[row][col]
        cls.selected_encounter_data = selected_encounter
        cls.selected_cell = (row, col)
        
        # Update grid selection
        cls.room_grid.set_selected_cell(row, col)
        
        print(f"Random encounter selected at ({row}, {col}): {selected_encounter}")
        return selected_encounter

    @classmethod
    def get_encounter_description(cls, encounter_data):
        """Get a description of the encounter"""
        if not encounter_data:
            return "No encounter selected"
        
        encounter_type = encounter_data.get('type', 'unknown')
        
        if encounter_type == 'enemy':
            enemy_name = encounter_data.get('name', 'Unknown Enemy')
            return f"Enemy: {enemy_name}"
        elif encounter_type == 'coin':
            coin_value = encounter_data.get('value', 0)
            return f"Treasure: {coin_value} coins"
        elif encounter_type == 'chest':
            return "Treasure: Mysterious chest"
        else:
            return f"Unknown encounter: {encounter_type}"

    @classmethod
    def update_animation(cls, dt):
        """Update rolling animation"""
        if cls.rolling_animation:
            cls.roll_timer += dt
            
            # During animation, randomly highlight different cells
            if cls.roll_timer < cls.roll_duration:
                if int(cls.roll_timer * 10) % 2 == 0:  # Change selection every 0.1 seconds
                    temp_row = random.randint(0, 2)
                    temp_col = random.randint(0, 2)
                    cls.room_grid.set_selected_cell(temp_row, temp_col)
            else:
                # Animation finished, show final selection
                cls.rolling_animation = False
                if cls.selected_cell:
                    row, col = cls.selected_cell
                    cls.room_grid.set_selected_cell(row, col)

    @classmethod
    def draw_title(cls, screen):
        """Draw the room title"""
        title_text = "ROOM EXPLORATION"
        title_surface = cls.large_font.render(title_text, True, cls.BUTTON_TEXT)
        title_y = cls.room_grid.y - 80
        screen.blit(title_surface, (
            cls.WIDTH//2 - title_surface.get_width()//2,
            title_y
        ))

    @classmethod
    def draw_encounter_info(cls, screen):
        """Draw information about the selected encounter"""
        info_y = cls.back_button_rect.bottom + 30
        
        if cls.rolling_animation:
            info_text = "Rolling for encounter..."
        elif cls.selected_encounter_data:
            info_text = cls.get_encounter_description(cls.selected_encounter_data)
        else:
            info_text = "Click 'Roll' to select a random encounter or click a cell manually"
        
        info_surface = cls.small_font.render(info_text, True, cls.INFO_TEXT)
        screen.blit(info_surface, (
            cls.WIDTH//2 - info_surface.get_width()//2,
            info_y
        ))
        
        # Show selected cell coordinates
        if cls.selected_cell:
            row, col = cls.selected_cell
            coord_text = f"Selected Cell: ({row}, {col})"
        else:
            coord_text = "No cell selected"
            
        coord_surface = cls.small_font.render(coord_text, True, cls.SELECTED_TEXT)
        screen.blit(coord_surface, (
            cls.WIDTH//2 - coord_surface.get_width()//2,
            info_y + 25
        ))

    @classmethod
    def draw_buttons(cls, screen):
        """Draw all action buttons"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw Roll button
        roll_color = cls.BUTTON_HOVER if cls.roll_button_rect.collidepoint(mouse_pos) else cls.BUTTON_COLOR
        if cls.rolling_animation:
            roll_color = (50, 50, 50)  # Disabled color during animation
        
        pygame.draw.rect(screen, roll_color, cls.roll_button_rect, border_radius=5)
        pygame.draw.rect(screen, cls.BUTTON_TEXT, cls.roll_button_rect, 2, border_radius=5)
        
        roll_text = cls.default_font.render("Roll", True, cls.BUTTON_TEXT)
        screen.blit(roll_text, (
            cls.roll_button_rect.centerx - roll_text.get_width()//2,
            cls.roll_button_rect.centery - roll_text.get_height()//2
        ))
        
        # Draw Play button
        play_color = cls.BUTTON_HOVER if cls.play_button_rect.collidepoint(mouse_pos) else cls.BUTTON_COLOR
        play_enabled = cls.selected_encounter_data is not None and not cls.rolling_animation
        if not play_enabled:
            play_color = (50, 50, 50)  # Disabled color
        
        pygame.draw.rect(screen, play_color, cls.play_button_rect, border_radius=5)
        pygame.draw.rect(screen, cls.BUTTON_TEXT, cls.play_button_rect, 2, border_radius=5)
        
        play_text = cls.default_font.render("Enter Battle", True, cls.BUTTON_TEXT)
        screen.blit(play_text, (
            cls.play_button_rect.centerx - play_text.get_width()//2,
            cls.play_button_rect.centery - play_text.get_height()//2
        ))
        
        # Draw Back button
        back_color = cls.BUTTON_HOVER if cls.back_button_rect.collidepoint(mouse_pos) else cls.BUTTON_COLOR
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
        if cls.rolling_animation:
            return False  # Ignore clicks during animation
        
        if cls.roll_button_rect.collidepoint(pos):
            print("Roll button clicked - selecting random encounter")
            cls.select_random_encounter()
            return True
            
        if cls.play_button_rect.collidepoint(pos):
            if cls.selected_encounter_data:
                print(f"Enter Battle clicked with encounter: {cls.selected_encounter_data}")
                return "battle"
            else:
                print("No encounter selected - cannot enter battle")
            return True
            
        if cls.back_button_rect.collidepoint(pos):
            print("Go Back button clicked")
            cls.running = False
            return "back"
            
        return False

    @classmethod
    def handle_grid_click(cls, pos):
        """Handle clicks on grid cells"""
        if cls.rolling_animation:
            return False
        
        # Check which cell was clicked
        for row in range(3):
            for col in range(3):
                cell_rect = pygame.Rect(
                    cls.room_grid.x + col * cls.room_grid.cell_width,
                    cls.room_grid.y + row * cls.room_grid.cell_height,
                    cls.room_grid.cell_width,
                    cls.room_grid.cell_height
                )
                
                if cell_rect.collidepoint(pos):
                    # Manual selection
                    cls.selected_cell = (row, col)
                    cls.selected_encounter_data = cls.encounter_grid_data[row][col]
                    cls.room_grid.set_selected_cell(row, col)
                    print(f"Manually selected encounter at ({row}, {col}): {cls.selected_encounter_data}")
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
        
        # Update animation
        dt = pygame.time.Clock().tick(60) / 1000.0
        cls.update_animation(dt)
        
        cls.frame += 1
        
        # Draw all elements
        cls.draw_background(screen)
        cls.draw_title(screen)
        
        if cls.room_grid:
            cls.room_grid.draw(screen, cls.default_font)
            
        cls.draw_buttons(screen)
        cls.draw_encounter_info(screen)

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
                return "back"
            elif event.key == pygame.K_SPACE and not cls.rolling_animation:
                # Space bar to roll
                cls.select_random_encounter()
                return True
            elif event.key == pygame.K_RETURN and cls.selected_encounter_data and not cls.rolling_animation:
                # Enter to battle
                return "battle"
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check buttons first
                button_result = cls.handle_button_click(event.pos)
                if button_result:
                    return button_result
                
                # Then check grid cells
                if cls.handle_grid_click(event.pos):
                    return True
                    
        return False

    @classmethod
    def get_selected_encounter(cls):
        """Get the currently selected encounter data"""
        return cls.selected_encounter_data

    @classmethod
    def clear(cls):
        """Reset screen state"""
        cls.running = False
        cls.initialized = False
        cls.frame = 0
        cls.selected_cell = None
        cls.selected_encounter_data = None
        cls.encounter_grid_data = None
        cls.room_grid = None
        cls.play_button_rect = None
        cls.back_button_rect = None
        cls.roll_button_rect = None
        cls.rolling_animation = False
        cls.roll_timer = 0
        
        # Clear level selection data if needed
        if hasattr(LevelSelectionScreen, 'selected_grid_data'):
            LevelSelectionScreen.selected_grid_data = None
        if hasattr(LevelSelectionScreen, 'selected_cell'):
            LevelSelectionScreen.selected_cell = None
        
        print("Room state cleared")