import pygame
import sys
import UIButton as Button
import Sound as Sound

class State:
    def __init__(self):
        self.isCurrentState = False
        self.uiElements = {}

    # Assumes that the render method in the UI class will require a 
    # Pygame screen as an argument.
    def render(self, screen):
        for element in self.uiElements:
            element.render(screen)

    def update(self, screen):
        self.render(screen)
    
    def checkCurrentState(self):
        return self.isCurrentState
    
    def changeCurrentState(self, input=False):
        self.isCurrentState = input
    
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

    # Performs the particular action that the specific button will do once 
    # clicked upon by the mouse left click.
    def buttonClicked(self, buttonKey):
        pass



    def startMusic(self):
        pass
    
   

class MainMenuState(State):

    def __init__(self):
        super().__init__()

    def startMusic(self):
        Sound.playTheme(songName='TitleTheme', loop=True)

    
    

class ShopState(State):
    
    def __init__(self):
        super().__init__()

    def startMusic(self):
        Sound.playTheme(songName='ShopTheme', loop=True)

class CharacterSelectState(State):
    
    def __init__(self):
        super().__init__()
    
    def startMusic(self):
        Sound.playTheme(songName='TitleTheme', loop=True)

class LevelSelectState(State):
    
    def __init__(self):
        super().__init__()

    def startMusic(self):
        Sound.playTheme(songName='TitleTheme', loop=True)


class RoomSelectState(State):
    
    def __init__(self):
        super().__init__()

    def startMusic(self):
        Sound.playTheme(songName='RoomSelectTheme', loop=True)

class RoomRollingState(State):
    
    def __init__(self):
        super().__init__()
    
    def startMusic(self):
        Sound.playTheme(songName='RoomSelectTheme', loop=True)

class BattleState(State):
    
    def __init__(self):
        super().__init__()
    
    def startMusic(self):
        Sound.playTheme(songName='BattleTheme1', loop=True)
        # Sound.playTheme(songName='BattleTheme2', loop=True)
        # Sound.playTheme(songName='VictoryTheme', loop=True)



class LoadState(State):
    
    def __init__(self):
        super().__init__()

    def startMusic(self):
        Sound.playTheme(songName='TitleTheme', loop=True)

class GameOver(State):

    def __init__(self):
        super().__init__()

    def startMusic(self):
        Sound.playTheme(songName='GameOverTheme', loop=True)

