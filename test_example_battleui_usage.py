import pygame
from scripts.UI.battleui_dynamic import BattleScreen

def open_inventory():
    print("Open")

def attempt_escape():
    print("Escape")
    
# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
battle_screen = BattleScreen(screen)

# Configure callbacks
def custom_attack():
    battle_screen.remove_hearts(enemy=1)
    print("Enemy hit!")

battle_screen.set_callback('attack', custom_attack)
battle_screen.set_callback('bag', open_inventory)  # Your function
battle_screen.set_callback('run', attempt_escape)  # Your function

# In game loop
running = True
while running:
    for event in pygame.event.get():
        battle_screen.handle_events(event)
    
    battle_screen.draw()
    pygame.display.flip()