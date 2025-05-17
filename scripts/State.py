# Import the pygame library for graphics and event handling
import pygame
# Import sys to allow for exiting the program
import sys
# Import Sound module to play music themes for different game states
from .Sound import MusicManager



class StateManager():

    def __init__(self):

# Dictionary storing all game state classes

        self.allStates = {
        'main': MainMenuState(),
        'shop': ShopState(),
        'character': CharacterSelectState(),
        'levelSelect': LevelSelectState(),
        'roomSelect': RoomSelectState(),
        'roomRolling': RoomRollingState(),
        'battle': BattleState(),
        'load': LoadState(),
        'gameOver': GameOver()

        }

        self.musicManager = MusicManager()

        self.setAction = None



        # Set the initial state to main menu

        self.currentState = 'main'

        # Activate the main menu state

        self.allStates[self.currentState].changeStateStatus(True)

        # Start the music for the main menu
        self.musicManager.playTheme(self.currentState, True)



    def checkCurrentState(self, currentState):

        return self.currentState == currentState


    # Switches to a different game state

    def switchState(self, nextState=''):

    # Deactivate the current state

        self.allStates[self.currentState].changeStateStatus(False)

        # Change to the new state

        self.currentState = nextState

        # Activate the new state

        self.allStates[self.currentState].changeStateStatus(True)

        # Start the music for the new state
        if self.currentState == 'battle':

            self.musicManager.playTheme(self.currentState, True)


# (MainMenuState, ShopState, etc.) before StateManager if you refer to them directly
# as above. For example:
# class State: ...
# class MainMenuState(State): ...
# class ShopState(State): ...
# etc.


# Base class for all game states
class State:
    def __init__(self):
        # Flag to determine if this state is currently active
        self.isCurrentState = False
        # Dictionary to store UI elements like buttons
        self.uiElements = {}

    # Renders the UI elements of this state to the screen
    def render(self, screen):
        if self.isCurrentState:
            for element in self.uiElements:
                element.render(screen)

    # Calls render only if this state is active
    def update(self, screen):
        if self.isCurrentState:
            self.render(screen)

    # Returns whether this state is the current state
    def checkCurrentState(self):
        return self.isCurrentState

    # Sets the state’s active status (True or False)
    def changeStateStatus(self, input=False):
        self.isCurrentState = input

    # Handles events (e.g. quitting, mouse clicks) when state is active
    def handleEvent(self, event):
        if self.isCurrentState:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handleMosClick(event.pos)

    # Optional method to add hover effects to UI (not yet implemented)
    def hoverEffect(self):
        pass

    # # Handles what happens when the mouse clicks on a button
    # def handleMosClick(self, mosPos):
    #     if self.isCurrentState:
    #         # Check if a UI button was clicked
    #         for key, element in self.uiElements.items():
    #             if isinstance(element, Button) and element.rect.collidepoint(mosPos):
    #                 self.buttonClicked(key)

    # Called when a button is clicked, to be overridden by child classes
    def buttonClicked(self, buttonKey):
        pass

    # Starts music for this state, to be overridden by child classes
    def startMusic(self):
        pass


# Main menu state
class MainMenuState(State):
    def __init__(self):
        super().__init__()

    # Play the title theme when in this state
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='TitleTheme', loop=True)


# Shop state
class ShopState(State):
    def __init__(self):
        super().__init__()

    # Play the shop theme when in this state
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='ShopTheme', loop=True)


# Character selection state
class CharacterSelectState(State):
    def __init__(self):
        super().__init__()

    # Play the title theme during character select
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='TitleTheme', loop=True)


# Level selection state
class LevelSelectState(State):
    def __init__(self):
        super().__init__()

    # Play the title theme during level select
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='TitleTheme', loop=True)


# Room selection state
class RoomSelectState(State):
    def __init__(self):
        super().__init__()

    # Play the room select theme
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='RoomSelectTheme', loop=True)


# Room rolling state
class RoomRollingState(State):
    def __init__(self):
        super().__init__()

    # Play the room select theme (same as above, maybe for continuity)
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='RoomSelectTheme', loop=True)


# Battle state
class BattleState(State):
    def __init__(self):
        super().__init__()

    # Play the battle theme when in battle
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='BattleTheme1', loop=True)
            # Other options for different phases
            # Sound.playTheme(songName='BattleTheme2', loop=True)
            # Sound.playTheme(songName='VictoryTheme', loop=True)


# Loading state
class LoadState(State):
    def __init__(self):
        super().__init__()

    # Play the title theme during loading
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='TitleTheme', loop=True)


# Game over state
class GameOver(State):
    def __init__(self):
        super().__init__()

    # Play the game over theme when in this state
    # def startMusic(self):
    #     if self.isCurrentState:
    #         MusicManager.playTheme(songName='GameOverTheme', loop=True)
