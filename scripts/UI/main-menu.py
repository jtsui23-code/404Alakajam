import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DUNGEON DEPTHS")

# Colors
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

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Pixelated font simulation
def pixel_font(size):
    # Try to use a pixelated font if available, otherwise use default
    try:
        return pygame.font.Font(None, size)
    except:
        return pygame.font.Font(None, size)

title_font = pixel_font(72)
button_font = pixel_font(36)
info_font = pixel_font(24)

# Create pixelated textures
def create_stone_texture(width, height, color_range=((40, 40, 40), (70, 70, 70))):
    """Create a pixelated stone wall texture"""
    texture = pygame.Surface((width, height))
    pixel_size = 4  # Size of each "pixel" in our texture
    
    # Create base pattern for stones
    stones = []
    for _ in range(100):
        stone_width = random.randint(3, 8) * pixel_size
        stone_height = random.randint(2, 6) * pixel_size
        x = random.randint(0, width - stone_width)
        y = random.randint(0, height - stone_height)
        stones.append((x, y, stone_width, stone_height))
    
    # Fill background with dark color
    texture.fill((30, 30, 35))
    
    # Draw stones
    for x, y, w, h in stones:
        # Random stone color
        color = (
            random.randint(color_range[0][0], color_range[1][0]),
            random.randint(color_range[0][1], color_range[1][1]),
            random.randint(color_range[0][2], color_range[1][2])
        )
        pygame.draw.rect(texture, color, (x, y, w, h))
        
        # Add some darker pixels for grout
        for i in range(0, w, pixel_size):
            for j in range(0, h, pixel_size):
                if random.random() < 0.2:
                    dark_color = (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20))
                    pygame.draw.rect(texture, dark_color, (x + i, y + j, pixel_size, pixel_size))
    
    # Add moss in some areas
    for _ in range(20):
        moss_x = random.randint(0, width - 20)
        moss_y = random.randint(0, height - 20)
        moss_size = random.randint(10, 30)
        
        for i in range(moss_size):
            mx = moss_x + random.randint(-10, 10)
            my = moss_y + random.randint(-10, 10)
            if 0 <= mx < width and 0 <= my < height:
                # Random moss color
                moss_color = (
                    random.randint(40, 70),
                    random.randint(80, 120),
                    random.randint(30, 50)
                )
                pygame.draw.rect(texture, moss_color, (mx, my, pixel_size, pixel_size))
    
    return texture

def create_wood_texture(width, height):
    """Create a pixelated wooden texture"""
    texture = pygame.Surface((width, height))
    pixel_size = 4
    
    # Draw wood grain lines
    for y in range(0, height, pixel_size):
        # Base wood color with some variation
        base_color = (
            random.randint(60, 80),
            random.randint(40, 60),
            random.randint(20, 30)
        )
        
        # Add grain curve
        grain_offset = int(10 * math.sin(y / 20))
        
        for x in range(0, width, pixel_size):
            # Add some noise to the wood grain
            noise = random.randint(-10, 10)
            grain_value = (math.sin((x + grain_offset) / 10) + 1) * 5
            color = (
                max(0, min(255, base_color[0] + noise + grain_value)),
                max(0, min(255, base_color[1] + noise)),
                max(0, min(255, base_color[2] + noise))
            )
            pygame.draw.rect(texture, color, (x, y, pixel_size, pixel_size))
            
            # Add darker grain lines occasionally
            if random.random() < 0.1:
                dark_color = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
                pygame.draw.rect(texture, dark_color, (x, y, pixel_size, pixel_size))
    
    # Add some knots in the wood
    for _ in range(random.randint(1, 3)):
        knot_x = random.randint(10, width - 20)
        knot_y = random.randint(10, height - 20)
        knot_size = random.randint(5, 10)
        
        for r in range(knot_size, 0, -1):
            color = (
                min(80 + (knot_size - r) * 3, 110),
                min(50 + (knot_size - r) * 2, 70),
                min(30 + (knot_size - r), 40)
            )
            pygame.draw.circle(texture, color, (knot_x, knot_y), r)
    
    return texture

# Create blood splatter
def create_blood_splatter(width, height):
    """Create a pixelated blood splatter texture"""
    texture = pygame.Surface((width, height))
    texture.fill(BLACK)  # Start with black (transparent)
    texture.set_colorkey(BLACK)  # Make black transparent
    
    # Create several blood drops
    for _ in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(2, 8)
        
        # Random blood color
        color = (
            random.randint(120, 180),
            random.randint(10, 30),
            random.randint(10, 30)
        )
        
        # Draw the blood drop
        pygame.draw.circle(texture, color, (x, y), size)
        
        # Add some drips
        if random.random() < 0.5:
            drip_length = random.randint(5, 15)
            drip_width = max(1, size // 2)
            pygame.draw.line(texture, color, (x, y), (x, y + drip_length), drip_width)
            
            # Sometimes add a blood pool at the end of the drip
            if random.random() < 0.3:
                pool_size = random.randint(size, size * 2)
                pygame.draw.circle(texture, color, (x, y + drip_length), pool_size)
    
    return texture

# Create torch flame animation frames
def create_torch_frames(width, height, num_frames=8):
    """Create pixelated torch flame animation frames"""
    frames = []
    
    for _ in range(num_frames):
        frame = pygame.Surface((width, height))
        frame.fill(BLACK)
        frame.set_colorkey(BLACK)
        
        # Base of flame
        pygame.draw.rect(frame, TORCH_ORANGE, (width//4, height//2, width//2, height//2))
        
        # Flame shape
        points = [
            (width//4, height//2),
            (width//4, height//4),
            (width//2, 0),
            (3*width//4, height//4),
            (3*width//4, height//2)
        ]
        
        # Add some randomness to the flame
        for i in range(1, 4):
            points[i] = (
                points[i][0] + random.randint(-width//8, width//8),
                points[i][1] + random.randint(-height//8, height//8)
            )
        
        pygame.draw.polygon(frame, TORCH_ORANGE, points)
        
        # Inner flame (brighter)
        inner_points = [
            (width//3, height//2),
            (width//3, height//3),
            (width//2, height//8),
            (2*width//3, height//3),
            (2*width//3, height//2)
        ]
        
        # Add some randomness to the inner flame
        for i in range(1, 4):
            inner_points[i] = (
                inner_points[i][0] + random.randint(-width//10, width//10),
                inner_points[i][1] + random.randint(-height//10, height//10)
            )
        
        pygame.draw.polygon(frame, TORCH_YELLOW, inner_points)
        
        # Add some sparks
        for _ in range(random.randint(0, 3)):
            spark_x = width//2 + random.randint(-width//4, width//4)
            spark_y = random.randint(0, height//2)
            spark_size = random.randint(1, 3)
            pygame.draw.circle(frame, TORCH_YELLOW, (spark_x, spark_y), spark_size)
        
        frames.append(frame)
    
    return frames

# Create water puddle animation
def create_water_puddle_frames(width, height, num_frames=4):
    """Create pixelated water puddle animation frames"""
    frames = []
    
    for frame_num in range(num_frames):
        frame = pygame.Surface((width, height))
        frame.fill(BLACK)
        frame.set_colorkey(BLACK)
        
        # Base puddle shape
        puddle_rect = pygame.Rect(0, 0, width, height)
        pygame.draw.ellipse(frame, WATER_BLUE, puddle_rect)
        
        # Add ripples
        ripple_offset = frame_num * (2 * math.pi / num_frames)
        for i in range(3):
            ripple_radius = width//2 - i * 5 - int(3 * math.sin(ripple_offset + i))
            ripple_color = (
                max(0, WATER_BLUE[0] - i * 10),
                max(0, WATER_BLUE[1] - i * 5),
                min(255, WATER_BLUE[2] + i * 10)
            )
            pygame.draw.ellipse(frame, ripple_color, 
                              (width//2 - ripple_radius, height//2 - ripple_radius//2, 
                               ripple_radius * 2, ripple_radius))
        
        frames.append(frame)
    
    return frames

# Create chain link
def create_chain_link(width, height):
    """Create a pixelated chain link"""
    link = pygame.Surface((width, height))
    link.fill(BLACK)
    link.set_colorkey(BLACK)
    
    # Draw the outer shape of the link
    pygame.draw.ellipse(link, GRAY, (0, 0, width, height))
    pygame.draw.ellipse(link, BLACK, (width//4, height//4, width//2, height//2))
    
    # Add highlight
    pygame.draw.arc(link, LIGHT_GRAY, (0, 0, width, height), 0, math.pi/2, 2)
    
    return link

# Torch class
class Torch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 32
        self.frames = create_torch_frames(self.width, self.height)
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 100  # milliseconds
        
        # Create torch base
        self.base = pygame.Surface((self.width, self.height//2))
        self.base.fill(DARK_BROWN)
        
        # Add some metal details to the torch base
        pygame.draw.rect(self.base, GRAY, (self.width//4, 0, self.width//2, self.height//8))
        pygame.draw.rect(self.base, GRAY, (self.width//4, self.height//4, self.width//2, self.height//8))
        
    def update(self, dt):
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_time = 0
            
    def draw(self, surface):
        # Draw torch base
        surface.blit(self.base, (self.x, self.y + self.height//2))
        
        # Draw flame
        surface.blit(self.frames[self.current_frame], (self.x, self.y))
        
        # Draw light effect (simple circle)
        light_surf = pygame.Surface((200, 200))
        light_surf.fill(BLACK)
        light_surf.set_colorkey(BLACK)
        
        # Draw radial gradient for light
        for radius in range(100, 0, -5):
            alpha = max(0, 100 - radius)
            color = (TORCH_YELLOW[0], TORCH_YELLOW[1], TORCH_YELLOW[2])
            pygame.draw.circle(light_surf, color, (100, 100), radius)
        
        # Blit with additive blending for glow effect
        surface.blit(light_surf, (self.x - 92 + self.width//2, self.y - 92 + self.height//2), 
                   special_flags=pygame.BLEND_RGB_ADD)

# Water puddle class
class WaterPuddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.frames = create_water_puddle_frames(width, height)
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 250  # milliseconds
        
    def update(self, dt):
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_time = 0
            
    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], (self.x, self.y))

# Chain class
class Chain:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.link_width = 12
        self.link_height = 20
        self.links = []
        self.swing_angle = 0
        self.swing_speed = random.uniform(0.01, 0.03)
        self.swing_range = random.uniform(0.05, 0.15)
        
        # Create chain links
        self.link_image = create_chain_link(self.link_width, self.link_height)
        
        for i in range(length):
            self.links.append({
                'x': 0,
                'y': i * (self.link_height - 5),
                'angle': 0
            })
            
    def update(self, dt):
        # Update swing animation
        self.swing_angle += self.swing_speed
        current_angle = math.sin(self.swing_angle) * self.swing_range
        
        # Update link positions
        for i, link in enumerate(self.links):
            # Each link swings more than the one above it
            link_factor = (i + 1) / len(self.links)
            link['angle'] = current_angle * link_factor
            
            # Calculate position based on angle
            if i == 0:
                link['x'] = 0
                link['y'] = 0
            else:
                prev_link = self.links[i-1]
                link['x'] = prev_link['x'] + math.sin(link['angle']) * (self.link_height - 5)
                link['y'] = prev_link['y'] + math.cos(link['angle']) * (self.link_height - 5)
            
    def draw(self, surface):
        for link in self.links:
            # Create a rotated copy of the link image
            rotated_link = pygame.transform.rotate(self.link_image, math.degrees(link['angle']))
            link_rect = rotated_link.get_rect(center=(self.x + link['x'], self.y + link['y']))
            surface.blit(rotated_link, link_rect)

# Pixelated button class
class PixelButton:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.clicked = False
        self.wood_texture = create_wood_texture(width, height)
        self.blood_splatter = None
        self.hover_offset = 0
        self.hover_dir = 1
        
        # Add blood splatter to some buttons randomly
        if random.random() < 0.5:
            self.blood_splatter = create_blood_splatter(width, height)
        
    def update(self, mouse_pos, mouse_clicked):
        previous_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Handle click
        if self.hovered and mouse_clicked:
            self.clicked = True
            if self.action:
                self.action()
        else:
            self.clicked = False
            
        # Update hover animation
        if self.hovered:
            self.hover_offset += 0.2 * self.hover_dir
            if self.hover_offset > 3:
                self.hover_dir = -1
            elif self.hover_offset < 0:
                self.hover_dir = 1
        else:
            self.hover_offset = 0
            self.hover_dir = 1
            
        # Return True if hover state changed
        return self.hovered != previous_hovered
            
    def draw(self, surface):
        # Create a copy of the rect for drawing
        draw_rect = self.rect.copy()
        
        # Apply hover effect
        if self.hovered:
            draw_rect.y -= int(self.hover_offset)
        
        # Draw button base with wood texture
        surface.blit(self.wood_texture, draw_rect)
        
        # Draw border
        border_color = BLOOD_RED if self.hovered else DARK_BROWN
        border_width = 3 if self.hovered else 2
        pygame.draw.rect(surface, border_color, draw_rect, border_width)
        
        # Draw blood splatter if it exists
        if self.blood_splatter:
            surface.blit(self.blood_splatter, draw_rect)
        
        # Draw text with shadow
        text_color = WHITE if self.hovered else LIGHT_GRAY
        text_surf = button_font.render(self.text, True, text_color)
        
        # Add pixelated shadow effect
        shadow_surf = button_font.render(self.text, True, BLACK)
        shadow_rect = shadow_surf.get_rect(center=(draw_rect.centerx + 2, draw_rect.centery + 2))
        surface.blit(shadow_surf, shadow_rect)
        
        # Draw main text
        text_rect = text_surf.get_rect(center=draw_rect.center)
        surface.blit(text_surf, text_rect)
        
        # Draw "pressed" effect
        if self.clicked:
            # Darken the button when clicked
            dark_overlay = pygame.Surface((draw_rect.width, draw_rect.height))
            dark_overlay.fill(BLACK)
            dark_overlay.set_alpha(100)
            surface.blit(dark_overlay, draw_rect)
            
            # Add some blood particles when clicked
            if random.random() < 0.3:
                for _ in range(5):
                    x = random.randint(draw_rect.left, draw_rect.right)
                    y = random.randint(draw_rect.top, draw_rect.bottom)
                    size = random.randint(1, 3)
                    color = (
                        random.randint(150, 200),
                        random.randint(10, 30),
                        random.randint(10, 30)
                    )
                    pygame.draw.circle(surface, color, (x, y), size)

# Floating skull effect
class FloatingSkull:
    def __init__(self):
        self.size = 32
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(-0.5, 0.5)
        self.alpha = random.randint(50, 150)
        self.alpha_change = random.choice([-1, 1])
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-0.5, 0.5)
        
        # Create a simple pixel skull
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(BLACK)
        self.surface.set_colorkey(BLACK)
        
        # Draw skull shape
        pygame.draw.circle(self.surface, LIGHT_GRAY, (self.size//2, self.size//2), self.size//3)
        
        # Draw eye sockets
        eye_size = self.size//8
        pygame.draw.rect(self.surface, BLACK, (self.size//3 - eye_size//2, self.size//2 - eye_size//2, eye_size, eye_size))
        pygame.draw.rect(self.surface, BLACK, (2*self.size//3 - eye_size//2, self.size//2 - eye_size//2, eye_size, eye_size))
        
        # Draw nose
        pygame.draw.rect(self.surface, BLACK, (self.size//2 - eye_size//4, self.size//2 + eye_size//2, eye_size//2, eye_size//2))
        
        # Draw teeth
        teeth_width = self.size//10
        for i in range(3):
            pygame.draw.rect(self.surface, BLACK, 
                           (self.size//3 + i*teeth_width, 2*self.size//3, teeth_width, teeth_width))
            
        # Add glowing eyes occasionally
        if random.random() < 0.3:
            eye_color = TORCH_ORANGE
            pygame.draw.rect(self.surface, eye_color, 
                           (self.size//3 - eye_size//2, self.size//2 - eye_size//2, eye_size, eye_size))
            pygame.draw.rect(self.surface, eye_color, 
                           (2*self.size//3 - eye_size//2, self.size//2 - eye_size//2, eye_size, eye_size))
        
    def update(self):
        # Move the skull
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Rotate the skull
        self.rotation += self.rotation_speed
        
        # Bounce off edges
        if self.x < 0 or self.x > WIDTH - self.size:
            self.speed_x *= -1
        if self.y < 0 or self.y > HEIGHT - self.size:
            self.speed_y *= -1
            
        # Change alpha for fading effect
        self.alpha += self.alpha_change
        if self.alpha <= 50 or self.alpha >= 150:
            self.alpha_change *= -1
            
    def draw(self, surface):
        # Create a rotated copy
        rotated_skull = pygame.transform.rotate(self.surface, self.rotation)
        rotated_rect = rotated_skull.get_rect(center=(int(self.x + self.size//2), int(self.y + self.size//2)))
        
        # Create a copy with current alpha
        skull_surface = rotated_skull.copy()
        skull_surface.set_alpha(self.alpha)
        surface.blit(skull_surface, rotated_rect)

# Dripping blood effect
class BloodDrip:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(2, 4)
        self.color = (
            random.randint(120, 180),
            random.randint(10, 30),
            random.randint(10, 30)
        )
        self.length = random.randint(5, 20)
        self.active = True
        self.drip_timer = 0
        self.drip_interval = random.randint(300, 800)
        self.dripping = False
        self.drip_y = 0
        
    def update(self, dt):
        if not self.dripping:
            self.drip_timer += dt
            if self.drip_timer >= self.drip_interval:
                self.dripping = True
                self.drip_timer = 0
                self.drip_y = 0
        else:
            self.drip_y += self.speed
            if self.drip_y > HEIGHT:
                self.dripping = False
                self.drip_interval = random.randint(300, 800)
            
    def draw(self, surface):
        # Always draw the blood source at the top
        pygame.draw.circle(surface, self.color, (self.x, 5), self.size)
        
        # Draw the dripping blood when active
        if self.dripping:
            # Draw the drip
            pygame.draw.line(surface, self.color, 
                           (self.x, 5), 
                           (self.x, 5 + self.drip_y), 
                           self.size)
            # Draw the drop at the end
            pygame.draw.circle(surface, self.color, 
                             (self.x, 5 + self.drip_y), 
                             self.size)

# Rat class
class Rat:
    def __init__(self):
        self.width = 20
        self.height = 10
        self.x = random.choice([-self.width, WIDTH])
        self.y = random.randint(HEIGHT - 100, HEIGHT - self.height)
        self.speed = random.uniform(1, 3) * (-1 if self.x > 0 else 1)
        self.frame = 0
        self.frame_time = 0
        self.frame_duration = 100
        self.active = True
        
        # Create simple rat animation frames
        self.frames = []
        for i in range(4):
            frame = pygame.Surface((self.width, self.height))
            frame.fill(BLACK)
            frame.set_colorkey(BLACK)
            
            # Body
            pygame.draw.ellipse(frame, DARK_GRAY, (0, 0, self.width * 2//3, self.height))
            
            # Head
            pygame.draw.circle(frame, DARK_GRAY, 
                             (self.width * 2//3, self.height//2), 
                             self.height//2)
            
            # Tail
            tail_y = self.height//2 + int(math.sin(i * math.pi/2) * 2)
            pygame.draw.line(frame, DARK_GRAY, 
                           (0, self.height//2), 
                           (self.width//3, tail_y), 
                           2)
            
            # Eyes
            pygame.draw.circle(frame, BLACK, 
                             (self.width * 2//3 + 2, self.height//2 - 1), 
                             1)
            
            # Feet
            foot_offset = i % 2 * 2  # Alternate feet positions
            pygame.draw.line(frame, DARK_GRAY, 
                           (self.width//3, self.height), 
                           (self.width//3 + foot_offset, self.height + 2), 
                           1)
            pygame.draw.line(frame, DARK_GRAY, 
                           (self.width//2, self.height), 
                           (self.width//2 + foot_offset, self.height + 2), 
                           1)
            
            self.frames.append(frame)
        
    def update(self, dt):
        # Move the rat
        self.x += self.speed
        
        # Update animation
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.frame = (self.frame + 1) % len(self.frames)
            self.frame_time = 0
            
        # Check if rat has left the screen
        if (self.speed > 0 and self.x > WIDTH) or (self.speed < 0 and self.x < -self.width):
            self.active = False
            
    def draw(self, surface):
        # Flip the frame if moving right to left
        if self.speed < 0:
            frame = self.frames[self.frame]
        else:
            frame = pygame.transform.flip(self.frames[self.frame], True, False)
            
        surface.blit(frame, (int(self.x), int(self.y)))

# Fog effect
class FogEffect:
    def __init__(self):
        self.particles = []
        self.generate_particles()
        
    def generate_particles(self):
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'size': random.randint(20, 60),
                'speed': random.uniform(0.1, 0.5),
                'alpha': random.randint(10, 40)
            })
            
    def update(self):
        for particle in self.particles:
            # Move fog particles
            particle['x'] += particle['speed']
            
            # Wrap around screen
            if particle['x'] > WIDTH + particle['size']:
                particle['x'] = -particle['size']
                particle['y'] = random.randint(0, HEIGHT)
                
    def draw(self, surface):
        fog_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        for particle in self.particles:
            # Draw fog particle as a semi-transparent circle
            pygame.draw.circle(
                fog_surface, 
                (200, 200, 200, particle['alpha']), 
                (int(particle['x']), int(particle['y'])), 
                particle['size']
            )
            
        surface.blit(fog_surface, (0, 0))

# Screen shake effect
class ScreenShake:
    def __init__(self):
        self.intensity = 0
        self.duration = 0
        
    def start(self, intensity=5, duration=300):
        self.intensity = intensity
        self.duration = duration
        
    def update(self, dt):
        if self.duration > 0:
            self.duration -= dt
            if self.duration <= 0:
                self.intensity = 0
                
    def get_offset(self):
        if self.duration <= 0:
            return (0, 0)
        
        dx = random.randint(-self.intensity, self.intensity)
        dy = random.randint(-self.intensity, self.intensity)
        return (dx, dy)

def main_menu():
    # Create background texture
    background = create_stone_texture(WIDTH, HEIGHT, ((30, 30, 30), (50, 50, 50)))
    
    # Create torches
    torches = [
        Torch(100, 100),
        Torch(WIDTH - 100 - 16, 100),
        Torch(100, HEIGHT - 150),
        Torch(WIDTH - 100 - 16, HEIGHT - 150)
    ]
    
    # Create water puddles
    puddles = [
        WaterPuddle(200, HEIGHT - 80, 60, 30),
        WaterPuddle(WIDTH - 250, HEIGHT - 100, 80, 40)
    ]
    
    # Create chains
    chains = [
        Chain(150, 0, 8),
        Chain(WIDTH - 150, 0, 10),
        Chain(WIDTH//2 - 100, 0, 6),
        Chain(WIDTH//2 + 100, 0, 7)
    ]
    
    # Create buttons
    button_width, button_height = 200, 50
    buttons = [
        PixelButton(WIDTH//2 - button_width//2, 300, button_width, button_height, 
                  "START", lambda: print("Start button clicked")),
        PixelButton(WIDTH//2 - button_width//2, 370, button_width, button_height, 
                  "SHOP", lambda: print("Shop button clicked")),
        PixelButton(WIDTH//2 - button_width//2, 440, button_width, button_height, 
                  "LOAD", lambda: print("Load button clicked"))
    ]
    
    # Create floating skulls
    skulls = [FloatingSkull() for _ in range(5)]
    
    # Blood drips
    blood_drips = [BloodDrip(random.randint(0, WIDTH)) for _ in range(8)]
    
    # Rats
    rats = []
    rat_spawn_timer = 0
    
    # Fog effect
    fog = FogEffect()
    
    # Screen shake
    screen_shake = ScreenShake()
    
    # Title text variables
    title_y = 150
    title_offset = 0
    title_dir = 1
    
    # Occasional ambient events
    ambient_timer = 0
    
    # Main loop
    running = True
    last_time = pygame.time.get_ticks()
    while running:
        # Calculate delta time
        current_time = pygame.time.get_ticks()
        dt = current_time - last_time
        last_time = current_time
        
        # Handle events
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        
        # Update torches
        for torch in torches:
            torch.update(dt)
            
        # Update puddles
        for puddle in puddles:
            puddle.update(dt)
            
        # Update chains
        for chain in chains:
            chain.update(dt)
            
        # Update buttons
        for button in buttons:
            if button.update(mouse_pos, mouse_clicked) and button.hovered:
                # Trigger screen shake when hovering over buttons
                screen_shake.start(2, 100)
            
        # Update floating skulls
        for skull in skulls:
            skull.update()
            
        # Update blood drips
        for drip in blood_drips:
            drip.update(dt)
                
        # Update rats
        rat_spawn_timer += dt
        if rat_spawn_timer > 5000:  # Spawn a new rat every 5 seconds
            rat_spawn_timer = 0
            if len(rats) < 3 and random.random() < 0.7:
                rats.append(Rat())
                
        for rat in rats[:]:
            rat.update(dt)
            if not rat.active:
                rats.remove(rat)
                
        # Update fog
        fog.update()
        
        # Update screen shake
        screen_shake.update(dt)
        
        # Update title animation
        title_offset += 0.05 * title_dir
        if title_offset > 2:
            title_dir = -1
        elif title_offset < -2:
            title_dir = 1
            
        # Ambient events
        ambient_timer += dt
        if ambient_timer > 10000:  # Every 10 seconds
            ambient_timer = 0
            if random.random() < 0.5:
                # Strong screen shake
                screen_shake.start(8, 500)
                
                # Add a new skull
                skulls.append(FloatingSkull())
        
        # Get screen shake offset
        shake_offset = screen_shake.get_offset()
        
        # Draw
        screen.blit(background, shake_offset)
        
        # Draw puddles
        for puddle in puddles:
            puddle.draw(screen)
        
        # Draw blood drips
        for drip in blood_drips:
            drip.draw(screen)
        
        # Draw floating skulls
        for skull in skulls:
            skull.draw(screen)
        
        # Draw rats
        for rat in rats:
            rat.draw(screen)
        
        # Draw chains
        for chain in chains:
            chain.draw(screen)
        
        # Draw torches
        for torch in torches:
            torch.draw(screen)
        
        # Draw fog
        fog.draw(screen)
        
        # Draw title with shadow and slight movement
        title_text = title_font.render("DUNGEON DEPTHS", True, BLOOD_RED)
        shadow_text = title_font.render("DUNGEON DEPTHS", True, BLACK)
        
        # Draw shadow
        shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 4 + shake_offset[0], 
                                                 title_y + 4 + title_offset + shake_offset[1]))
        screen.blit(shadow_text, shadow_rect)
        
        # Draw main text
        title_rect = title_text.get_rect(center=(WIDTH//2 + shake_offset[0], 
                                               title_y + title_offset + shake_offset[1]))
        screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = info_font.render("NEW GAME", True, LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2 + shake_offset[0], 
                                                     220 + shake_offset[1]))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw level text
        level_text = info_font.render("HIGHEST LEVEL: 7", True, TORCH_YELLOW)
        level_rect = level_text.get_rect(center=(WIDTH//2 + shake_offset[0], 
                                               250 + shake_offset[1]))
        screen.blit(level_text, level_rect)
        
        # Draw buttons
        for button in buttons:
            button.draw(screen)
        
        # Draw version info
        version_text = info_font.render("v1.0.0", True, GRAY)
        version_rect = version_text.get_rect(bottomright=(WIDTH-20 + shake_offset[0], 
                                                        HEIGHT-20 + shake_offset[1]))
        screen.blit(version_text, version_rect)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()