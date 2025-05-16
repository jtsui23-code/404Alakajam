import pygame
from scripts.Grid import Grid, GridLogic
import random 

class LevelSelectionScreen:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    TORCH_FRAMES = [  # Simple torch animation frames
        (255, 160, 0), 
        (255, 100, 0),
        (200, 50, 0)
    ]
    
    @staticmethod
    def init(font):
        LevelSelectionScreen.font = font
        LevelSelectionScreen.selected_level = None
        LevelSelectionScreen.torch_frame = 0
        LevelSelectionScreen.frame_count = 0
        
        # Load medieval textures (simple pattern-based)
        LevelSelectionScreen.stone_texture = LevelSelectionScreen.create_stone_pattern()
        LevelSelectionScreen.wood_texture = LevelSelectionScreen.create_wood_pattern()
        
        # Door settings
        door_width = 280
        door_height = 420
        door_margin = 70
        
        # Grid settings
        grid_width = 160
        grid_height = 160
        
        # Calculate positions
        total_width = 3 * door_width + 2 * door_margin
        start_x = (LevelSelectionScreen.SCREEN_WIDTH - total_width) // 2
        
        # Initialize doors and grids
        LevelSelectionScreen.doors = []
        for i in range(3):
            door_rect = pygame.Rect(
                start_x + i * (door_width + door_margin),
                (LevelSelectionScreen.SCREEN_HEIGHT - door_height) // 2,
                door_width,
                door_height
            )
            
            # Create grid with dungeon aesthetic
            grid = Grid(
                door_rect.centerx - grid_width // 2,
                door_rect.centery - grid_height // 2 + 10,
                grid_width,
                grid_height,
                3, 3
            )
            
            # Generate and store grid data
            grid_data = GridLogic.generateGrid()
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
        """Create a simple stone pattern surface"""
        texture = pygame.Surface((64, 64), pygame.SRCALPHA)
        colors = [(80, 80, 90), (70, 70, 80), (90, 90, 100)]
        for _ in range(50):
            x, y = random.randint(0, 63), random.randint(0, 63)
            pygame.draw.circle(texture, random.choice(colors), (x, y), 1)
        return texture

    @staticmethod
    def create_wood_pattern():
        """Create a simple wood grain pattern"""
        texture = pygame.Surface((64, 64))
        texture.fill((94, 53, 17))
        for _ in range(20):
            x = random.randint(0, 63)
            pygame.draw.line(texture, (74, 33, 7), (x, 0), (x, 63), 1)
        return texture

    @staticmethod
    def handle_event(event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for door in LevelSelectionScreen.doors:
                if door['rect'].collidepoint(mouse_pos):
                    LevelSelectionScreen.selected_level = door['level']
                    return True
        return False

    @staticmethod
    def draw_dungeon_background(screen):
        """Draw tiled stone background with cracks"""
        # Stone texture
        for x in range(0, LevelSelectionScreen.SCREEN_WIDTH, 64):
            for y in range(0, LevelSelectionScreen.SCREEN_HEIGHT, 64):
                screen.blit(LevelSelectionScreen.stone_texture, (x, y))
        
        # Random cracks
        for _ in range(3):
            start = (random.randint(0, 1280), random.randint(0, 720))
            end = (start[0] + random.randint(-50, 50), start[1] + random.randint(-50, 50))
            pygame.draw.line(screen, (40, 40, 50), start, end, 3)

    @staticmethod
    def draw_medieval_door(screen, door_rect, hover=False):
        """Draw a medieval-style dungeon door"""
        # Door frame
        pygame.draw.rect(screen, (40, 40, 50), door_rect.inflate(10, 10), border_radius=12)
        
        # Main door (wood texture)
        door_surface = pygame.Surface(door_rect.size)
        door_surface.blit(LevelSelectionScreen.wood_texture, (0, 0))
        
        # Add metal bands
        for y in range(20, door_rect.height, 80):
            pygame.draw.rect(door_surface, (80, 80, 90), (0, y, door_rect.width, 10))
        
        # Add rivets
        for x in range(10, door_rect.width, 30):
            for y in range(10, door_rect.height, 30):
                pygame.draw.circle(door_surface, (100, 100, 110), (x, y), 2)
        
        # Add hover effect
        if hover:
            door_surface.fill((255, 255, 255, 30), special_flags=pygame.BLEND_RGBA_ADD)
        
        screen.blit(door_surface, door_rect.topleft)
        
        # Draw torch sconces
        torch_color = LevelSelectionScreen.TORCH_FRAMES[
            (LevelSelectionScreen.frame_count // 5) % len(LevelSelectionScreen.TORCH_FRAMES)
        ]
        pygame.draw.circle(screen, torch_color, (door_rect.left - 15, door_rect.centery), 12)
        pygame.draw.circle(screen, torch_color, (door_rect.right + 15, door_rect.centery), 12)

    @staticmethod
    def draw(screen):
        LevelSelectionScreen.frame_count += 1
        
        # Draw dungeon background
        LevelSelectionScreen.draw_dungeon_background(screen)
        
        # Draw title with medieval text effect
        title_text = LevelSelectionScreen.font.render("CHOOSE THY PATH", True, (180, 30, 30))
        shadow_text = LevelSelectionScreen.font.render("CHOOSE THY PATH", True, (40, 40, 50))
        title_pos = (LevelSelectionScreen.SCREEN_WIDTH//2 - title_text.get_width()//2, 30)
        screen.blit(shadow_text, (title_pos[0]+3, title_pos[1]+3))
        screen.blit(title_text, title_pos)
        
        # Draw doors and grids
        mouse_pos = pygame.mouse.get_pos()
        for door in LevelSelectionScreen.doors:
            # Update hover state
            door['hover'] = door['rect'].collidepoint(mouse_pos)
            
            # Draw medieval door
            LevelSelectionScreen.draw_medieval_door(screen, door['rect'], door['hover'])
            
            # Draw grid with dungeon cell style
            grid = door['grid']
            grid.draw(screen, LevelSelectionScreen.font)
            
            # Draw level number on ancient parchment
            parchment = pygame.Surface((120, 40), pygame.SRCALPHA)
            parchment.fill((200, 180, 140, 200))
            pygame.draw.rect(parchment, (150, 120, 90), (0, 0, 120, 40), 2)
            level_text = LevelSelectionScreen.font.render(f"LEVEL {door['level']}", True, (80, 50, 30))
            parchment.blit(level_text, (60 - level_text.get_width()//2, 20 - level_text.get_height()//2))
            screen.blit(parchment, (
                door['rect'].centerx - 60,
                door['rect'].bottom - 30
            ))
            
            # Add chains effect
            if door['hover']:
                chain_color = (100, 100, 100)
                for x in [door['rect'].left + 10, door['rect'].right - 10]:
                    pygame.draw.line(screen, chain_color, 
                        (x, door['rect'].top - 20), (x, door['rect'].top), 3)

    @staticmethod
    def get_selected_level():
        return LevelSelectionScreen.selected_level
    
    @staticmethod
    def reset_selection():
        LevelSelectionScreen.selected_level = None