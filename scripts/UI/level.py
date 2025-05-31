import pygame
import random
from scripts.Grid import Grid, GridLogic

class LevelSelectionScreen:
    selected_grid_data = None
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    TORCH_FRAMES = [(255, 160, 0), (255, 100, 0), (200, 50, 0)]
    
    # Game state
    state = "SELECTING"  # "SELECTING", "ANIMATING", "OUTCOME"
    active_door = None
    selected_cell = None
    animation_timer = 0
    outcome_timer = 0
    
    @staticmethod
    def init(font):
        LevelSelectionScreen.font = font
        LevelSelectionScreen.selected_level = None
        LevelSelectionScreen.torch_frame = 0
        LevelSelectionScreen.frame_count = 0
        LevelSelectionScreen.state = "SELECTING"
        LevelSelectionScreen.active_door = None
        LevelSelectionScreen.selected_cell = None
        
        # Load medieval textures
        LevelSelectionScreen.stone_texture = LevelSelectionScreen.create_stone_pattern()
        LevelSelectionScreen.wood_texture = LevelSelectionScreen.create_wood_pattern()
        
        # Create new door grids
        LevelSelectionScreen.create_doors()
    
    @staticmethod
    def create_doors():
        """Create new door grids with random content"""
        door_width = 280
        door_height = 420
        door_margin = 70
        grid_width = 160
        grid_height = 160
        
        total_width = 3 * door_width + 2 * door_margin
        start_x = (LevelSelectionScreen.SCREEN_WIDTH - total_width) // 2
        
        LevelSelectionScreen.doors = []
        for i in range(3):
            door_rect = pygame.Rect(
                start_x + i * (door_width + door_margin),
                (LevelSelectionScreen.SCREEN_HEIGHT - door_height) // 2,
                door_width,
                door_height
            )
            
            grid = Grid(
                door_rect.centerx - grid_width // 2,
                door_rect.centery - grid_height // 2 + 10,
                grid_width,
                grid_height,
                3, 3
            )
            
            # Generate new grid data for this door
            grid_data = GridLogic.generateEncounterGrid()
            GridLogic.displayGrid(grid, grid_data, LevelSelectionScreen.font)
            
            LevelSelectionScreen.doors.append({
                'rect': door_rect,
                'grid': grid,
                'level': i+1,
                'grid_data': grid_data,
                'hover': False
            })

    @staticmethod
    def create_stone_pattern():
        texture = pygame.Surface((64, 64), pygame.SRCALPHA)
        colors = [(80, 80, 90), (70, 70, 80), (90, 90, 100)]
        for _ in range(50):
            x, y = random.randint(0, 63), random.randint(0, 63)
            pygame.draw.circle(texture, random.choice(colors), (x, y), 1)
        return texture

    @staticmethod
    def create_wood_pattern():
        texture = pygame.Surface((64, 64))
        texture.fill((94, 53, 17))
        for _ in range(20):
            x = random.randint(0, 63)
            pygame.draw.line(texture, (74, 33, 7), (x, 0), (x, 63), 1)
        return texture

    @staticmethod
    def handle_event(event):
        if LevelSelectionScreen.state == "SELECTING":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, door in enumerate(LevelSelectionScreen.doors):
                    if door['rect'].collidepoint(mouse_pos):
                        LevelSelectionScreen.selected_level = door['level']
                        LevelSelectionScreen.active_door = i
                        LevelSelectionScreen.selected_grid_data = door['grid_data']  

                        
                        # Randomly select a cell
                        row = random.randint(0, 2)
                        col = random.randint(0, 2)
                        LevelSelectionScreen.selected_cell = (row, col)
                        
                        # Highlight the selected cell
                        door['grid'].set_selected_cell(row, col)
                        
                        # Start animation
                        LevelSelectionScreen.state = "ANIMATING"
                        LevelSelectionScreen.animation_timer = 0
                        return True

        elif LevelSelectionScreen.state == "OUTCOME":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Reset for next selection
                LevelSelectionScreen.state = "SELECTING"
                LevelSelectionScreen.active_door = None
                LevelSelectionScreen.selected_cell = None
                
                # If it was a coin, create new doors
                door = LevelSelectionScreen.doors[LevelSelectionScreen.active_door]
                cell = door['grid_data'][LevelSelectionScreen.selected_cell[0]][LevelSelectionScreen.selected_cell[1]]
                if cell.get('type') == 'coin':
                    LevelSelectionScreen.create_doors()
                
                return True
        return False

    @staticmethod
    def update(dt):
        """Update screen state"""
        LevelSelectionScreen.frame_count += 1
        LevelSelectionScreen.torch_frame = (LevelSelectionScreen.frame_count // 5) % 3
        
        if LevelSelectionScreen.state == "ANIMATING":
            LevelSelectionScreen.animation_timer += dt
            
            # After 2 seconds of animation, show outcome
            if LevelSelectionScreen.animation_timer > 2000:  # 2000ms = 2 seconds
                LevelSelectionScreen.state = "OUTCOME"
                LevelSelectionScreen.outcome_timer = 0
                
        elif LevelSelectionScreen.state == "OUTCOME":
            LevelSelectionScreen.outcome_timer += dt

    @staticmethod
    def draw_dungeon_background(screen):
        for x in range(0, LevelSelectionScreen.SCREEN_WIDTH, 64):
            for y in range(0, LevelSelectionScreen.SCREEN_HEIGHT, 64):
                screen.blit(LevelSelectionScreen.stone_texture, (x, y))
        
        for _ in range(3):
            start = (random.randint(0, 1280), random.randint(0, 720))
            end = (start[0] + random.randint(-50, 50), start[1] + random.randint(-50, 50))
            pygame.draw.line(screen, (40, 40, 50), start, end, 3)

    @staticmethod
    def draw_medieval_door(screen, door_rect, hover=False):
        pygame.draw.rect(screen, (40, 40, 50), door_rect.inflate(10, 10), border_radius=12)
        
        door_surface = pygame.Surface(door_rect.size)
        door_surface.blit(LevelSelectionScreen.wood_texture, (0, 0))
        
        for y in range(20, door_rect.height, 80):
            pygame.draw.rect(door_surface, (80, 80, 90), (0, y, door_rect.width, 10))
        
        for x in range(10, door_rect.width, 30):
            for y in range(10, door_rect.height, 30):
                pygame.draw.circle(door_surface, (100, 100, 110), (x, y), 2)
        
        if hover:
            door_surface.fill((255, 255, 255, 30), special_flags=pygame.BLEND_RGBA_ADD)
        
        screen.blit(door_surface, door_rect.topleft)
        
        torch_color = LevelSelectionScreen.TORCH_FRAMES[LevelSelectionScreen.torch_frame]
        pygame.draw.circle(screen, torch_color, (door_rect.left - 15, door_rect.centery), 12)
        pygame.draw.circle(screen, torch_color, (door_rect.right + 15, door_rect.centery), 12)

    @staticmethod
    def draw_outcome(screen, door):
        """Draw outcome message based on selected cell content"""
        if not LevelSelectionScreen.selected_cell:
            return
            
        cell = door['grid_data'][LevelSelectionScreen.selected_cell[0]][LevelSelectionScreen.selected_cell[1]]
        
        if cell.get('type') == 'enemy':
            text = "ENEMY ENCOUNTER! Click to battle."
            color = (200, 50, 50)
        elif cell.get('type') == 'coin':
            text = f"FOUND {cell.get('value', 0)} COINS! Click to continue."
            color = (255, 215, 0)
        elif cell.get('type') == 'chest':
            text = "FOUND A CHEST! Click to continue."
            color = (200, 180, 50)
        else:
            text = "Click to continue."
            color = (200, 200, 200)
        
        # Create message background
        message_rect = pygame.Rect(
            LevelSelectionScreen.SCREEN_WIDTH // 2 - 250,
            LevelSelectionScreen.SCREEN_HEIGHT - 100,
            500, 60
        )
        pygame.draw.rect(screen, (30, 30, 50), message_rect, border_radius=10)
        pygame.draw.rect(screen, color, message_rect, 3, border_radius=10)
        
        # Draw text
        text_surf = LevelSelectionScreen.font.render(text, True, color)
        screen.blit(text_surf, (
            message_rect.centerx - text_surf.get_width() // 2,
            message_rect.centery - text_surf.get_height() // 2
        ))

    @staticmethod
    def draw(screen):
        LevelSelectionScreen.frame_count += 1
        
        # Draw dungeon background
        LevelSelectionScreen.draw_dungeon_background(screen)
        
        # Draw title
        title_text = LevelSelectionScreen.font.render("CHOOSE THY PATH", True, (180, 30, 30))
        shadow_text = LevelSelectionScreen.font.render("CHOOSE THY PATH", True, (40, 40, 50))
        title_pos = (LevelSelectionScreen.SCREEN_WIDTH//2 - title_text.get_width()//2, 30)
        screen.blit(shadow_text, (title_pos[0]+3, title_pos[1]+3))
        screen.blit(title_text, title_pos)
        
        # Draw doors and grids
        mouse_pos = pygame.mouse.get_pos()
        for i, door in enumerate(LevelSelectionScreen.doors):
            door['hover'] = door['rect'].collidepoint(mouse_pos)
            
            # Draw door
            LevelSelectionScreen.draw_medieval_door(screen, door['rect'], door['hover'])
            
            # Draw grid
            door['grid'].draw(screen, LevelSelectionScreen.font)
            
            # Draw level number
            parchment = pygame.Surface((120, 40), pygame.SRCALPHA)
            parchment.fill((200, 180, 140, 200))
            pygame.draw.rect(parchment, (150, 120, 90), (0, 0, 120, 40), 2)
            level_text = LevelSelectionScreen.font.render(f"LEVEL {door['level']}", True, (80, 50, 30))
            parchment.blit(level_text, (60 - level_text.get_width()//2, 20 - level_text.get_height()//2))
            screen.blit(parchment, (door['rect'].centerx - 60, door['rect'].bottom - 30))
            
            # Add chains effect
            if door['hover']:
                chain_color = (100, 100, 100)
                for x in [door['rect'].left + 10, door['rect'].right - 10]:
                    pygame.draw.line(screen, chain_color, 
                        (x, door['rect'].top - 20), (x, door['rect'].top), 3)
        
        # Draw outcome message if needed
        if (LevelSelectionScreen.state == "OUTCOME" and 
            LevelSelectionScreen.active_door is not None and 
            LevelSelectionScreen.selected_cell is not None):
            door = LevelSelectionScreen.doors[LevelSelectionScreen.active_door]
            LevelSelectionScreen.draw_outcome(screen, door)

    @staticmethod
    def get_selected_level():
        return LevelSelectionScreen.selected_level
    
    @staticmethod
    def get_selected_cell():
        return LevelSelectionScreen.selected_cell
    
    @staticmethod
    def get_active_door():
        if LevelSelectionScreen.active_door is not None:
            return LevelSelectionScreen.doors[LevelSelectionScreen.active_door]
        return None
    
    @staticmethod
    def reset_selection():
        LevelSelectionScreen.selected_level = None
        LevelSelectionScreen.active_door = None
        LevelSelectionScreen.selected_cell = None
        LevelSelectionScreen.state = "SELECTING"