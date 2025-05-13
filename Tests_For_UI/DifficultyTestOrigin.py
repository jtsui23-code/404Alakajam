import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Ignore lines above ^^^^

"""

## In your main game file
import pygame
import sys
from scripts.UI.difficulty import DifficultySelector

# Import other screen classes

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("DUNGEON GAME")

# Game state
current_screen = "difficulty"
running = True
clock = pygame.time.Clock()

# Initialize screens
DifficultySelector.initialize(screen)
# Other initializations...

# Main game loop
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))  # Clear screen
    
    # Handle different screens
    if current_screen == "difficulty":
        DifficultySelector.draw(screen)
        if DifficultySelector.update(events):
            result = DifficultySelector.get_result()
            if result:
                difficulty = result
                DifficultySelector.clear(screen)
                current_screen = "character"  # Move to next screen
    
    # elif current_screen == "character":
    #     CharacterSelector.draw(screen)
    #     # Similar logic...
    
    # elif current_screen == "game":
    #     GameScreen.draw(screen)
    #     # Similar logic...
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()