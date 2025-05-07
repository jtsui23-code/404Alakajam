import pygame
import sys
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Medieval Dungeon Character Select")

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (20, 20, 20)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (150, 30, 30)
DARK_RED = (100, 20, 20)
BROWN = (139, 69, 19)
DARK_BROWN = (80, 40, 10)
GOLD = (212, 175, 55)
DARK_GOLD = (160, 120, 40)
PURPLE = (128, 0, 128)
BLUE = (30, 30, 150)
GREEN = (30, 150, 30)

# Font
pixel_font = pygame.font.SysFont("monospace", 20)
title_font = pygame.font.SysFont("monospace", 40)
title_font.set_bold(True)

# Character class data
#Knight, Wizzard, Thief, Goblin, Rat
character_classes = [
    {
        "name": "KNIGHT",
        "color": BLUE,
        "highlight": (100, 100, 255),
        "stats": {"STR": 8, "DEX": 5, "INT": 3, "VIT": 9},
        "weapon": "Longsword"
    },
    {
        "name": "Wizzard",
        "color": PURPLE,
        "highlight": (200, 100, 200),
        "stats": {"STR": 3, "DEX": 4, "INT": 10, "VIT": 4},
        "weapon": "Staff"
    },
    {
        "name": "Thief",
        "color": GREEN,
        "highlight": (100, 200, 100),
        "stats": {"STR": 5, "DEX": 10, "INT": 6, "VIT": 4},
        "weapon": "Daggers"
    },
    {
        "name": "Goblin",
        "color": RED,
        "highlight": (255, 100, 100),
        "stats": {"STR": 10, "DEX": 6, "INT": 2, "VIT": 7},
        "weapon": "Battle Axe"
    }, 
    {
        "name": "Rat",
        "color": RED,
        "highlight": (255, 100, 100),
        "stats": {"STR": 10, "DEX": 6, "INT": 2, "VIT": 7},
        "weapon": "Battle Axe"
    }, 
]

# Game state
selected_character = 0
animation_timer = 0
torch_flicker = 0
show_description = False

# Draw pixelated character
def draw_character(x, y, color, selected=False):
    # Base character size
    size = 80
    
    # Draw character body (pixelated style)
    body_color = color if not selected else character_classes[selected_character]["highlight"]
    
    # Head
    pygame.draw.rect(screen, body_color, (x, y, size, size))
    
    # Eyes (creepy for fear theme)
    eye_color = RED if selected else WHITE
    pygame.draw.rect(screen, BLACK, (x + size//4, y + size//3, size//6, size//6))
    pygame.draw.rect(screen, BLACK, (x + size - size//4 - size//6, y + size//3, size//6, size//6))
    pygame.draw.rect(screen, eye_color, (x + size//4 + 1, y + size//3 + 1, size//6 - 2, size//6 - 2))
    pygame.draw.rect(screen, eye_color, (x + size - size//4 - size//6 + 1, y + size//3 + 1, size//6 - 2, size//6 - 2))
    
    # Mouth (creepy smile)
    mouth_y = y + size//2 + size//8
    pygame.draw.rect(screen, BLACK, (x + size//4, mouth_y, size//2, size//8))
    
    # Weapon based on character class
    if character_classes[selected_character]["name"] == "KNIGHT":
        # Sword
        pygame.draw.rect(screen, LIGHT_GRAY, (x + size + 5, y + size//2, 8, size//2 + 20))
        pygame.draw.rect(screen, GOLD, (x + size + 5 - 10, y + size//2, 28, 8))
    elif character_classes[selected_character]["name"] == "MAGE":
        # Staff
        pygame.draw.rect(screen, BROWN, (x + size + 5, y, 6, size + 20))
        pygame.draw.rect(screen, PURPLE, (x + size + 5 - 5, y - 10, 16, 16))
    elif character_classes[selected_character]["name"] == "ROGUE":
        # Daggers
        pygame.draw.rect(screen, LIGHT_GRAY, (x + size + 5, y + size//2, 5, size//3))
        pygame.draw.rect(screen, LIGHT_GRAY, (x + size + 15, y + size//2 + 10, 5, size//3))
    elif character_classes[selected_character]["name"] == "BERSERKER":
        # Axe
        pygame.draw.rect(screen, BROWN, (x + size + 5, y + size//3, 6, size//2))
        pygame.draw.rect(screen, LIGHT_GRAY, (x + size + 5 - 15, y + size//3, 30, 20))
    
    # Selection indicator
    if selected:
        border_thickness = 4
        pygame.draw.rect(screen, GOLD, (x - border_thickness, y - border_thickness, 
                                        size + 2*border_thickness, size + 2*border_thickness), border_thickness)

# Draw dungeon background
def draw_background():
    # Dark background
    screen.fill(BLACK)
    
    # Draw stone wall pattern
    stone_size = 40
    for y in range(0, SCREEN_HEIGHT, stone_size):
        offset = stone_size // 2 if (y // stone_size) % 2 == 1 else 0
        for x in range(-offset, SCREEN_WIDTH, stone_size):
            stone_color = (
                DARK_GRAY[0] + pygame.math.Vector2(x, y).length() % 10,
                DARK_GRAY[1] + pygame.math.Vector2(x, y).length() % 10,
                DARK_GRAY[2] + pygame.math.Vector2(x, y).length() % 8
            )
            pygame.draw.rect(screen, stone_color, (x, y, stone_size - 2, stone_size - 2))
    
    # Draw torches with flickering effect
    torch_positions = [(50, 100), (SCREEN_WIDTH - 50, 100), 
                       (50, SCREEN_HEIGHT - 100), (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 100)]
    
    for tx, ty in torch_positions:
        # Torch base
        pygame.draw.rect(screen, DARK_BROWN, (tx - 5, ty, 10, 30))
        
        # Flickering flame
        flicker = math.sin(torch_flicker + tx * 0.1) * 3
        flame_height = 20 + int(flicker)
        flame_width = 14 + int(flicker)
        
        pygame.draw.polygon(screen, RED, [
            (tx, ty),
            (tx - flame_width//2, ty - flame_height//2),
            (tx, ty - flame_height),
            (tx + flame_width//2, ty - flame_height//2)
        ])
        
        # Light effect (simple circle gradient)
        max_radius = 100 + int(flicker * 5)
        for r in range(max_radius, 0, -10):
            alpha = 20 - int(20 * r / max_radius)
            s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 200, 100, alpha), (r, r), r)
            screen.blit(s, (tx - r, ty - r))

# Draw character stats
def draw_stats():
    if show_description:
        # Stats background
        stats_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 180, 300, 150)
        pygame.draw.rect(screen, BLACK, stats_rect)
        pygame.draw.rect(screen, GOLD, stats_rect, 2)
        
        # Character info
        char_data = character_classes[selected_character]
        name_text = title_font.render(char_data["name"], True, char_data["color"])
        screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, SCREEN_HEIGHT - 170))
        
        # Weapon
        weapon_text = pixel_font.render(f"WEAPON: {char_data['weapon']}", True, WHITE)
        screen.blit(weapon_text, (SCREEN_WIDTH//2 - weapon_text.get_width()//2, SCREEN_HEIGHT - 130))
        
        # Stats
        y_pos = SCREEN_HEIGHT - 100
        for stat, value in char_data["stats"].items():
            stat_text = pixel_font.render(f"{stat}: {value}", True, WHITE)
            screen.blit(stat_text, (SCREEN_WIDTH//2 - 100 + (list(char_data["stats"].keys()).index(stat) * 50), y_pos))
        
        # Instruction
        select_text = pixel_font.render("PRESS ENTER TO SELECT", True, GOLD)
        screen.blit(select_text, (SCREEN_WIDTH//2 - select_text.get_width()//2, SCREEN_HEIGHT - 40))

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                selected_character = (selected_character - 1) % len(character_classes)
            elif event.key == K_RIGHT:
                selected_character = (selected_character + 1) % len(character_classes)
            elif event.key == K_SPACE or event.key == K_RETURN:
                # Here you would transition to the game with the selected character
                print(f"Selected character: {character_classes[selected_character]['name']}")
            elif event.key == K_d:
                show_description = not show_description
    
    # Update animations
    animation_timer += 0.05
    torch_flicker += 0.1
    
    # Draw everything
    draw_background()
    
    # Draw title
    title = title_font.render("CHOOSE YOUR CHAMPION", True, GOLD)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
    
    # Draw subtitle with fear theme
    subtitle = pixel_font.render("(ONLY THE BRAVE SURVIVE THE DUNGEON)", True, RED)
    screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 100))
    
    # Draw character selection
    spacing = 160
    start_x = SCREEN_WIDTH//2 - (spacing * (len(character_classes) - 1))//2
    
    for i, char in enumerate(character_classes):
        x_pos = start_x + i * spacing
        y_pos = SCREEN_HEIGHT//2 - 50
        
        # Character platform (stone)
        platform_width = 100
        platform_height = 20
        pygame.draw.rect(screen, DARK_GRAY, (x_pos - 10, y_pos + 80, platform_width, platform_height))
        
        # Draw character
        draw_character(x_pos, y_pos, char["color"], i == selected_character)
        
        # Draw name
        name_text = pixel_font.render(char["name"], True, WHITE)
        screen.blit(name_text, (x_pos + 40 - name_text.get_width()//2, y_pos + 100))
    
    # Draw stats for selected character
    draw_stats()
    
    # Draw instructions
    instructions = pixel_font.render("ARROW KEYS: NAVIGATE   D: TOGGLE DETAILS", True, WHITE)
    screen.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, SCREEN_HEIGHT - 20))
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()