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


    # Runs the game loop for the entire game.
    def run(self):
        while self.running: 
            
            # Checks if a button was clicked within the main menu state for state and screen transition.  
            actionFromUI = None

            # Handle events
            for event in pygame.event.get():

                # Checks if the user clicked the X on the top right.
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handles events within the different States other than main. This is different from 
                # actionFromUI because this handle event section does not do anything regarding state transition 
                # just the events self contained in the current State of the game.
                if not self.stateManager.currentState == 'main':
                    self.handler.handleEvent(self.stateManager.currentState, event)
            
            # Renders the UI of the current state only. If there was no distinction, all of the 
            # UI's would be rendered at once instead of the intended UI of the current state/screen.
            if self.stateManager.currentState == 'main':
                
                # The render method from the UI Hanlder class returns a string if any of the particular buttons where 
                # clicked on the main menu. So this self.handler.render('menu')  will return a string "Start Button"
                # if the start button was clicked which needs to be stored and checked to change the state and screen of the 
                # main menu to the next screen after clicking the start button which would be the character select.
                actionFromUI = self.handler.render('menu') 
                
            elif self.stateManager.currentState == 'shop':

                # self.handler.render('shop') will return a string "Shop Button" if the shop button on the main menu was 
                # clicked. This is needs to be stored and checked for the state/screen transition to the Shop state/screen.
                actionFromUI = self.handler.render('shop')

            elif self.stateManager.currentState == 'character':

                
                actionFromUI = self.handler.render('character')

            
            # This checks the value of actionFromUI to see if there is need to state transition.
            if actionFromUI:
                print(f"value of actionFromUI is ", {actionFromUI})

                # If the Start Button was clicked, go from the main menu to the character select state/screen.
                if actionFromUI == "Start Button":
                    self.handler.stop('menu')                    
                    self.stateManager.switchState('character')

                # If the Shop Button was clicked, go from the main menu to the shop state/screen.
                elif actionFromUI == "Shop Button":
                    self.handler.stop('menu')
                    self.stateManager.switchState('shop')


                # elif actionFromUI == "Load Button":
                #     self.handler.stop('menu')
                #     self.stateManager.switchState('character')




            # Updates the display
            pygame.display.flip()
            # Sets FPS to 60
            pygame.time.Clock().tick(60)    

if __name__ == "__main__":
    game = Game()
    game.run()

