import pygame
from scripts.Battle import BattleData


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    battle = BattleData(screen)
    pygame.display.set_caption("RPG Battle")
    clock = pygame.time.Clock()
    
    # Initialize battle screen (now static)    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to battle UI
            battle.screen.handle_events(event)
        
        # Clear screen
        screen.fill(battle.screen.colors['background'])

        outcome = battle.checkWin()
        
        if outcome == 'enemy won':
            print("Game Over! You lost!")
            running = False
        elif outcome == 'player won':
            print("Victory! Enemy defeated!")
            running = False
        
        
        # Draw battle UI
        battle.screen.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()