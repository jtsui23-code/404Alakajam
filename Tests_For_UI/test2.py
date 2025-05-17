import pygame
import sys
from scripts.UI.level import LevelSelectionScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Level Selection")
    clock = pygame.time.Clock()
    
    # Load font
    try:
        font = pygame.font.Font(None, 36)
    except:
        font = pygame.font.SysFont('Arial', 36)
    
    # Initialize level selection (generates grids once)
    LevelSelectionScreen.init(font)
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle level selection
            if LevelSelectionScreen.handle_event(event):
                selected_level = LevelSelectionScreen.get_selected_level()
                print(f"Starting Level {selected_level}")
                # Add your level loading logic here
                # For demo, we'll just reset after 2 seconds
                LevelSelectionScreen.reset_selection()
        
        # Drawing
        screen.fill((0, 0, 0))  # Clear screen
        
        # Draw level selection screen
        LevelSelectionScreen.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()