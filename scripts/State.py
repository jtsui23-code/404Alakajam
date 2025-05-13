# Import the pygame library for graphics and event handling
import pygame
# Import sys to allow for exiting the program
import sys
# Import Sound module to play music themes for different game states
from .Sound import MusicManager

# Manages switching between different game states

# In scripts/State.py

# Assuming your state classes (MainMenuState, ShopState, etc.) are defined
# in this file or imported appropriately. For example:
# from .main_menu_state import MainMenuState # If they are in separate files
# from .shop_state import ShopState
# ... and so on for all state classes

class StateManager:
    # --- Class-level attributes instead of instance attributes ---
    all_states_instances = {}  # Stores instances of your state classes
    current_state_name = None
    # setAction = None # This was in your __init__, its purpose isn't clear from the code
                      # If needed, it would also become a class attribute:
    # set_action_value = None

    @classmethod
    def initialize(cls):
        """
        Initializes the state manager's class-level data.
        Call this once when your game starts.
        """
        # Ensure state classes like MainMenuState, ShopState are defined/imported
        # For example, if MainMenuState is defined in this file:
        # global MainMenuState, ShopState, ... (if needed, but direct use is fine if in scope)

        cls.all_states_instances = {
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

        cls.setAction = None

        cls.current_state_name = 'main'  # Set the initial state name

        # Activate the initial state
        if cls.current_state_name in cls.all_states_instances:
            initial_state_object = cls.all_states_instances[cls.current_state_name]
            initial_state_object.changeStateStatus(True)
            # initial_state_object.startMusic() # Uncomment if needed and defined in your State classes
            print(f"StateManager initialized. Current state: {cls.current_state_name}")
        else:
            print(f"Error: Initial state '{cls.current_state_name}' not found during StateManager initialization.")

    @ classmethod
    def setAction(cls, action=""):
        cls.setAction = action

    @classmethod
    def checkCurrentState(cls, state_name_to_check=''):
        if cls.current_state_name == None:
            cls.current_state_name = 'main'
            
        print(f"current state is {cls.current_state_name}")
        print(f"name to check is {state_name_to_check}")
        return cls.current_state_name == state_name_to_check

    @classmethod
    def switchState(cls, next_state_name=''):
        print(f"StateManager: Attempting to switch from '{cls.current_state_name}' to '{next_state_name}'")
        # Deactivate the current state
        if cls.current_state_name in cls.all_states_instances:
            current_state_object = cls.all_states_instances[cls.current_state_name]
            current_state_object.changeStateStatus(False)
            # if hasattr(current_state_object, 'stopMusic'):
            #     current_state_object.stopMusic()
            print(f"StateManager: Deactivated state '{cls.current_state_name}'.")

        # Change to the new state name
        cls.current_state_name = next_state_name

        # Activate the new state
        if cls.current_state_name in cls.all_states_instances:
            next_state_object = cls.all_states_instances[cls.current_state_name]
            next_state_object.changeStateStatus(True)
            if hasattr(next_state_object, 'startMusic'): # Check if the method exists
                 next_state_object.startMusic()
            print(f"StateManager: Activated state '{cls.current_state_name}'.")
        else:
            print(f"Warning: State '{cls.current_state_name}' not found when trying to activate.")

    @classmethod
    def getCurrentStateObject(cls):
        """Returns the actual instance of the current state."""
        return cls.all_states_instances.get(cls.current_state_name)

# Important: You would need to define or import your state classes
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
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='TitleTheme', loop=True)


# Shop state
class ShopState(State):
    def __init__(self):
        super().__init__()

    # Play the shop theme when in this state
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='ShopTheme', loop=True)


# Character selection state
class CharacterSelectState(State):
    def __init__(self):
        super().__init__()

    # Play the title theme during character select
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='TitleTheme', loop=True)


# Level selection state
class LevelSelectState(State):
    def __init__(self):
        super().__init__()

    # Play the title theme during level select
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='TitleTheme', loop=True)


# Room selection state
class RoomSelectState(State):
    def __init__(self):
        super().__init__()

    # Play the room select theme
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='RoomSelectTheme', loop=True)


# Room rolling state
class RoomRollingState(State):
    def __init__(self):
        super().__init__()

    # Play the room select theme (same as above, maybe for continuity)
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='RoomSelectTheme', loop=True)


# Battle state
class BattleState(State):
    def __init__(self):
        super().__init__()

    # Play the battle theme when in battle
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='BattleTheme1', loop=True)
            # Other options for different phases
            # Sound.playTheme(songName='BattleTheme2', loop=True)
            # Sound.playTheme(songName='VictoryTheme', loop=True)


# Loading state
class LoadState(State):
    def __init__(self):
        super().__init__()

    # Play the title theme during loading
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='TitleTheme', loop=True)


# Game over state
class GameOver(State):
    def __init__(self):
        super().__init__()

    # Play the game over theme when in this state
    def startMusic(self):
        if self.isCurrentState:
            MusicManager.playTheme(songName='GameOverTheme', loop=True)
