import pygame
# import sys
# import random
from scripts.UI.UIHandler import UIHandler
from scripts.State import StateManager
from scripts.UI.difficulty import DifficultySelector
class Game:
    def __init__(self):
        pygame.init()
        self.stateManager = StateManager()
        # Sets the dimensions of the Pygame window 1280x720
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Sets the caption of the Pygame window.
        pygame.display.set_caption("DUNGEON DEPTHS")

        

        # Flag for the while run loop of the game. 
        self.running = True
        # Need Pygame clock for the frame work of the game which will be 60 fps
        self.clock = pygame.time.Clock()
        
        # Creating instance of UI Handler for all of the UI's in the game.
        self.handler = UIHandler(self.screen)

    def switchUI(self, currentUI, nextUI):
        self.handler.stop(currentUI)
        self.stateManager.switchState(nextUI)


    # Runs the game loop for the entire game.
    def run(self):
        while self.running:

            actionFromUI = None
            
            # Handle events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.running = False

                elif event.type == pygame.KEYDOWN:


                    if event.key == pygame.K_ESCAPE:

                        # Handle Escape for all states
                        if self.stateManager.currentState == 'shop':

                            self.switchUI('shop', 'main')

                        elif self.stateManager.currentState == 'levelSelect':

                            self.switchUI('levelSelect', 'character')
                        elif self.stateManager.currentState == 'character':

                            self.switchUI('character', 'main')

                    # Let DifficultySelector handle Enter in levelSelect state
                    
                    if self.stateManager.currentState != 'levelSelect':
                        if event.key == pygame.K_RETURN:
                            if self.stateManager.currentState == 'character':
                                self.switchUI('character', 'levelSelect')


                                

                # Pass events to current UI
                if not self.stateManager.currentState == 'main':
                    self.handler.handleEvent(self.stateManager.currentState, event)

            # Render current UI
            if self.stateManager.currentState == 'main':
                actionFromUI = self.handler.render('menu')

            elif self.stateManager.currentState == 'shop':
                self.handler.render('shop')

            elif self.stateManager.currentState == 'character':
                self.handler.render('character')

            elif self.stateManager.currentState == 'levelSelect':
                self.handler.render('difficulty')

                # Check if difficulty was selected
                if DifficultySelector.result is not None:
                    print(f"Selected difficulty: {DifficultySelector.result}")
                    self.switchUI('levelSelect', 'roomSelect')
                    DifficultySelector.clear(self.screen)
                    print("It's over")

            elif self.stateManager.currentState == 'roomSelect':
                actionFromUI = self.handler.render('roomSelect')

            # Handle UI actions
            if actionFromUI:
                if actionFromUI == "Start Button":
                    self.handler.stop('menu')
                    self.stateManager.switchState('character')
                elif actionFromUI == "Shop Button":
                    self.handler.stop('menu')
                    self.stateManager.switchState('shop')

            # Updates the display
            pygame.display.flip()
            # Sets FPS to 60
            pygame.time.Clock().tick(60)    

if __name__ == "__main__":
    game = Game()
    game.run()

