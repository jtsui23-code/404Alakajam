import pygame
from scripts.UI.battleui import BattleScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("RPG Battle")
    clock = pygame.time.Clock()
    
    # Initialize battle screen (now static)
    BattleScreen.init(screen)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to battle UI
            BattleScreen.handle_events(event)
        
        # Clear screen
        screen.fill(BattleScreen.colors['background'])
        
        # Draw battle UI
        BattleScreen.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()