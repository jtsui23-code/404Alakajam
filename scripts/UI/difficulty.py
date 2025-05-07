import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DUNGEON CRAWLER")

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (20, 20, 20)
GRAY = (40, 40, 40)
LIGHT_GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
RED = (170, 30, 30)
DARK_RED = (100, 20, 20)
GOLD = (180, 150, 30)

# Difficulty options
difficulties = [
    {"name": "EASY", "desc": "More health, weaker enemies"},
    {"name": "NORMAL", "desc": "Standard challenge"},
    {"name": "HARD", "desc": "Less health, stronger enemies"},
    {"name": "NIGHTMARE", "desc": "Death awaits..."}
]

selected = 0
clock = pygame.time.Clock()
frame_count = 0

# Create a pixelated font
def pixel_font(size):
    return pygame.font.SysFont("courier", size, bold=True)

# Draw pixelated text
def draw_text(text, font, color, x, y, shadow=True):
    if shadow:
        text_surface = font.render(text, False, BLACK)
        screen.blit(text_surface, (x+2, y+2))
    text_surface = font.render(text, False, color)
    screen.blit(text_surface, (x, y))

# Draw a pixelated rectangle
def draw_pixel_rect(x, y, width, height, color, border_color=None):
    pygame.draw.rect(screen, color, (x, y, width, height))
    if border_color:
        pygame.draw.rect(screen, border_color, (x, y, width, height), 1)

# Draw a simple pixelated torch
def draw_torch(x, y, frame):
    # Handle
    draw_pixel_rect(x, y+8, 4, 12, (80, 50, 20))
    
    # Flame (animated)
    flame_height = 6 + math.sin(frame * 0.2) * 2
    flame_width = 6 + math.sin(frame * 0.3) * 1
    
    # Outer flame
    draw_pixel_rect(x-1, y-int(flame_height), 6, 8, (200, 50, 10))
    
    # Inner flame
    draw_pixel_rect(x, y-int(flame_height)+2, 4, 5, (250, 180, 10))

# Draw the stone wall background
def draw_background():
    # Fill with black
    screen.fill(BLACK)
    
    # Draw stone bricks
    brick_size = 32
    for y in range(0, HEIGHT, brick_size):
        offset = brick_size // 2 if (y // brick_size) % 2 else 0
        for x in range(-offset, WIDTH, brick_size):
            # Random variation in brick color
            color_var = random.randint(-5, 5)
            brick_color = (GRAY[0] + color_var, GRAY[0] + color_var, GRAY[0] + color_var)
            
            # Draw brick
            draw_pixel_rect(x, y, brick_size-1, brick_size-1, brick_color, DARK_GRAY)
            
            # Occasionally add cracks or details
            if random.random() < 0.1:
                crack_x = x + random.randint(5, brick_size-10)
                crack_y = y + random.randint(5, brick_size-10)
                crack_length = random.randint(3, 8)
                pygame.draw.line(screen, DARK_GRAY, 
                                (crack_x, crack_y), 
                                (crack_x + random.randint(-crack_length, crack_length), 
                                 crack_y + random.randint(-crack_length, crack_length)), 
                                1)

# Draw a difficulty option
def draw_option(index, name, desc, y_pos, is_selected):
    # Option background
    option_width = 300
    option_height = 50
    option_x = (WIDTH - option_width) // 2
    
    # Determine colors based on selection
    if is_selected:
        # Pulsing effect for selected option
        pulse = math.sin(frame_count * 0.1) * 20
        bg_color = (min(255, RED[0] + pulse), min(255, RED[1] + pulse), min(255, RED[2] + pulse))
        text_color = WHITE
    else:
        bg_color = DARK_GRAY
        text_color = LIGHT_GRAY
    
    # Draw option box
    draw_pixel_rect(option_x, y_pos, option_width, option_height, bg_color, BLACK)
    
    # Draw option text
    name_font = pixel_font(24)
    desc_font = pixel_font(14)
    
    # Draw name
    draw_text(name, name_font, text_color, option_x + 20, y_pos + 10)
    
    # Draw description
    draw_text(desc, desc_font, text_color, option_x + 20, y_pos + 30, shadow=False)
    
    # Draw selection indicator
    if is_selected:
        draw_text(">", name_font, GOLD, option_x - 20, y_pos + 10)
        draw_text("<", name_font, GOLD, option_x + option_width + 5, y_pos + 10)

# Main game loop
def main():
    global selected, frame_count
    running = True
    
    while running:
        frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                    print("* Chain rattles *")
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                    print("* Chain rattles *")
                elif event.key == pygame.K_RETURN:
                    difficulty = difficulties[selected]["name"]
                    print(f"\nSelected difficulty: {difficulty}")
                    print("* Door creaks open *")
                    return difficulty
                    
            # Mouse handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                option_width = 300
                option_height = 50
                option_x = (WIDTH - option_width) // 2
                
                for i, diff in enumerate(difficulties):
                    y_pos = 180 + i * 60
                    option_rect = pygame.Rect(option_x, y_pos, option_width, option_height)
                    if option_rect.collidepoint(mouse_pos):
                        difficulty = difficulties[i]["name"]
                        print(f"\nSelected difficulty: {difficulty}")
                        print("* Door creaks open *")
                        return difficulty
        
        # Draw background
        draw_background()
        
        # Draw title with slight flicker effect
        title_font = pixel_font(48)
        subtitle_font = pixel_font(20)
        
        # Random flicker for title
        flicker = random.randint(0, 20) > 18
        title_color = LIGHT_GRAY if flicker else RED
        
        draw_text("DUNGEON CRAWLER", title_font, title_color, 120, 80)
        draw_text("SELECT DIFFICULTY", subtitle_font, GOLD, 220, 140)
        
        # Draw difficulty options
        for i, diff in enumerate(difficulties):
            y_pos = 180 + i * 60
            draw_option(i, diff["name"], diff["desc"], y_pos, i == selected)
        
        # Draw torches
        draw_torch(100, 100, frame_count)
        draw_torch(540, 100, frame_count + 10)
        draw_torch(100, 380, frame_count + 5)
        draw_torch(540, 380, frame_count + 15)
        
        # Draw instructions
        instruction_font = pixel_font(16)
        draw_text("UP/DOWN: Select   ENTER: Confirm", instruction_font, LIGHT_GRAY, 160, 430)
        
        # Add vignette effect (darkened corners)
        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(10):
            alpha = i * 10
            pygame.draw.rect(vignette, (0, 0, 0, alpha), 
                           ((i*10, i*10), (WIDTH-i*20, HEIGHT-i*20)), 1)
        screen.blit(vignette, (0, 0))
        
        # Update display
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    selected_difficulty = main()
    pygame.quit()