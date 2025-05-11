import math
import random

class Character:
    # Class variables to maintain state
    BLACK = (0, 0, 0)
    DARK_GRAY = (20, 20, 20)
    GRAY = (50, 50, 50)
    LIGHT_GRAY = (100, 100, 100)
    WHITE = (255, 255, 255)
    RED = (150, 30, 30)
    DARK_RED = (100, 20, 20)
    BLOOD_RED = (120, 10, 10)
    BROWN = (139, 69, 19)
    DARK_BROWN = (80, 40, 10)
    GOLD = (212, 175, 55)
    DARK_GOLD = (160, 120, 40)
    PURPLE = (128, 0, 128)
    BLUE = (30, 30, 150)
    GREEN = (30, 150, 30)
    
    # Character class data
    character_classes = [
        {
            "name": "KNIGHT",
            "description": "A stalwart defender clad in heavy armor. Specializes in sword and shield combat.",
            "color": BLUE,
            "highlight": (100, 100, 255),
            "stats": {"STR": 8, "DEX": 5, "INT": 3, "VIT": 9, "DEF": 10},
            "weapon": "Longsword & Shield",
            "special": "Shield Bash",
            "weakness": "Slow Movement"
        },
        {
            "name": "WIZZARD",
            "description": "A master of arcane arts. Wields devastating spells but lacks physical defense.",
            "color": PURPLE,
            "highlight": (200, 100, 200),
            "stats": {"STR": 3, "DEX": 4, "INT": 10, "VIT": 4, "DEF": 2},
            "weapon": "Magic Staff",
            "special": "Fireball",
            "weakness": "Physical Attacks"
        },
        {
            "name": "THIEF",
            "description": "A nimble rogue who strikes from the shadows. Excels at finding traps and treasures.",
            "color": GREEN,
            "highlight": (100, 200, 100),
            "stats": {"STR": 5, "DEX": 10, "INT": 6, "VIT": 4, "DEF": 3},
            "weapon": "Daggers",
            "special": "Backstab",
            "weakness": "Direct Combat"
        },
        {
            "name": "GOBLIN",
            "description": "A cunning creature with a knack for trickery. Small but dangerous in numbers.",
            "color": (100, 150, 50),
            "highlight": (150, 200, 100),
            "stats": {"STR": 4, "DEX": 8, "INT": 5, "VIT": 3, "DEF": 2},
            "weapon": "Crude Spear",
            "special": "Ambush",
            "weakness": "Low Health"
        },
        {
            "name": "RAT",
            "description": "Small and quick, able to squeeze through tight spaces. Carries disease.",
            "color": (150, 150, 150),
            "highlight": (200, 200, 200),
            "stats": {"STR": 2, "DEX": 9, "INT": 3, "VIT": 2, "DEF": 1},
            "weapon": "Sharp Teeth",
            "special": "Plague Bite",
            "weakness": "Very Fragile"
        }
    ]
    
    # State variables
    selected_character = 0
    animation_timer = 0
    torch_flicker = 0
    dust_particles = []
    blood_splatters = []
    chains = []
    embers = []
    initialized = False
    
    @classmethod
    def initialize(cls):
        """Initialize particles and effects only when needed"""
        if not cls.initialized:
            # Create dust particles
            cls.dust_particles = []
            for _ in range(20):
                cls.dust_particles.append({
                    "x": random.randint(0, 800),
                    "y": random.randint(0, 600),
                    "size": random.randint(1, 3),
                    "speed": random.uniform(0.2, 0.8),
                    "color": (random.randint(100, 150), random.randint(100, 150), random.randint(100, 150), random.randint(50, 150))
                })
            
            # Create blood splatters
            cls.blood_splatters = []
            for _ in range(10):
                cls.blood_splatters.append({
                    "x": random.randint(0, 800),
                    "y": random.randint(0, 600),
                    "size": random.randint(3, 8),
                    "shape": random.randint(0, 2)  # 0: circle, 1: rect, 2: splatter
                })
            
            # Create chains
            cls.chains = []
            for _ in range(3):
                x = random.randint(50, 750)
                length = random.randint(50, 150)
                cls.chains.append({
                    "x": x,
                    "y": 0,
                    "length": length,
                    "segments": random.randint(5, 10),
                    "swing": random.uniform(0, math.pi * 2),
                    "swing_speed": random.uniform(0.01, 0.05)
                })
            
            cls.embers = []
            cls.initialized = True
    
    @classmethod
    def stop(cls):
        """Stop everything and clear all drawn elements"""
        # Reset state variables
        cls.selected_character = 0
        cls.animation_timer = 0
        cls.torch_flicker = 0
        cls.dust_particles = []
        cls.blood_splatters = []
        cls.chains = []
        cls.embers = []
        cls.initialized = False
    
    @classmethod
    def handle_event(cls, event):
        """Handle pygame events for character selection"""
        import pygame  # Import locally to avoid initialization
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cls.selected_character = (cls.selected_character - 1) % len(cls.character_classes)
                return True
            elif event.key == pygame.K_RIGHT:
                cls.selected_character = (cls.selected_character + 1) % len(cls.character_classes)
                return True
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                # Return the selected character
                return cls.character_classes[cls.selected_character]["name"]
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if clicked on a character
                spacing = 120  # Reduced spacing to fit 5 characters
                start_x = 400 - (spacing * (len(cls.character_classes) - 1))//2
                
                for i in range(len(cls.character_classes)):
                    x_pos = start_x + i * spacing
                    y_pos = 300 - 50
                    
                    # Simple hit box
                    if x_pos <= event.pos[0] <= x_pos + 80 and y_pos <= event.pos[1] <= y_pos + 80:
                        cls.selected_character = i
                        return True
        
        return False
    
    @classmethod
    def get_selected_character(cls):
        """Return the currently selected character data"""
        return cls.character_classes[cls.selected_character]
    
    @classmethod
    def update(cls, dt=1/30):
        """Update animations and particles"""
        cls.animation_timer += 0.05
        cls.torch_flicker += 0.1
        
        # Update chains
        for chain in cls.chains:
            chain["swing"] += chain["swing_speed"]
        
        # Update embers
        for i in range(len(cls.embers) - 1, -1, -1):
            ember = cls.embers[i]
            ember["x"] += ember["speed_x"]
            ember["y"] += ember["speed_y"]
            ember["life"] -= 1
            
            if ember["life"] <= 0:
                cls.embers.pop(i)
        
        # Generate new embers
        if random.random() < 0.1:
            torch_positions = [(50, 100), (750, 100), (50, 450), (750, 450)]
            tx, ty = random.choice(torch_positions)
            cls.embers.append({
                "x": tx + random.randint(-5, 5),
                "y": ty - random.randint(0, 10),
                "size": random.randint(1, 3),
                "speed_x": random.uniform(-0.5, 0.5),
                "speed_y": random.uniform(-1, -0.5),
                "life": random.randint(20, 40)
            })
        
        # Update dust particles
        for particle in cls.dust_particles:
            particle["y"] += particle["speed"]
            if particle["y"] > 600:
                particle["y"] = 0
                particle["x"] = random.randint(0, 800)
    
    @classmethod
    def draw_character(cls, screen, x, y, char_index, selected=False):
        """Draw a character at the specified position"""
        import pygame  # Import locally to avoid initialization
        
        # Base character size - smaller to fit all characters
        size = 80
        
        # Character data
        char_data = cls.character_classes[char_index]
        body_color = char_data["highlight"] if selected else char_data["color"]
        
        # Animation offsets
        bounce = math.sin(cls.animation_timer * 2) * 3 if selected else 0
        weapon_swing = math.sin(cls.animation_timer) * 5 if selected else 0
        
        # Draw character shadow
        shadow_size = size // 2
        shadow_surface = pygame.Surface((shadow_size, shadow_size // 4), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, shadow_size, shadow_size // 4))
        screen.blit(shadow_surface, (x + size // 4, y + size - shadow_size // 4))
        
        # Draw character body (pixelated style)
        y_offset = int(bounce)
        
        # Different drawing based on character type
        if char_data["name"] == "KNIGHT":
            # Draw legs
            leg_width = size // 5
            leg_height = size // 3
            pygame.draw.rect(screen, cls.DARK_GRAY, (x + size // 3 - leg_width // 2, y + size - leg_height + y_offset, leg_width, leg_height))
            pygame.draw.rect(screen, cls.DARK_GRAY, (x + size - size // 3 - leg_width // 2, y + size - leg_height + y_offset, leg_width, leg_height))
            
            # Draw body (armored)
            body_height = size // 2
            pygame.draw.rect(screen, body_color, (x + size // 6, y + size - leg_height - body_height + y_offset, size - size // 3, body_height))
            
            # Draw head with helmet
            head_size = size // 2
            pygame.draw.rect(screen, body_color, (x + size // 4, y + size - leg_height - body_height - head_size + y_offset, head_size, head_size))
            
            # Draw helmet visor
            visor_width = head_size // 2
            visor_height = head_size // 4
            visor_y = y + size - leg_height - body_height - head_size + head_size // 3 + y_offset
            pygame.draw.rect(screen, cls.BLACK, (x + size // 4 + head_size // 4, visor_y, visor_width, visor_height))
            
            # Draw sword and shield
            shield_x = x - 10 + weapon_swing
            shield_y = y + size // 2 + y_offset
            pygame.draw.rect(screen, cls.BLUE, (shield_x, shield_y, 15, 30))
            pygame.draw.rect(screen, cls.GOLD, (shield_x + 2, shield_y + 2, 11, 26))
            
            sword_x = x + size + 5
            sword_y = y + size // 2 + y_offset - weapon_swing
            pygame.draw.rect(screen, cls.LIGHT_GRAY, (sword_x, sword_y, 8, 40))
            pygame.draw.rect(screen, cls.GOLD, (sword_x - 10, sword_y, 28, 8))
            
        elif char_data["name"] == "WIZZARD":
            # Draw legs
            leg_width = size // 6
            leg_height = size // 3
            pygame.draw.rect(screen, cls.DARK_GRAY, (x + size // 3 - leg_width // 2, y + size - leg_height + y_offset, leg_width, leg_height))
            pygame.draw.rect(screen, cls.DARK_GRAY, (x + size - size // 3 - leg_width // 2, y + size - leg_height + y_offset, leg_width, leg_height))
            
            # Draw robe
            robe_width = size - size // 4
            robe_height = size - leg_height // 2
            pygame.draw.rect(screen, body_color, (x + size // 8, y + y_offset, robe_width, robe_height))
            
            # Draw head
            head_size = size // 2
            pygame.draw.rect(screen, cls.LIGHT_GRAY, (x + size // 4, y - head_size // 2 + y_offset, head_size, head_size))
            
            # Draw wizard hat
            hat_width = head_size + 10
            hat_height = head_size
            pygame.draw.polygon(screen, body_color, [
                (x + size // 4 - 5, y - head_size // 2 + y_offset),
                (x + size // 4 + head_size + 5, y - head_size // 2 + y_offset),
                (x + size // 2, y - head_size - 15 + y_offset)
            ])
            
            # Draw eyes
            eye_size = head_size // 6
            eye_y = y - head_size // 4 + y_offset
            pygame.draw.rect(screen, cls.BLACK, (x + size // 3, eye_y, eye_size, eye_size))
            pygame.draw.rect(screen, cls.BLACK, (x + size - size // 3, eye_y, eye_size, eye_size))
            
            # Draw staff with glowing orb
            staff_x = x + size + 5
            staff_y = y + y_offset
            pygame.draw.rect(screen, cls.BROWN, (staff_x, staff_y, 6, size))
            
            # Glowing orb with pulsing effect
            orb_size = 12 + int(math.sin(cls.animation_timer * 3) * 3)
            orb_surface = pygame.Surface((orb_size * 2, orb_size * 2), pygame.SRCALPHA)
            
            # Draw multiple circles for glow effect
            for r in range(orb_size, 0, -2):
                alpha = 150 if r == orb_size else 50 - int(50 * r / orb_size)
                pygame.draw.circle(orb_surface, (200, 100, 255, alpha), (orb_size, orb_size), r)
            
            screen.blit(orb_surface, (staff_x - orb_size + 3, staff_y - orb_size))
            
        elif char_data["name"] == "THIEF":
            # Draw legs
            leg_width = size // 6
            leg_height = size // 3
            pygame.draw.rect(screen, cls.DARK_GRAY, (x + size // 3 - leg_width // 2, y + size - leg_height + y_offset, leg_width, leg_height))
            pygame.draw.rect(screen, cls.DARK_GRAY, (x + size - size // 3 - leg_width // 2, y + size - leg_height + y_offset, leg_width, leg_height))
            
            # Draw body (slim)
            body_height = size // 2
            body_width = size - size // 2
            pygame.draw.rect(screen, body_color, (x + size // 4, y + size - leg_height - body_height + y_offset, body_width, body_height))
            
            # Draw head with hood
            head_size = size // 2
            pygame.draw.rect(screen, cls.LIGHT_GRAY, (x + size // 4, y + size - leg_height - body_height - head_size + y_offset, head_size, head_size))
            pygame.draw.rect(screen, body_color, (x + size // 4 - 5, y + size - leg_height - body_height - head_size + y_offset, head_size + 10, head_size // 2))
            
            # Draw eyes (sneaky)
            eye_color = cls.RED if selected else cls.WHITE
            eye_size = head_size // 8
            eye_y = y + size - leg_height - body_height - head_size + head_size // 3 + y_offset
            
            pygame.draw.rect(screen, cls.BLACK, (x + size // 3, eye_y, eye_size, eye_size))
            pygame.draw.rect(screen, eye_color, (x + size // 3 + 1, eye_y + 1, eye_size - 2, eye_size - 2))
            
            pygame.draw.rect(screen, cls.BLACK, (x + size - size // 3, eye_y, eye_size, eye_size))
            pygame.draw.rect(screen, eye_color, (x + size - size // 3 + 1, eye_y + 1, eye_size - 2, eye_size - 2))
            
            # Draw daggers
            dagger1_x = x + size + 5
            dagger1_y = y + size // 2 + y_offset - weapon_swing
            pygame.draw.rect(screen, cls.LIGHT_GRAY, (dagger1_x, dagger1_y, 5, 25))
            pygame.draw.rect(screen, cls.DARK_GRAY, (dagger1_x, dagger1_y - 5, 5, 5))
            
            dagger2_x = x + size + 15
            dagger2_y = y + size // 2 + 10 + y_offset + weapon_swing
            pygame.draw.rect(screen, cls.LIGHT_GRAY, (dagger2_x, dagger2_y, 5, 25))
            pygame.draw.rect(screen, cls.DARK_GRAY, (dagger2_x, dagger2_y - 5, 5, 5))
            
        elif char_data["name"] == "GOBLIN":
            # Draw legs (short)
            leg_width = size // 6
            leg_height = size // 4
            pygame.draw.rect(screen, cls.DARK_GRAY, (x + size // 3 - leg_width // 2, y + size - leg_height + y_offset, leg_width, leg_height))
            pygame.draw.rect(screen, cls.DARK_GRAY, (x + size - size // 3 - leg_width // 2, y + size - leg_height + y_offset, leg_width, leg_height))
            
            # Draw body (hunched)
            body_height = size // 2
            body_width = size - size // 3
            pygame.draw.rect(screen, body_color, (x + size // 6, y + size - leg_height - body_height + y_offset, body_width, body_height))
            
            # Draw head (large with pointy ears)
            head_size = size // 2 + 5
            pygame.draw.rect(screen, body_color, (x + size // 4 - 5, y + size - leg_height - body_height - head_size + 10 + y_offset, head_size, head_size))
            
            # Draw pointy ears
            ear_width = head_size // 4
            ear_height = head_size // 2
            pygame.draw.polygon(screen, body_color, [
                (x + size // 4 - 5, y + size - leg_height - body_height - head_size // 2 + y_offset),
                (x + size // 4 - 15, y + size - leg_height - body_height - head_size + y_offset),
                (x + size // 4, y + size - leg_height - body_height - head_size // 2 + y_offset)
            ])
            pygame.draw.polygon(screen, body_color, [
                (x + size // 4 + head_size - 5, y + size - leg_height - body_height - head_size // 2 + y_offset),
                (x + size // 4 + head_size + 5, y + size - leg_height - body_height - head_size + y_offset),
                (x + size // 4 + head_size - 10, y + size - leg_height - body_height - head_size // 2 + y_offset)
            ])
            
            # Draw eyes (beady)
            eye_color = cls.RED if selected else cls.WHITE
            eye_size = head_size // 6
            eye_y = y + size - leg_height - body_height - head_size // 2 + y_offset
            
            pygame.draw.rect(screen, cls.BLACK, (x + size // 3 - 5, eye_y, eye_size, eye_size))
            pygame.draw.rect(screen, eye_color, (x + size // 3 - 5 + 1, eye_y + 1, eye_size - 2, eye_size - 2))
            
            pygame.draw.rect(screen, cls.BLACK, (x + size - size // 3, eye_y, eye_size, eye_size))
            pygame.draw.rect(screen, eye_color, (x + size - size // 3 + 1, eye_y + 1, eye_size - 2, eye_size - 2))
            
            # Draw mouth (toothy grin)
            mouth_width = head_size // 2
            mouth_height = head_size // 6
            mouth_y = y + size - leg_height - body_height - head_size // 4 + y_offset
            pygame.draw.rect(screen, cls.BLACK, (x + size // 4 + head_size // 4, mouth_y, mouth_width, mouth_height))
            
            # Draw teeth
            teeth_width = mouth_width // 5
            teeth_height = mouth_height // 2
            for i in range(3):
                teeth_x = x + size // 4 + head_size // 4 + i * teeth_width * 2
                pygame.draw.rect(screen, cls.WHITE, (teeth_x, mouth_y, teeth_width, teeth_height))
            
            # Draw spear
            spear_x = x + size + 5
            spear_y = y + y_offset
            pygame.draw.rect(screen, cls.BROWN, (spear_x, spear_y, 5, size))
            pygame.draw.polygon(screen, cls.LIGHT_GRAY, [
                (spear_x, spear_y),
                (spear_x + 15, spear_y - 10),
                (spear_x + 5, spear_y - 20),
                (spear_x - 5, spear_y - 10)
            ])
            
        elif char_data["name"] == "RAT":
            # Draw rat body (oval)
            body_width = size
            body_height = size // 2
            pygame.draw.ellipse(screen, body_color, (x, y + size // 2 + y_offset, body_width, body_height))
            
            # Draw head
            head_size = size // 2
            pygame.draw.ellipse(screen, body_color, (x + body_width - head_size // 2, y + size // 2 - head_size // 4 + y_offset, head_size, head_size))
            
            # Draw ears
            ear_size = head_size // 3
            pygame.draw.ellipse(screen, body_color, (x + body_width - head_size // 4, y + size // 2 - head_size // 2 + y_offset, ear_size, ear_size))
            pygame.draw.ellipse(screen, body_color, (x + body_width + head_size // 4, y + size // 2 - head_size // 2 + y_offset, ear_size, ear_size))
            
            # Draw eyes (beady)
            eye_color = cls.RED
            eye_size = head_size // 8
            eye_y = y + size // 2 + y_offset
            
            pygame.draw.circle(screen, cls.BLACK, (x + body_width + head_size // 4, eye_y), eye_size)
            pygame.draw.circle(screen, eye_color, (x + body_width + head_size // 4, eye_y), eye_size - 1)
            
            # Draw whiskers
            whisker_length = head_size // 2
            whisker_y = y + size // 2 + head_size // 4 + y_offset
            whisker_x = x + body_width + head_size // 2
            
            for i in range(3):
                offset_y = (i - 1) * 3
                pygame.draw.line(screen, cls.LIGHT_GRAY, (whisker_x, whisker_y + offset_y), (whisker_x + whisker_length, whisker_y + offset_y - 5), 1)
                pygame.draw.line(screen, cls.LIGHT_GRAY, (whisker_x, whisker_y + offset_y), (whisker_x + whisker_length, whisker_y + offset_y + 5), 1)
            
            # Draw tail
            tail_length = size
            tail_points = []
            for i in range(10):
                tail_x = x - i * (tail_length // 10)
                tail_y = y + size // 2 + body_height // 2 + math.sin(i / 2 + cls.animation_timer) * 3 + y_offset
                tail_points.append((tail_x, tail_y))
            
            if len(tail_points) > 1:
                pygame.draw.lines(screen, body_color, False, tail_points, 3)
            
            # Draw feet
            feet_width = body_width // 8
            feet_height = body_height // 4
            
            # Front feet
            pygame.draw.ellipse(screen, cls.DARK_GRAY, (x + body_width - feet_width * 2, y + size // 2 + body_height - feet_height // 2 + y_offset, feet_width, feet_height))
            pygame.draw.ellipse(screen, cls.DARK_GRAY, (x + body_width - feet_width * 4, y + size // 2 + body_height - feet_height // 2 + y_offset, feet_width, feet_height))
            
            # Back feet
            pygame.draw.ellipse(screen, cls.DARK_GRAY, (x + feet_width, y + size // 2 + body_height - feet_height // 2 + y_offset, feet_width, feet_height))
            pygame.draw.ellipse(screen, cls.DARK_GRAY, (x + feet_width * 3, y + size // 2 + body_height - feet_height // 2 + y_offset, feet_width, feet_height))
        
        # Selection indicator
        if selected:
            # Animated border
            border_thickness = 3
            border_offset = int(math.sin(cls.animation_timer * 4) * 2)
            border_rect = (x - border_thickness - border_offset, 
                          y - border_thickness - border_offset + y_offset, 
                          size + 2 * border_thickness + border_offset * 2, 
                          size + 2 * border_thickness + border_offset * 2)
            
            pygame.draw.rect(screen, cls.GOLD, border_rect, border_thickness)
            
            # Corner highlights
            corner_size = 8
            for corner_x, corner_y in [(border_rect[0], border_rect[1]), 
                                      (border_rect[0] + border_rect[2] - corner_size, border_rect[1]),
                                      (border_rect[0], border_rect[1] + border_rect[3] - corner_size),
                                      (border_rect[0] + border_rect[2] - corner_size, border_rect[1] + border_rect[3] - corner_size)]:
                pygame.draw.rect(screen, cls.GOLD, (corner_x, corner_y, corner_size, corner_size))
            
            # Draw name with glow effect
            font = pygame.font.SysFont("monospace", 16)
            name_text = font.render(char_data["name"], True, cls.GOLD)
            name_glow = font.render(char_data["name"], True, char_data["highlight"])
            
            name_x = x + size // 2 - name_text.get_width() // 2
            name_y = y - 25 + y_offset
            
            # Glow effect
            screen.blit(name_glow, (name_x - 1, name_y))
            screen.blit(name_glow, (name_x + 1, name_y))
            screen.blit(name_glow, (name_x, name_y - 1))
            screen.blit(name_glow, (name_x, name_y + 1))
            
            # Actual text
            screen.blit(name_text, (name_x, name_y))
        else:
            # Just draw the name without effects
            font = pygame.font.SysFont("monospace", 16)
            name_text = font.render(char_data["name"], True, cls.WHITE)
            name_x = x + size // 2 - name_text.get_width() // 2
            name_y = y - 20
            screen.blit(name_text, (name_x, name_y))
    
    @classmethod
    def draw_background(cls, screen):
        """Draw the dungeon background with all effects"""
        import pygame  # Import locally to avoid initialization
        
        # Screen dimensions
        SCREEN_WIDTH = screen.get_width()
        SCREEN_HEIGHT = screen.get_height()
        
        # Dark background
        screen.fill(cls.BLACK)
        
        # Draw stone wall pattern
        stone_size = 40
        for y in range(0, SCREEN_HEIGHT, stone_size):
            offset = stone_size // 2 if (y // stone_size) % 2 == 1 else 0
            for x in range(-offset, SCREEN_WIDTH, stone_size):
                # Vary stone color slightly for more texture
                darkness = random.randint(-10, 10)
                stone_color = (
                    max(10, min(50, cls.DARK_GRAY[0] + darkness)),
                    max(10, min(50, cls.DARK_GRAY[1] + darkness)),
                    max(10, min(50, cls.DARK_GRAY[2] + darkness))
                )
                
                # Draw stone block with slight randomization
                stone_rect = (x, y, stone_size - 2, stone_size - 2)
                pygame.draw.rect(screen, stone_color, stone_rect)
                
                # Draw cracks in some stones
                if random.random() < 0.2:
                    crack_points = []
                    start_x = x + random.randint(5, stone_size - 7)
                    start_y = y + random.randint(5, stone_size - 7)
                    crack_points.append((start_x, start_y))
                    
                    # Generate random crack path
                    for _ in range(random.randint(2, 5)):
                        next_x = crack_points[-1][0] + random.randint(-8, 8)
                        next_y = crack_points[-1][1] + random.randint(-8, 8)
                        # Keep within stone boundaries
                        next_x = max(x + 2, min(x + stone_size - 4, next_x))
                        next_y = max(y + 2, min(y + stone_size - 4, next_y))
                        crack_points.append((next_x, next_y))
                    
                    # Draw the crack
                    if len(crack_points) > 1:
                        pygame.draw.lines(screen, cls.DARK_GRAY, False, crack_points, 1)
        
        # Draw blood splatters
        for splatter in cls.blood_splatters:
            if splatter["shape"] == 0:
                # Circle splatter
                pygame.draw.circle(screen, cls.BLOOD_RED, (splatter["x"], splatter["y"]), splatter["size"])
            elif splatter["shape"] == 1:
                # Rectangle splatter
                pygame.draw.rect(screen, cls.BLOOD_RED, (splatter["x"], splatter["y"], splatter["size"] * 2, splatter["size"]))
            else:
                # Random splatter shape
                points = []
                for i in range(5):
                    angle = i * (2 * math.pi / 5)
                    distance = splatter["size"] + random.randint(-2, 2)
                    px = splatter["x"] + int(math.cos(angle) * distance)
                    py = splatter["y"] + int(math.sin(angle) * distance)
                    points.append((px, py))
                pygame.draw.polygon(screen, cls.BLOOD_RED, points)
        
        # Draw chains
        for chain in cls.chains:
            angle = math.sin(chain["swing"]) * 0.3
            
            # Calculate chain points
            points = [(chain["x"], 0)]
            segment_length = chain["length"] / chain["segments"]
            
            for i in range(1, chain["segments"] + 1):
                # Each segment hangs lower and swings more
                segment_angle = angle * (i / chain["segments"]) * 2
                x_offset = math.sin(segment_angle) * (segment_length * i * 0.5)
                y_pos = segment_length * i
                points.append((chain["x"] + x_offset, y_pos))
            
            # Draw chain segments
            for i in range(len(points) - 1):
                start = points[i]
                end = points[i + 1]
                
                # Draw thick line for chain
                pygame.draw.line(screen, cls.LIGHT_GRAY, start, end, 3)
                
                # Draw chain link
                link_center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
                pygame.draw.circle(screen, cls.LIGHT_GRAY, link_center, 4)
        
        # Draw torches with flickering effect
        torch_positions = [(50, 100), (SCREEN_WIDTH - 50, 100), 
                           (50, SCREEN_HEIGHT - 150), (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 150)]
        
        for tx, ty in torch_positions:
            # Torch base
            pygame.draw.rect(screen, cls.DARK_BROWN, (tx - 5, ty, 10, 30))
            
            # Flickering flame
            flicker = math.sin(cls.torch_flicker + tx * 0.1) * 3
            flame_height = 20 + int(flicker)
            flame_width = 14 + int(flicker)
            
            # Draw flame layers
            flame_colors = [(255, 200, 50), (255, 150, 50), (200, 50, 0)]
            for i, color in enumerate(flame_colors):
                size_factor = 1 - (i * 0.2)
                pygame.draw.polygon(screen, color, [
                    (tx, ty),
                    (tx - flame_width//2 * size_factor, ty - flame_height//2 * size_factor),
                    (tx, ty - flame_height * size_factor),
                    (tx + flame_width//2 * size_factor, ty - flame_height//2 * size_factor)
                ])
            
            # Light effect (simple circle gradient)
            max_radius = 100 + int(flicker * 5)
            for r in range(max_radius, 0, -20):
                alpha = 20 - int(20 * r / max_radius)
                s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 200, 100, alpha), (r, r), r)
                screen.blit(s, (tx - r, ty - r))
        
        # Update and draw dust particles
        for particle in cls.dust_particles:
            s = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, particle["color"], (particle["size"], particle["size"]), particle["size"])
            screen.blit(s, (particle["x"], particle["y"]))
        
        # Update and draw embers
        for ember in cls.embers:
            # Draw ember with fading effect
            alpha = min(255, ember["life"] * 6)
            color = (255, 200, 50, alpha)
            s = pygame.Surface((ember["size"] * 2, ember["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (ember["size"], ember["size"]), ember["size"])
            screen.blit(s, (ember["x"] - ember["size"], ember["y"] - ember["size"]))
    
    @classmethod
    def draw_character_details(cls, screen):
        """Draw the details panel for the selected character"""
        import pygame  # Import locally to avoid initialization
        
        SCREEN_WIDTH = screen.get_width()
        SCREEN_HEIGHT = screen.get_height()
        
        char_data = cls.character_classes[cls.selected_character]
        
        # Stats background
        stats_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT - 160, 400, 140)
        
        # Semi-transparent background
        s = pygame.Surface((stats_rect.width, stats_rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (stats_rect.x, stats_rect.y))
        
        # Border with character color
        pygame.draw.rect(screen, char_data["color"], stats_rect, 2)
        
        # Character name
        title_font = pygame.font.SysFont("monospace", 30)
        title_font.set_bold(True)
        name_text = title_font.render(char_data["name"], True, char_data["color"])
        screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, SCREEN_HEIGHT - 155))
        
        # Character description
        pixel_font = pygame.font.SysFont("monospace", 14)
        desc_lines = []
        words = char_data["description"].split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if pixel_font.size(test_line)[0] < 380:
                line = test_line
            else:
                desc_lines.append(line)
                line = word + " "
        if line:
            desc_lines.append(line)
        
        for i, line in enumerate(desc_lines):
            desc_text = pixel_font.render(line, True, cls.WHITE)
            screen.blit(desc_text, (SCREEN_WIDTH//2 - 190, SCREEN_HEIGHT - 125 + i * 16))
        
        # Weapon and special
        weapon_text = pixel_font.render(f"WEAPON: {char_data['weapon']}", True, cls.GOLD)
        screen.blit(weapon_text, (SCREEN_WIDTH//2 - 190, SCREEN_HEIGHT - 90))
        
        special_text = pixel_font.render(f"SPECIAL: {char_data['special']}", True, cls.GOLD)
        screen.blit(special_text, (SCREEN_WIDTH//2 - 190, SCREEN_HEIGHT - 75))
        
        weakness_text = pixel_font.render(f"WEAKNESS: {char_data['weakness']}", True, cls.RED)
        screen.blit(weakness_text, (SCREEN_WIDTH//2 - 190, SCREEN_HEIGHT - 60))
        
        # Stats
        stat_x = SCREEN_WIDTH//2 + 20
        stat_y = SCREEN_HEIGHT - 90
        stat_width = 150
        stat_height = 8
        
        stats_font = pygame.font.SysFont("monospace", 14)
        for i, (stat, value) in enumerate(char_data["stats"].items()):
            # Stat name
            stat_text = stats_font.render(stat, True, cls.WHITE)
            screen.blit(stat_text, (stat_x, stat_y + i * 15))
            
            # Stat bar background
            pygame.draw.rect(screen, cls.DARK_GRAY, (stat_x + 40, stat_y + i * 15 + 3, stat_width, stat_height))
            
            # Stat bar value
            bar_width = int((value / 10) * stat_width)
            
            # Determine color based on stat value
            if value >= 8:
                bar_color = cls.GREEN
            elif value >= 5:
                bar_color = cls.GOLD
            else:
                bar_color = cls.RED
                
            pygame.draw.rect(screen, bar_color, (stat_x + 40, stat_y + i * 15 + 3, bar_width, stat_height))
            
            # Stat value text
            value_text = stats_font.render(str(value), True, cls.WHITE)
            screen.blit(value_text, (stat_x + 40 + stat_width + 5, stat_y + i * 15))
        
        # Draw selection prompt
        select_text = pixel_font.render("PRESS ENTER TO SELECT", True, cls.GOLD)
        screen.blit(select_text, (SCREEN_WIDTH//2 - select_text.get_width()//2, SCREEN_HEIGHT - 30))
    
    @classmethod
    def draw_ui(cls, screen):
        """Draw title and UI elements"""
        import pygame  # Import locally to avoid initialization
        
        SCREEN_WIDTH = screen.get_width()
        SCREEN_HEIGHT = screen.get_height()
        
        # Draw title with blood dripping effect
        title_font = pygame.font.SysFont("monospace", 36)
        title_font.set_bold(True)
        title = title_font.render("CHOOSE YOUR CHAMPION", True, cls.GOLD)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        
        # Blood drips from title
        for i in range(5):
            drip_x = SCREEN_WIDTH//2 - title.get_width()//2 + random.randint(0, title.get_width())
            drip_length = random.randint(5, 20)
            drip_width = random.randint(2, 4)
            
            # Make drips animate
            drip_offset = (cls.animation_timer * 30 + i * 50) % 50
            
            pygame.draw.rect(screen, cls.BLOOD_RED, (drip_x, 70 + drip_offset, drip_width, drip_length))
        
        # Draw subtitle with fear theme
        pixel_font = pygame.font.SysFont("monospace", 16)
        subtitle = pixel_font.render("ONLY THE BRAVE SURVIVE THE DUNGEON", True, cls.RED)
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 80))
        
        # Draw instructions
        instructions = pixel_font.render("ARROW KEYS: NAVIGATE   ENTER: SELECT   MOUSE: CLICK TO CHOOSE", True, cls.WHITE)
        screen.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, SCREEN_HEIGHT - 20))
    
    @classmethod
    def draw(cls, screen):
        """Draw the entire character selection screen"""
        # Initialize if not already done
        if not cls.initialized:
            cls.initialize()
        
        # Update animations and particles
        cls.update()
        
        # Get screen dimensions
        SCREEN_WIDTH = screen.get_width()
        SCREEN_HEIGHT = screen.get_height()
        
        # Draw everything
        cls.draw_background(screen)
        cls.draw_ui(screen)
        
        # Draw character selection - adjusted spacing for 5 characters
        spacing = 120  # Reduced spacing to fit 5 characters
        start_x = SCREEN_WIDTH//2 - (spacing * (len(cls.character_classes) - 1))//2
        
        for i, char in enumerate(cls.character_classes):
            x_pos = start_x + i * spacing
            y_pos = SCREEN_HEIGHT//2 - 50
            
            # Character platform (stone)
            platform_width = 100
            platform_height = 15
            import pygame
            pygame.draw.rect(screen, cls.DARK_GRAY, (x_pos - 10, y_pos + 80, platform_width, platform_height))
            
            # Platform shadow
            shadow_surface = pygame.Surface((platform_width, platform_height//2), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, platform_width, platform_height//2))
            screen.blit(shadow_surface, (x_pos - 10, y_pos + 80 + platform_height))
            
            # Draw character
            cls.draw_character(screen, x_pos, y_pos, i, i == cls.selected_character)
        
        # Draw stats for selected character
        cls.draw_character_details(screen)