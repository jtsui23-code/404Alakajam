import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Ignore lines above ^^^^

"""
from scripts.UI.main_menu import MainMenu
import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DUNGEON DEPTHS")

# Game state
current_screen = "main_menu"  # Could be "main_menu", "game", "settings", etc.

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Example of switching screens
                if current_screen == "main_menu":
                    # Stop the main menu before switching to another screen
                    MainMenu.stop()
                    current_screen = "game"
                    print("Switched to game screen")
                else:
                    current_screen = "main_menu"
                    print("Switched to main menu")
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Render the current screen
    if current_screen == "main_menu":
        MainMenu.render(screen)
    elif current_screen == "game":
        # This would be your game rendering code
        font = pygame.font.Font(None, 36)
        text = font.render("Game Screen (Press SPACE to return to menu)", True, (255, 255, 255))
        screen.blit(text, (50, HEIGHT // 2))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Make sure to stop the main menu before quitting
MainMenu.stop()

# Clean up
pygame.quit()
sys.exit()