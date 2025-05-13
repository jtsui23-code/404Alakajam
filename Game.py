import pygame
# import sys
# import random
from scripts.UI.UIHandler import UIHandler
from scripts.State import StateManager

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


    def run(self):
        while self.running: 

            actionFromUI = None
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                

            if self.stateManager.currentState == 'main':

                actionFromUI = self.handler.render('menu') 
                
            elif self.stateManager.currentState == 'shop':

                actionFromUI = self.handler.render('shop')

            elif self.stateManager.currentState == 'character':
                actionFromUI = self.handler.render('character')

            

            if actionFromUI:
                print(f"value of actionFromUI is ", {actionFromUI})


                if actionFromUI == "Start Button":
                    self.handler.stop('menu')                    
                    self.stateManager.switchState('character')

                elif actionFromUI == "Shop Button":
                    self.handler.stop('menu')
                    self.stateManager.switchState('shop')


                elif actionFromUI == "Load Button":
                    self.handler.stop('menu')
                    self.stateManager.switchState('character')




            # Updates the display
            pygame.display.flip()
            # Sets FPS to 60
            pygame.time.Clock().tick(60)    

if __name__ == "__main__":
    game = Game()
    game.run()

