import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Jack, if you are reading this. The only important part is 
Line 14, 29, and 38
That shows you how to use the UI module

"""
from scripts.UI.char_select import CharacterSelect
import pygame
import sys
# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Medieval Dungeon Game")

# Create character selection screen
character_select = CharacterSelect()

# Main game loop
clock = pygame.time.Clock()
running = True
selected_character = None

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Pass events to character selection screen
        result = character_select.handle_event(event)
        if result == True:
            # Selection changed
            pass
        elif result:  # Character name returned
            selected_character = result
            print(f"Selected character: {selected_character}")
            # Here you would transition to the game with the selected character
    
    # Render character selection screen
    character_select.render(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()