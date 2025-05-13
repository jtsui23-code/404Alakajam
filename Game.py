import pygame
# import sys
# import random
from scripts.UI.UIHandler import UIHandler
from scripts.State import StateManager

class Game:
    def __init__(self):
        pygame.init()

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


            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                

            if StateManager.checkCurrentState('main'):

                self.handler.render('menu') 
                
            elif StateManager.checkCurrentState('shop'):

                self.handler.render('shop')

            elif StateManager.checkCurrentState('character'):
                self.handler.render('character')

            if StateManager.setAction:
                

                if StateManager.setAction == "Start":
                    self.handler.stop('menu')                    
                    StateManager.switchState('character')

            # Updates the display
            pygame.display.flip()
            # Sets FPS to 60
            pygame.time.Clock().tick(60)    

if __name__ == "__main__":
    game = Game()
    game.run()

