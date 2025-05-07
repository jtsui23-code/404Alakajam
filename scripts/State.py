import pygame
import sys
import UIButton as Button

class State:
    def __init__(self, stateName=''):
        self.currentState = stateName
        self.uiElements = {}

    # Assumes that the render method in the UI class will require a 
    # Pygame screen as an argument.
    def render(self, screen):
        for element in self.uiElements:
            element.render(screen)

    def update(self, screen):
        self.render(screen)
    
    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handleMosClick(event.pos)

    
    # Changes the mouse cursor when hovering over a button
    def hoverEffect(self):
        pass

    def handleMosClick(self, mosPos):

        # Checks if a mouse click has occured on a button UI.
        for key, element in self.uiElements.items():
            if isinstance(element, Button) and element.rect.collidepoint(mosPos):
                self.buttonClicked(key)



    def enterState(self):
        pass
    
    # Performs the particular action that the specific button will do once 
    # clicked upon by the mouse left click.
    def buttonClicked(self, buttonKey):
        pass

    def exitState(self):
        pass

    def switchState(self):
        pass