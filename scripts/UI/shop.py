import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Medieval Dungeon Shop")

# Colors
DARK_BROWN = (54, 36, 24)
LIGHT_BROWN = (101, 67, 33)
GRAY = (80, 80, 80)
DARK_RED = (120, 20, 20)
GOLD = (212, 175, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TORCH_YELLOW = (230, 180, 50)

# Fonts
pixel_font = pygame.font.SysFont("monospace", 20)
title_font = pygame.font.SysFont("monospace", 32)
title_font.set_bold(True)

# Shop items
items = [
    {"name": "Rusty Sword", "price": 15, "description": "Barely sharp, but better than nothing."},
    {"name": "Leather Armor", "price": 25, "description": "Offers minimal protection from the horrors."},
    {"name": "Health Potion", "price": 10, "description": "Heals wounds, tastes terrible."},
    {"name": "Torch", "price": 5, "description": "Keeps the darkness at bay... for a while."},
    {"name": "Silver Dagger", "price": 35, "description": "Effective against the undead."},
    {"name": "Scroll of Escape", "price": 50, "description": "Your last hope when all else fails."}
]

# Player info
player_gold = 100
player_inventory = []
selected_item = 0

# Torch flicker effect
torch_intensity = 100
torch_direction = -1

# Create pixelated item icons (simulated)
def create_pixelated_icon(color):
    icon = pygame.Surface((48, 48))
    icon.fill(BLACK)
    
    # Create a pixelated pattern
    pixel_size = 6
    for y in range(0, 48, pixel_size):
        for x in range(0, 48, pixel_size):
            if random.random() > 0.5:
                pygame.draw.rect(icon, color, (x, y, pixel_size, pixel_size))
            else:
                pygame.draw.rect(icon, (color[0]//2, color[1]//2, color[2]//2), (x, y, pixel_size, pixel_size))
    
    # Add border
    pygame.draw.rect(icon, LIGHT_BROWN, (0, 0, 48, 48), 2)
    return icon

# Generate item icons
item_icons = [
    create_pixelated_icon(DARK_RED),  # Rusty Sword
    create_pixelated_icon(LIGHT_BROWN),  # Leather Armor
    create_pixelated_icon((200, 0, 0)),  # Health Potion
    create_pixelated_icon(TORCH_YELLOW),  # Torch
    create_pixelated_icon((192, 192, 192)),  # Silver Dagger
    create_pixelated_icon((100, 100, 255))  # Scroll of Escape
]

# Shopkeeper dialogue
shopkeeper_dialogues = [
    "Welcome to my humble shop, traveler...",
    "Don't touch anything unless you're buying it!",
    "The dungeon grows more dangerous by the day...",
    "I don't offer refunds. Ever.",
    "Many enter the dungeon, few return...",
    "These items might save your life, if you're lucky."
]
current_dialogue = random.choice(shopkeeper_dialogues)
dialogue_timer = 0

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(items)
                current_dialogue = f"Ah, the {items[selected_item]['name']}. {items[selected_item]['description']}"
                dialogue_timer = 0
            elif event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(items)
                current_dialogue = f"Ah, the {items[selected_item]['name']}. {items[selected_item]['description']}"
                dialogue_timer = 0
            elif event.key == pygame.K_RETURN:
                # Buy item
                if player_gold >= items[selected_item]['price']:
                    player_gold -= items[selected_item]['price']
                    player_inventory.append(items[selected_item]['name'])
                    current_dialogue = f"The {items[selected_item]['name']} is yours. Use it wisely..."
                else:
                    current_dialogue = "You don't have enough gold, beggar!"
                dialogue_timer = 0
    
    # Update torch flicker
    torch_intensity += torch_direction * random.uniform(0.5, 1.5)
    if torch_intensity < 70:
        torch_intensity = 70
        torch_direction = 1
    elif torch_intensity > 100:
        torch_intensity = 100
        torch_direction = -1
    
    # Update dialogue
    dialogue_timer += 1
    if dialogue_timer > 300:  # Change dialogue every ~5 seconds
        dialogue_timer = 0
        current_dialogue = random.choice(shopkeeper_dialogues)
    
    # Draw background
    screen.fill(DARK_BROWN)
    
    # Draw shop frame (pixelated style)
    pygame.draw.rect(screen, BLACK, (50, 50, WIDTH-100, HEIGHT-100))
    pygame.draw.rect(screen, LIGHT_BROWN, (50, 50, WIDTH-100, HEIGHT-100), 4)
    
    # Draw flickering torch effect in corners
    torch_color = (min(255, int(TORCH_YELLOW[0] * torch_intensity/100)),
                  min(255, int(TORCH_YELLOW[1] * torch_intensity/100)),
                  min(255, int(TORCH_YELLOW[2] * torch_intensity/100)))
    
    pygame.draw.circle(screen, torch_color, (70, 70), 15)
    pygame.draw.circle(screen, torch_color, (WIDTH-70, 70), 15)
    
    # Draw shop title
    title = title_font.render("DUNGEON MERCHANT", True, GOLD)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 70))
    
    # Draw shopkeeper dialogue
    dialogue_box = pygame.Rect(100, 120, WIDTH-200, 60)
    pygame.draw.rect(screen, BLACK, dialogue_box)
    pygame.draw.rect(screen, LIGHT_BROWN, dialogue_box, 2)
    
    dialogue_text = pixel_font.render(current_dialogue, True, WHITE)
    screen.blit(dialogue_text, (dialogue_box.x + 10, dialogue_box.y + 20))
    
    # Draw items
    item_start_y = 200
    for i, item in enumerate(items):
        item_rect = pygame.Rect(100, item_start_y + i*60, WIDTH-200, 50)
        
        # Highlight selected item
        if i == selected_item:
            pygame.draw.rect(screen, DARK_RED, item_rect)
            pygame.draw.rect(screen, GOLD, item_rect, 2)
        else:
            pygame.draw.rect(screen, BLACK, item_rect)
            pygame.draw.rect(screen, LIGHT_BROWN, item_rect, 1)
        
        # Draw item icon
        screen.blit(item_icons[i], (item_rect.x + 10, item_rect.y + 1))
        
        # Draw item name and price
        name_text = pixel_font.render(item['name'], True, WHITE)
        price_text = pixel_font.render(f"{item['price']} gold", True, GOLD)
        
        screen.blit(name_text, (item_rect.x + 70, item_rect.y + 15))
        screen.blit(price_text, (item_rect.right - price_text.get_width() - 20, item_rect.y + 15))
    
    # Draw player info
    pygame.draw.rect(screen, BLACK, (100, HEIGHT-100, WIDTH-200, 50))
    pygame.draw.rect(screen, LIGHT_BROWN, (100, HEIGHT-100, WIDTH-200, 50), 2)
    
    gold_text = pixel_font.render(f"Gold: {player_gold}", True, GOLD)
    inventory_text = pixel_font.render(f"Inventory: {', '.join(player_inventory) if player_inventory else 'Empty'}", True, WHITE)
    
    screen.blit(gold_text, (120, HEIGHT-85))
    screen.blit(inventory_text, (250, HEIGHT-85))
    
    # Draw controls hint
    controls_text = pixel_font.render("UP/DOWN: Select   ENTER: Buy   ESC: Exit", True, GRAY)
    screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT-30))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()