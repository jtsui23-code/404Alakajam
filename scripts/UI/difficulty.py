import random
import math

class DifficultySelector:
    # Class variables to maintain state
    selected = 1  # Default to KNIGHT
    frame = 0
    result = None
    running = False
    blood_stains = []
    initialized = False
    
    # Screen dimensions
    WIDTH = 800
    HEIGHT = 600
    
    # Difficulty options
    difficulties = [
        "SQUIRE",
        "KNIGHT", 
        "REAPER",
        "DOOMED"
    ]
    
    # Colors
    BLACK = (0, 0, 0)
    DARK_GRAY = (30, 30, 30)
    GRAY = (60, 60, 60)
    WHITE = (255, 255, 255)
    RED = (180, 20, 20)
    GOLD = (200, 170, 60)
    
    @classmethod
    def initialize(cls, screen):
        """Initialize state but don't draw anything"""
        cls.WIDTH, cls.HEIGHT = screen.get_size()
        
        # Generate blood stains
        cls.blood_stains = []
        for _ in range(20):
            cls.blood_stains.append((
                random.randint(0, cls.WIDTH),
                random.randint(0, cls.HEIGHT),
                random.randint(2, 8)  # Size
            ))
        
        cls.initialized = True
        cls.result = None
    
    @classmethod
    def draw_text(cls, screen, text, size, color, x, y):
        """Draw pixelated text with shadow"""
        font_obj = pygame.font.SysFont("monospace", size, bold=True)
        text_surface = font_obj.render(text, False, cls.BLACK)
        screen.blit(text_surface, (x+2, y+2))
        text_surface = font_obj.render(text, False, color)
        screen.blit(text_surface, (x, y))
    
    @classmethod
    def draw_background(cls, screen):
        """Draw the brick wall background"""
        # Draw simple brick pattern
        for y in range(0, cls.HEIGHT, 24):
            offset = 12 if (y // 24) % 2 else 0
            for x in range(-offset, cls.WIDTH, 24):
                # Random variation in brick color
                color_var = random.randint(-10, 5)
                brick_color = (
                    cls.DARK_GRAY[0] + color_var, 
                    cls.DARK_GRAY[1] + color_var, 
                    cls.DARK_GRAY[2] + color_var
                )
                pygame.draw.rect(screen, brick_color, (x, y, 23, 23))
                pygame.draw.rect(screen, cls.BLACK, (x, y, 24, 24), 1)
        
        # Draw blood stains
        for x, y, size in cls.blood_stains:
            pygame.draw.circle(screen, cls.RED, (x, y), size, 0)
            # Add some darker blood in the center
            pygame.draw.circle(screen, (100, 0, 0), (x, y), size//2, 0)
    
    @classmethod
    def draw_decorations(cls, screen):
        """Draw decorative elements"""
        # Draw chains
        chain_positions = [(100, 50), (cls.WIDTH-100, 50)]
        for x, y in chain_positions:
            for i in range(6):
                pygame.draw.rect(screen, cls.GRAY, (x-3, y+i*20, 6, 15))
                pygame.draw.rect(screen, cls.BLACK, (x-3, y+i*20, 6, 15), 1)
        
        # Draw skulls at the bottom of chains
        for x, y in chain_positions:
            # Skull base
            pygame.draw.circle(screen, cls.WHITE, (x, y+120), 12)
            pygame.draw.rect(screen, cls.BLACK, (x-12, y+120, 24, 12), 1)
            # Eye sockets
            pygame.draw.rect(screen, cls.BLACK, (x-6, y+116, 4, 4))
            pygame.draw.rect(screen, cls.BLACK, (x+2, y+116, 4, 4))
            # Nose
            pygame.draw.rect(screen, cls.BLACK, (x-1, y+122, 2, 3))
            # Teeth
            pygame.draw.rect(screen, cls.BLACK, (x-6, y+127, 12, 1))
        
        # Draw torches with animated flames
        torch_positions = [(150, 60), (cls.WIDTH-150, 60)]
        for x, y in torch_positions:
            # Handle
            pygame.draw.rect(screen, (80, 50, 20), (x-2, y, 4, 15))
            
            # Flame (animated)
            flame_height = 6 + (cls.frame % 6) // 2
            flame_offset = (cls.frame % 4) - 2
            
            # Main flame
            pygame.draw.polygon(screen, (220, 100, 0), [
                (x, y-flame_height-3),
                (x-4, y-3),
                (x+4, y-3)
            ])
            
            # Inner flame
            pygame.draw.polygon(screen, (250, 200, 0), [
                (x+flame_offset//2, y-flame_height-1),
                (x-2, y-2),
                (x+2, y-2)
            ])
    
    @classmethod
    def draw_options(cls, screen):
        """Draw the difficulty options"""
        # Draw title banner
        banner_y = 60
        pygame.draw.rect(screen, cls.RED, (cls.WIDTH//2-180, banner_y, 360, 60))
        pygame.draw.rect(screen, cls.BLACK, (cls.WIDTH//2-180, banner_y, 360, 60), 2)
        cls.draw_text(screen, "CHOOSE YOUR FATE", 30, cls.WHITE, cls.WIDTH//2-160, banner_y+15)
        
        # Draw options
        option_width = 300
        option_height = 40
        
        for i, diff in enumerate(cls.difficulties):
            y_pos = 180 + i * 60
            option_x = cls.WIDTH//2 - option_width//2
            
            # Option background
            if i == cls.selected:
                # Pulsing effect for selected option
                pulse = abs(math.sin(cls.frame * 0.1) * 20)
                color = (min(255, cls.RED[0] + pulse), 
                         min(255, cls.RED[1] + pulse), 
                         min(255, cls.RED[2] + pulse))
                
                # Draw selection indicators
                cls.draw_text(screen, ">>", 24, cls.GOLD, option_x - 40, y_pos + 8)
                cls.draw_text(screen, "<<", 24, cls.GOLD, option_x + option_width + 10, y_pos + 8)
            else:
                color = cls.DARK_GRAY
            
            pygame.draw.rect(screen, color, (option_x, y_pos, option_width, option_height))
            pygame.draw.rect(screen, cls.BLACK, (option_x, y_pos, option_width, option_height), 2)
            
            # Option text
            text_x = option_x + 20
            text_y = y_pos + 8
            cls.draw_text(screen, diff, 24, cls.WHITE, text_x, text_y)
            
            # Add difficulty indicators
            if diff == "SQUIRE":
                indicator = "I"
            elif diff == "KNIGHT":
                indicator = "II"
            elif diff == "REAPER":
                indicator = "III"
            else:  # DOOMED
                indicator = "IIII"
                
            cls.draw_text(screen, indicator, 20, cls.WHITE, option_x + option_width - 40, y_pos + 8)
    
    @classmethod
    def draw(cls, screen):
        """Draw the entire difficulty selection screen"""
        if not cls.initialized:
            cls.initialize(screen)
            
        # Increment frame counter
        cls.frame += 1
        
        # Draw all elements
        cls.draw_background(screen)
        cls.draw_decorations(screen)
        cls.draw_options(screen)
        
        # Draw instructions
        instruction_y = cls.HEIGHT - 60
        cls.draw_text(screen, "UP/DOWN: SELECT", 18, cls.WHITE, cls.WIDTH//2 - 140, instruction_y)
        cls.draw_text(screen, "ENTER: CONFIRM", 18, cls.WHITE, cls.WIDTH//2 - 140, instruction_y + 30)
    
    @classmethod
    def update(cls, events):
        """Handle events and update state"""
        if not cls.initialized:
            return False
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cls.selected = (cls.selected - 1) % len(cls.difficulties)
                    return True  # Something changed
                elif event.key == pygame.K_DOWN:
                    cls.selected = (cls.selected + 1) % len(cls.difficulties)
                    return True  # Something changed
                elif event.key == pygame.K_RETURN:
                    cls.result = cls.difficulties[cls.selected]
                    cls.running = False
                    return True  # Something changed
        
        return False  # Nothing changed
    
    @classmethod
    def clear(cls, screen):
        """Clear the screen and reset state"""
        screen.fill(cls.BLACK)
        cls.running = False
        cls.result = None
    
    @classmethod
    def get_result(cls):
        """Get the selected difficulty"""
        return cls.result

# Import pygame at the top level but don't initialize it
import pygame