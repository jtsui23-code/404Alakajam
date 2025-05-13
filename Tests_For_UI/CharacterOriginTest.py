import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Ignore lines above ^^^^

"""

import pygame
import sys
from scripts.UI.char_select import Character

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Medieval Dungeon Game")

# Main game loop
clock = pygame.time.Clock()
running = True
selected_character = None
current_screen = "character_select"  # Could be "main_menu", "game", etc.

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Pass events to current screen
        if current_screen == "character_select":
            result = Character.handle_event(event)
            if result == True:
                # Selection changed
                pass
            elif result:  # Character name returned
                selected_character = result
                print(f"Selected character: {selected_character}")
                # Here you would transition to the game with the selected character
                # current_screen = "game"
                # Character.stop()  # Stop the character selection screen
    
    # Clear screen
    screen.fill((0, 0, 0))
    
    # Draw current screen
    if current_screen == "character_select":
        Character.draw(screen)
    # elif current_screen == "game":
    #     Game.draw(screen)
    # elif current_screen == "main_menu":
    #     MainMenu.draw(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

# Clean up before exiting
Character.stop()
pygame.quit()
sys.exit()