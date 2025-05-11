import random
import math
import pygame

class MainMenu:
    # Static class variables
    BLACK = (0, 0, 0)
    DARK_GRAY = (20, 20, 20)
    GRAY = (50, 50, 50)
    LIGHT_GRAY = (100, 100, 100)
    BROWN = (80, 60, 30)
    DARK_BROWN = (40, 30, 15)
    DARK_RED = (120, 20, 20)
    BLOOD_RED = (180, 30, 30)
    TORCH_YELLOW = (230, 180, 50)
    TORCH_ORANGE = (220, 120, 30)
    MOSS_GREEN = (60, 100, 40)
    WATER_BLUE = (40, 80, 120)
    WHITE = (255, 255, 255)
    
    # State variables - will be initialized when needed
    initialized = False
    title_font = None
    button_font = None
    info_font = None
    background = None
    torches = []
    puddles = []
    chains = []
    buttons = []
    skulls = []
    blood_drips = []
    rats = []
    fog = None
    screen_shake = None
    
    # Animation variables
    title_y = 150
    title_offset = 0
    title_dir = 1
    rat_spawn_timer = 0
    ambient_timer = 0
    last_time = 0
    
    # Screen dimensions
    WIDTH = 800
    HEIGHT = 600
    
    @classmethod
    def stop(cls):
        """Stop all animations and reset the state"""
        # Reset initialization flag
        cls.initialized = False
        
        # Clear all game elements
        cls.title_font = None
        cls.button_font = None
        cls.info_font = None
        cls.background = None
        cls.torches = []
        cls.puddles = []
        cls.chains = []
        cls.buttons = []
        cls.skulls = []
        cls.blood_drips = []
        cls.rats = []
        cls.fog = None
        cls.screen_shake = None
        
        # Reset animation variables
        cls.title_offset = 0
        cls.title_dir = 1
        cls.rat_spawn_timer = 0
        cls.ambient_timer = 0
        cls.last_time = 0
        
        # This ensures that the next time render is called, everything will be reinitialized
        print("MainMenu stopped and reset")
    
    @classmethod
    def render(cls, screen):
        """Render the menu to the provided screen"""
        import pygame  # Import pygame here to ensure it's available
        
        # Get screen dimensions
        cls.WIDTH, cls.HEIGHT = screen.get_size()
        
        # Initialize if not already done
        if not cls.initialized:
            cls._initialize(pygame)
        
        # Calculate delta time
        current_time = pygame.time.get_ticks()
        dt = current_time - cls.last_time if cls.last_time > 0 else 16
        cls.last_time = current_time
        
        # Handle input
        cls._handle_input(pygame)
        
        # Update game elements
        cls._update(dt)
        
        # Get screen shake offset
        shake_offset = cls.screen_shake.get_offset()
        
        # Draw background
        screen.blit(cls.background, shake_offset)
        
        # Draw puddles
        for puddle in cls.puddles:
            puddle.draw(screen)
        
        # Draw blood drips
        for drip in cls.blood_drips:
            drip.draw(pygame, screen)
        
        # Draw floating skulls
        for skull in cls.skulls:
            skull.draw(pygame, screen)
        
        # Draw rats
        for rat in cls.rats:
            rat.draw(pygame, screen)
        
        # Draw chains
        for chain in cls.chains:
            chain.draw(pygame, screen)
        
        # Draw torches
        for torch in cls.torches:
            torch.draw(pygame, screen)
        
        # Draw fog
        cls.fog.draw(pygame, screen)
        
        # Draw title with shadow and slight movement
        title_text = cls.title_font.render("DUNGEON DEPTHS", True, cls.BLOOD_RED)
        shadow_text = cls.title_font.render("DUNGEON DEPTHS", True, cls.BLACK)
        
        # Draw shadow
        shadow_rect = shadow_text.get_rect(center=(cls.WIDTH//2 + 4 + shake_offset[0], 
                                                 cls.title_y + 4 + cls.title_offset + shake_offset[1]))
        screen.blit(shadow_text, shadow_rect)
        
        # Draw main text
        title_rect = title_text.get_rect(center=(cls.WIDTH//2 + shake_offset[0], 
                                               cls.title_y + cls.title_offset + shake_offset[1]))
        screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = cls.info_font.render("NEW GAME", True, cls.LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(cls.WIDTH//2 + shake_offset[0], 
                                                     220 + shake_offset[1]))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw level text
        level_text = cls.info_font.render("HIGHEST LEVEL: 7", True, cls.TORCH_YELLOW)
        level_rect = level_text.get_rect(center=(cls.WIDTH//2 + shake_offset[0], 
                                               250 + shake_offset[1]))
        screen.blit(level_text, level_rect)
        
        # Draw buttons
        for button in cls.buttons:
            button.draw(pygame, screen)
        
        # Draw version info
        version_text = cls.info_font.render("v1.0.0", True, cls.GRAY)
        version_rect = version_text.get_rect(bottomright=(cls.WIDTH-20 + shake_offset[0], 
                                                        cls.HEIGHT-20 + shake_offset[1]))
        screen.blit(version_text, version_rect)
    
    @classmethod
    def _initialize(cls, pygame):
        """Initialize all game elements"""
        # Set up fonts
        cls.title_font = pygame.font.Font(None, 72)
        cls.button_font = pygame.font.Font(None, 36)
        cls.info_font = pygame.font.Font(None, 24)
        
        # Create background texture
        cls.background = cls._create_stone_texture(pygame, cls.WIDTH, cls.HEIGHT, ((30, 30, 30), (50, 50, 50)))
        
        # Create torches
        cls.torches = [
            cls.Torch(pygame, 100, 100),
            cls.Torch(pygame, cls.WIDTH - 100 - 16, 100),
            cls.Torch(pygame, 100, cls.HEIGHT - 150),
            cls.Torch(pygame, cls.WIDTH - 100 - 16, cls.HEIGHT - 150)
        ]
        
        # Create water puddles
        cls.puddles = [
            cls.WaterPuddle(pygame, 200, cls.HEIGHT - 80, 60, 30),
            cls.WaterPuddle(pygame, cls.WIDTH - 250, cls.HEIGHT - 100, 80, 40)
        ]
        
        # Create chains
        cls.chains = [
            cls.Chain(pygame, 150, 0, 8),
            cls.Chain(pygame, cls.WIDTH - 150, 0, 10),
            cls.Chain(pygame, cls.WIDTH//2 - 100, 0, 6),
            cls.Chain(pygame, cls.WIDTH//2 + 100, 0, 7)
        ]
        
        # Create buttons
        button_width, button_height = 200, 50
        cls.buttons = [
            cls.PixelButton(pygame, cls.WIDTH//2 - button_width//2, 300, button_width, button_height, 
                          "START", lambda: print("Start button clicked")),
            cls.PixelButton(pygame, cls.WIDTH//2 - button_width//2, 370, button_width, button_height, 
                          "SHOP", lambda: print("Shop button clicked")),
            cls.PixelButton(pygame, cls.WIDTH//2 - button_width//2, 440, button_width, button_height, 
                          "LOAD", lambda: print("Load button clicked"))
        ]
        
        # Create floating skulls
        cls.skulls = [cls.FloatingSkull() for _ in range(5)]
        
        # Blood drips
        cls.blood_drips = [cls.BloodDrip(random.randint(0, cls.WIDTH)) for _ in range(8)]
        
        # Fog effect
        cls.fog = cls.FogEffect()
        
        # Screen shake
        cls.screen_shake = cls.ScreenShake()
        
        cls.initialized = True
        print("MainMenu initialized")
    
    @classmethod
    def _create_stone_texture(cls, pygame, width, height, colors):
        """Create a stone texture surface"""
        surface = pygame.Surface((width, height))
        
        # Base color
        surface.fill(colors[0])
        
        # Add noise for texture
        for y in range(0, height, 4):
            for x in range(0, width, 4):
                if random.random() < 0.5:
                    # Random stone block size
                    block_w = random.randint(4, 12)
                    block_h = random.randint(4, 12)
                    
                    # Random color variation
                    color_variation = random.randint(-10, 10)
                    stone_color = tuple(max(0, min(255, c + color_variation)) for c in colors[1])
                    
                    # Draw the stone block
                    pygame.draw.rect(surface, stone_color, (x, y, block_w, block_h))
        
        # Add cracks
        for _ in range(50):
            start_x = random.randint(0, width)
            start_y = random.randint(0, height)
            length = random.randint(5, 30)
            angle = random.uniform(0, 2 * math.pi)
            
            end_x = int(start_x + length * math.cos(angle))
            end_y = int(start_y + length * math.sin(angle))
            
            # Draw crack
            pygame.draw.line(surface, (20, 20, 20), (start_x, start_y), (end_x, end_y), 1)
        
        # Add moss patches
        for _ in range(20):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(5, 15)
            
            # Draw moss patch
            pygame.draw.circle(surface, cls.MOSS_GREEN, (x, y), radius)
            
            # Blend moss with background
            for i in range(10):
                blend_radius = radius - i/2
                if blend_radius > 0:
                    blend_color = (
                        int(cls.MOSS_GREEN[0] * (1 - i/10) + colors[0][0] * (i/10)),
                        int(cls.MOSS_GREEN[1] * (1 - i/10) + colors[0][1] * (i/10)),
                        int(cls.MOSS_GREEN[2] * (1 - i/10) + colors[0][2] * (i/10))
                    )
                    pygame.draw.circle(surface, blend_color, (x, y), blend_radius)
        
        return surface
    
    @classmethod
    def _handle_input(cls, pygame):
        """Handle user input"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        # Update buttons
        for button in cls.buttons:
            button.update(mouse_pos, mouse_pressed)
    
    @classmethod
    def _update(cls, dt):
        """Update game elements"""
        # Update title floating animation
        cls.title_offset += 0.05 * cls.title_dir * (dt / 16)
        if abs(cls.title_offset) > 5:
            cls.title_dir *= -1
        
        # Update torches
        for torch in cls.torches:
            torch.update(dt)
        
        # Update chains
        for chain in cls.chains:
            chain.update(dt)
        
        # Update floating skulls
        for skull in cls.skulls:
            skull.update(dt)
        
        # Update blood drips
        for drip in cls.blood_drips:
            drip.update(dt)
        
        # Update rats
        for i in range(len(cls.rats) - 1, -1, -1):
            cls.rats[i].update(dt)
            if cls.rats[i].x < -50 or cls.rats[i].x > cls.WIDTH + 50:
                cls.rats.pop(i)
        
        # Spawn new rats occasionally
        cls.rat_spawn_timer += dt
        if cls.rat_spawn_timer > 5000:  # Every 5 seconds
            cls.rat_spawn_timer = 0
            if len(cls.rats) < 3 and random.random() < 0.3:
                if random.random() < 0.5:
                    cls.rats.append(cls.Rat(-30, cls.HEIGHT - 30, 1))
                else:
                    cls.rats.append(cls.Rat(cls.WIDTH + 30, cls.HEIGHT - 30, -1))
        
        # Update fog
        cls.fog.update(dt)
        
        # Random ambient effects
        cls.ambient_timer += dt
        if cls.ambient_timer > 2000:  # Every 2 seconds
            cls.ambient_timer = 0
            if random.random() < 0.1:
                cls.screen_shake.start(5, 200)  # Small shake
    
    # Nested classes for game elements
    class Torch:
        def __init__(self, pygame, x, y):
            self.x = x
            self.y = y
            self.width = 16
            self.height = 32
            self.flame_offset = 0
            self.flame_dir = 1
            self.flame_size = random.uniform(0.8, 1.2)
            self.flame_color = MainMenu.TORCH_YELLOW
            self.particles = []
            
            # Create torch base texture
            self.torch_base = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(self.torch_base, MainMenu.DARK_BROWN, (4, 0, 8, 24))
            pygame.draw.rect(self.torch_base, MainMenu.BROWN, (6, 2, 4, 20))
            
        def update(self, dt):
            # Update flame animation
            self.flame_offset += 0.2 * self.flame_dir * (dt / 16)
            if abs(self.flame_offset) > 3:
                self.flame_dir *= -1
            
            # Update flame color
            r = random.randint(-20, 20)
            g = random.randint(-20, 10)
            self.flame_color = (
                max(180, min(255, MainMenu.TORCH_YELLOW[0] + r)),
                max(150, min(200, MainMenu.TORCH_YELLOW[1] + g)),
                max(30, min(70, MainMenu.TORCH_YELLOW[2]))
            )
            
            # Add new particles
            if random.random() < 0.3 * (dt / 16):
                self.particles.append({
                    'x': self.x + 8 + random.uniform(-2, 2),
                    'y': self.y - 5 + random.uniform(-2, 2),
                    'vx': random.uniform(-0.5, 0.5),
                    'vy': random.uniform(-1.5, -0.5),
                    'size': random.uniform(1, 3),
                    'life': 1.0
                })
            
            # Update particles
            for i in range(len(self.particles) - 1, -1, -1):
                p = self.particles[i]
                p['x'] += p['vx'] * (dt / 16)
                p['y'] += p['vy'] * (dt / 16)
                p['life'] -= 0.02 * (dt / 16)
                if p['life'] <= 0:
                    self.particles.pop(i)
        
        def draw(self, pygame, screen):
            # Draw torch base
            screen.blit(self.torch_base, (self.x, self.y))
            
            # Draw flame
            flame_x = self.x + 8 + self.flame_offset
            flame_y = self.y - 5
            
            # Draw flame glow
            glow_radius = 40 * self.flame_size
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            for r in range(int(glow_radius), 0, -2):
                alpha = max(0, min(150, int(255 * (r / glow_radius))))
                color = (*self.flame_color, alpha)
                pygame.draw.circle(glow_surface, color, (glow_radius, glow_radius), r)
            
            screen.blit(glow_surface, (flame_x - glow_radius, flame_y - glow_radius), special_flags=pygame.BLEND_ADD)
            
            # Draw flame
            flame_points = [
                (flame_x, flame_y),
                (flame_x - 5 * self.flame_size, flame_y - 8 * self.flame_size),
                (flame_x, flame_y - 15 * self.flame_size),
                (flame_x + 5 * self.flame_size, flame_y - 8 * self.flame_size)
            ]
            pygame.draw.polygon(screen, self.flame_color, flame_points)
            
            # Draw particles
            for p in self.particles:
                alpha = int(255 * p['life'])
                color = (*self.flame_color, alpha)
                pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), int(p['size']))
    
    class WaterPuddle:
        def __init__(self, pygame, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = MainMenu.WATER_BLUE
            self.ripples = []
            self.time = 0
            
            # Create puddle surface
            self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.ellipse(self.surface, (*self.color, 150), (0, 0, width, height))
            
            # Add some ripples
            for _ in range(3):
                self.ripples.append({
                    'x': random.uniform(0.3, 0.7) * width,
                    'y': random.uniform(0.3, 0.7) * height,
                    'size': random.uniform(5, 15),
                    'max_size': random.uniform(15, 25),
                    'growth': random.uniform(0.1, 0.3),
                    'alpha': 255
                })
        
        def update(self, dt):
            self.time += dt
            
            # Update ripples
            for i in range(len(self.ripples) - 1, -1, -1):
                r = self.ripples[i]
                r['size'] += r['growth'] * (dt / 16)
                r['alpha'] = max(0, r['alpha'] - 5 * (dt / 16))
                
                if r['size'] >= r['max_size'] or r['alpha'] <= 0:
                    self.ripples.pop(i)
            
            # Add new ripples occasionally
            if random.random() < 0.01 * (dt / 16) and len(self.ripples) < 5:
                self.ripples.append({
                    'x': random.uniform(0.3, 0.7) * self.width,
                    'y': random.uniform(0.3, 0.7) * self.height,
                    'size': 5,
                    'max_size': random.uniform(15, 25),
                    'growth': random.uniform(0.1, 0.3),
                    'alpha': 255
                })
        
        def draw(self, screen):
            # Draw puddle
            screen.blit(self.surface, (self.x, self.y))
            
            # Draw ripples
            for r in self.ripples:
                pygame.draw.circle(screen, (*self.color, int(r['alpha'])), 
                                 (int(self.x + r['x']), int(self.y + r['y'])), 
                                 int(r['size']), 1)
    
    class Chain:
        def __init__(self, pygame, x, y, length):
            self.x = x
            self.y = y
            self.length = length
            self.links = []
            self.swing_angle = random.uniform(-0.1, 0.1)
            self.swing_speed = random.uniform(0.01, 0.02)
            self.swing_dir = 1 if random.random() < 0.5 else -1
            
            # Create chain links
            for i in range(length):
                self.links.append({
                    'x': x,
                    'y': y + i * 15,
                    'angle': 0
                })
        
        def update(self, dt):
            # Update swing animation
            self.swing_angle += self.swing_speed * self.swing_dir * (dt / 16)
            if abs(self.swing_angle) > 0.2:
                self.swing_dir *= -1
            
            # Update chain links
            for i, link in enumerate(self.links):
                if i == 0:
                    link['angle'] = self.swing_angle
                else:
                    # Each link follows the previous one with a slight delay
                    prev_link = self.links[i-1]
                    angle_diff = prev_link['angle'] - link['angle']
                    link['angle'] += angle_diff * 0.1 * (dt / 16)
                
                # Calculate position based on angle
                if i == 0:
                    link['x'] = self.x
                    link['y'] = self.y
                else:
                    prev_link = self.links[i-1]
                    link['x'] = prev_link['x'] + 15 * math.sin(link['angle'])
                    link['y'] = prev_link['y'] + 15 * math.cos(link['angle'])
        
        def draw(self, pygame, screen):
            # Draw chain links
            for i, link in enumerate(self.links):
                pygame.draw.circle(screen, MainMenu.GRAY, (int(link['x']), int(link['y'])), 4)
                
                # Draw connection to previous link
                if i > 0:
                    prev_link = self.links[i-1]
                    pygame.draw.line(screen, MainMenu.GRAY, 
                                   (int(prev_link['x']), int(prev_link['y'])), 
                                   (int(link['x']), int(link['y'])), 2)
    
    class PixelButton:
        def __init__(self, pygame, x, y, width, height, text, action=None):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.action = action
            self.hovered = False
            self.clicked = False
            self.font = pygame.font.Font(None, 36)
            
            # Create button surfaces
            self.normal_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            self.hovered_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            self.clicked_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Normal state
            pygame.draw.rect(self.normal_surface, MainMenu.DARK_BROWN, (0, 0, width, height))
            pygame.draw.rect(self.normal_surface, MainMenu.BROWN, (4, 4, width-8, height-8))
            
            # Hovered state
            pygame.draw.rect(self.hovered_surface, MainMenu.DARK_BROWN, (0, 0, width, height))
            pygame.draw.rect(self.hovered_surface, (MainMenu.BROWN[0]+20, MainMenu.BROWN[1]+20, MainMenu.BROWN[2]+20), (4, 4, width-8, height-8))
            
            # Clicked state
            pygame.draw.rect(self.clicked_surface, MainMenu.DARK_BROWN, (0, 0, width, height))
            pygame.draw.rect(self.clicked_surface, (MainMenu.BROWN[0]-20, MainMenu.BROWN[1]-20, MainMenu.BROWN[2]-20), (4, 4, width-8, height-8))
        
        def update(self, mouse_pos, mouse_pressed):
            # Check if mouse is over button
            self.hovered = (self.x <= mouse_pos[0] <= self.x + self.width and 
                           self.y <= mouse_pos[1] <= self.y + self.height)
            
            # Handle click
            if self.hovered and mouse_pressed and not self.clicked:
                self.clicked = True
                if self.action:
                    self.action()
            elif not mouse_pressed:
                self.clicked = False
        
        def draw(self, pygame, screen):
            # Draw button background
            if self.clicked:
                screen.blit(self.clicked_surface, (self.x, self.y))
            elif self.hovered:
                screen.blit(self.hovered_surface, (self.x, self.y))
            else:
                screen.blit(self.normal_surface, (self.x, self.y))
            
            # Draw text
            text_color = MainMenu.WHITE if self.hovered else MainMenu.LIGHT_GRAY
            text_surface = self.font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
            
            # Add slight offset when clicked
            if self.clicked:
                text_rect.x += 2
                text_rect.y += 2
            
            screen.blit(text_surface, text_rect)
    
    class FloatingSkull:
        def __init__(self):
            self.x = random.randint(0, MainMenu.WIDTH)
            self.y = random.randint(100, MainMenu.HEIGHT - 200)
            self.size = random.randint(20, 40)
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-0.3, 0.3)
            self.rotation = random.uniform(0, 360)
            self.rotation_speed = random.uniform(-1, 1)
            self.glow_intensity = random.uniform(0.5, 1.0)
            self.glow_dir = 1 if random.random() < 0.5 else -1
        
        def update(self, dt):
            # Update position
            self.x += self.vx * (dt / 16)
            self.y += self.vy * (dt / 16)
            
            # Bounce off edges
            if self.x < 0 or self.x > MainMenu.WIDTH:
                self.vx *= -1
            if self.y < 100 or self.y > MainMenu.HEIGHT - 200:
                self.vy *= -1
            
            # Update rotation
            self.rotation += self.rotation_speed * (dt / 16)
            
            # Update glow
            self.glow_intensity += 0.01 * self.glow_dir * (dt / 16)
            if self.glow_intensity < 0.5 or self.glow_intensity > 1.0:
                self.glow_dir *= -1
        
        def draw(self, pygame, screen):
            # Create skull surface
            skull_surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            
            # Draw skull glow
            glow_radius = int(self.size * 1.5 * self.glow_intensity)
            glow_color = (100, 255, 100, 50)  # Green ghostly glow
            pygame.draw.circle(skull_surface, glow_color, (self.size, self.size), glow_radius)
            
            # Draw skull
            skull_color = (220, 220, 200, 200)  # Off-white with transparency
            
            # Draw skull shape (simplified)
            pygame.draw.circle(skull_surface, skull_color, (self.size, self.size), self.size)
            
            # Draw eye sockets
            eye_size = self.size // 3
            eye_offset = self.size // 3
            pygame.draw.circle(skull_surface, (0, 0, 0, 200), (self.size - eye_offset, self.size - eye_offset//2), eye_size)
            pygame.draw.circle(skull_surface, (0, 0, 0, 200), (self.size + eye_offset, self.size - eye_offset//2), eye_size)
            
            # Draw nose
            nose_size = self.size // 4
            pygame.draw.circle(skull_surface, (0, 0, 0, 150), (self.size, self.size + eye_offset//2), nose_size)
            
            # Draw teeth
            teeth_width = self.size // 5
            teeth_height = self.size // 3
            pygame.draw.rect(skull_surface, (0, 0, 0, 150), 
                           (self.size - teeth_width*2, self.size + eye_offset, teeth_width*4, teeth_height))
            
            # Rotate skull
            rotated_skull = pygame.transform.rotate(skull_surface, self.rotation)
            rotated_rect = rotated_skull.get_rect(center=(self.x, self.y))
            
            # Draw to screen
            screen.blit(rotated_skull, rotated_rect)
    
    class BloodDrip:
        def __init__(self, x):
            self.x = x
            self.y = random.randint(-50, 0)
            self.speed = random.uniform(0.5, 2.0)
            self.size = random.randint(3, 8)
            self.active = True
            self.splat = False
            self.splat_time = 0
            self.splat_particles = []
        
        def update(self, dt):
            if self.active:
                # Update position
                self.y += self.speed * (dt / 16)
                
                # Check if hit bottom
                if self.y > MainMenu.HEIGHT and not self.splat:
                    self.splat = True
                    self.active = False
                    self.splat_time = 0
                    
                    # Create splat particles
                    for _ in range(5):
                        self.splat_particles.append({
                            'x': self.x,
                            'y': MainMenu.HEIGHT,
                            'vx': random.uniform(-2, 2),
                            'vy': random.uniform(-4, -1),
                            'size': random.uniform(1, 3),
                            'life': 1.0
                        })
            elif self.splat:
                # Update splat animation
                self.splat_time += dt
                
                # Update splat particles
                for i in range(len(self.splat_particles) - 1, -1, -1):
                    p = self.splat_particles[i]
                    p['x'] += p['vx'] * (dt / 16)
                    p['y'] += p['vy'] * (dt / 16)
                    p['vy'] += 0.1 * (dt / 16)  # Gravity
                    p['life'] -= 0.02 * (dt / 16)
                    
                    if p['life'] <= 0:
                        self.splat_particles.pop(i)
                
                # Reset if splat animation is done
                if self.splat_time > 2000:  # 2 seconds
                    self.y = random.randint(-50, 0)
                    self.x = random.randint(0, MainMenu.WIDTH)
                    self.speed = random.uniform(0.5, 2.0)
                    self.size = random.randint(3, 8)
                    self.active = True
                    self.splat = False
        
        def draw(self, pygame, screen):
            if self.active:
                # Draw blood drip
                pygame.draw.circle(screen, MainMenu.BLOOD_RED, (int(self.x), int(self.y)), self.size)
                
                # Draw trail
                for i in range(1, 4):
                    trail_y = self.y - i * 5
                    if trail_y > 0:
                        trail_size = self.size * (1 - i * 0.2)
                        pygame.draw.circle(screen, MainMenu.BLOOD_RED, (int(self.x), int(trail_y)), int(trail_size))
            elif self.splat:
                # Draw splat particles
                for p in self.splat_particles:
                    alpha = int(255 * p['life'])
                    pygame.draw.circle(screen, (*MainMenu.BLOOD_RED, alpha), 
                                     (int(p['x']), int(p['y'])), 
                                     int(p['size']))
    
    class Rat:
        def __init__(self, x, y, direction):
            self.x = x
            self.y = y
            self.direction = direction  # 1 for right, -1 for left
            self.speed = random.uniform(1.0, 2.0)
            self.size = random.randint(8, 12)
            self.frame = 0
            self.frame_time = 0
            self.frame_count = 4
            self.frame_duration = 100  # milliseconds
        
        def update(self, dt):
            # Update position
            self.x += self.speed * self.direction * (dt / 16)
            
            # Update animation
            self.frame_time += dt
            if self.frame_time >= self.frame_duration:
                self.frame_time = 0
                self.frame = (self.frame + 1) % self.frame_count
        
        def draw(self, pygame, screen):
            # Draw rat (simple animation)
            body_length = self.size * 2
            
            # Calculate leg positions based on animation frame
            leg_offset = [2, 0, -2, 0][self.frame]
            
            # Draw body
            pygame.draw.ellipse(screen, (80, 70, 60), 
                              (int(self.x - body_length/2), int(self.y - self.size/2), 
                               int(body_length), int(self.size)))
            
            # Draw head
            head_x = self.x + body_length/2 * self.direction
            pygame.draw.circle(screen, (80, 70, 60), 
                             (int(head_x), int(self.y)), 
                             int(self.size * 0.7))
            
            # Draw eyes
            eye_x = head_x + self.size * 0.3 * self.direction
            pygame.draw.circle(screen, (0, 0, 0), 
                             (int(eye_x), int(self.y - self.size * 0.2)), 
                             int(self.size * 0.15))
            
            # Draw ears
            ear_x = head_x - self.size * 0.2 * self.direction
            pygame.draw.circle(screen, (100, 90, 80), 
                             (int(ear_x), int(self.y - self.size * 0.5)), 
                             int(self.size * 0.3))
            
            # Draw legs
            for i in range(4):
                leg_x = self.x - body_length/3 + (i * body_length/3) * self.direction
                leg_y = self.y + self.size/2
                
                # Alternate legs up and down
                leg_offset_y = leg_offset if i % 2 == 0 else -leg_offset
                
                pygame.draw.line(screen, (80, 70, 60), 
                               (int(leg_x), int(leg_y)), 
                               (int(leg_x), int(leg_y + self.size + leg_offset_y)), 
                               int(self.size * 0.3))
            
            # Draw tail
            tail_start_x = self.x - body_length/2 * self.direction
            pygame.draw.line(screen, (100, 90, 80), 
                           (int(tail_start_x), int(self.y)), 
                           (int(tail_start_x - body_length * self.direction), int(self.y - self.size * 0.5)), 
                           int(self.size * 0.2))
    
    class FogEffect:
        def __init__(self):
            self.particles = []
            self.time = 0
            
            # Create initial fog particles
            for _ in range(50):
                self.particles.append({
                    'x': random.randint(0, MainMenu.WIDTH),
                    'y': random.randint(0, MainMenu.HEIGHT),
                    'size': random.randint(50, 150),
                    'speed': random.uniform(0.1, 0.3),
                    'alpha': random.randint(10, 40)
                })
        
        def update(self, dt):
            self.time += dt
            
            # Update fog particles
            for p in self.particles:
                p['x'] += p['speed'] * math.sin(self.time / 1000 + p['y'] / 100) * (dt / 16)
                p['y'] += p['speed'] * math.cos(self.time / 1000 + p['x'] / 100) * (dt / 16)
                
                # Wrap around screen
                if p['x'] < -p['size']:
                    p['x'] = MainMenu.WIDTH + p['size']
                elif p['x'] > MainMenu.WIDTH + p['size']:
                    p['x'] = -p['size']
                
                if p['y'] < -p['size']:
                    p['y'] = MainMenu.HEIGHT + p['size']
                elif p['y'] > MainMenu.HEIGHT + p['size']:
                    p['y'] = -p['size']
        
        def draw(self, pygame, screen):
            # Draw fog particles
            for p in self.particles:
                fog_surface = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(fog_surface, (200, 200, 220, p['alpha']), 
                                 (p['size'], p['size']), p['size'])
                screen.blit(fog_surface, (int(p['x'] - p['size']), int(p['y'] - p['size'])))
    
    class ScreenShake:
        def __init__(self):
            self.intensity = 0
            self.duration = 0
            self.start_time = 0
            self.active = False
        
        def start(self, intensity, duration):
            self.intensity = intensity
            self.duration = duration
            self.start_time = pygame.time.get_ticks()
            self.active = True
        
        def get_offset(self):
            if not self.active:
                return (0, 0)
            
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.start_time
            
            if elapsed > self.duration:
                self.active = False
                return (0, 0)
            
            # Calculate remaining intensity based on time
            remaining = 1 - (elapsed / self.duration)
            current_intensity = self.intensity * remaining
            
            # Calculate random offset
            offset_x = random.uniform(-current_intensity, current_intensity)
            offset_y = random.uniform(-current_intensity, current_intensity)
            
            return (offset_x, offset_y)