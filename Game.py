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

        if nextUI == 'levelSelect':
            # By setting initialized to False, we ensure that the .draw() method
            # for DifficultySelector will call .initialize() when this state
            # is first rendered after the switch. .initialize() sets .result = None
            # and initialized = True.
            DifficultySelector.initialized = False


    # Runs the game loop for the entire game.
    def run(self):
        while self.running:

            pygame.display.flip()
            self.clock.tick(60) 
            
            # Checks if a button was clicked within the main menu state for state and screen transition.  
            actionFromUI = None

            # print(f"The current state is ", {self.stateManager.currentState})

            # Handle events
            for event in pygame.event.get():

                # Checks if the user clicked the X on the top right.
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        # If you are in the shop state/screen and click esc key, you return to the main menu.
                        if self.stateManager.currentState == 'shop':
                            self.switchUI('shop', 'main')

                        elif self.stateManager.currentState == 'levelSelect':
                            self.switchUI('levelSelect', 'character')

                        elif self.stateManager.currentState == 'character':
                            self.switchUI('character', 'main')

                  
                    # Level Selection UI cannot handle enter event here because this will cause the 
                    # screen to freeze while the other UI's can.
                    if self.stateManager.currentState != 'levelSelect':
                        if event.key == pygame.K_RETURN:
                            if self.stateManager.currentState == 'character':
                                self.switchUI('character', 'levelSelect')





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

                
                self.handler.render('shop')

            elif self.stateManager.currentState == 'character':

                
                self.handler.render('character')

            elif self.stateManager.currentState =='levelSelect':

                self.handler.render('difficulty')

                # Check if difficulty was selected
                if DifficultySelector.result is not None:

                    print(f"Selected difficulty: {DifficultySelector.result}")

                    self.switchUI('levelSelect', 'roomSelect')

                    DifficultySelector.clear(self.screen)

                    print("It's over")
            

            elif self.stateManager.currentState =='roomSelect':

                self.handler.render('roomSelect')


            
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

