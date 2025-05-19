import pygame
from scripts.UI.main_menu import MainMenu
#from scripts.UI.shop import Shop
from scripts.UI.char_select import Character
from scripts.UI.shop import Shop
from scripts.UI.difficulty import DifficultySelector
from scripts.UI.level import LevelSelectionScreen


from scripts.Battle import BattleData



class UIHandler:
    def __init__(self, screen):
        self.screen = screen
        
        self.battleData = BattleData(self.screen)        
       # self.Shop = Shop()
       # self.Character = Character()

    
    def render(self,atr):
        match atr:
            case 'menu':
                triggered_action = MainMenu.render(self.screen)
            case 'shop':
                triggered_action = Shop.render(self.screen)

            case 'character':
                triggered_action = Character.draw(self.screen)
                #self.Character(screen)
            case 'difficulty':
                LevelSelectionScreen.init(pygame.font.SysFont("Arial",72))
                triggered_action = DifficultySelector.draw(self.screen)
            case 'roomSelect':
                triggered_action = LevelSelectionScreen.draw(self.screen)
            
            case 'battle':

                triggered_action = self.battleData.screen.draw()
            
        return triggered_action 


    def handleEvent(self, state, event):
        match state:
            case 'shop':
                Shop.handle_event(event)
            case 'character':
                Character.handle_event(event)

            case 'levelSelect':
                DifficultySelector.update(event)
            
            case 'roomSelect':
                LevelSelectionScreen.handle_event(event)

            case 'battle':
                self.battleData.screen.handle_events(event)

    def stop(self, atr):
        match atr:
            case'menu':
                MainMenu.stop()
            case 'character':
                Character.stop()

    
    def checkOutCome(self):
        outcome = self.battleData.checkWin()
        print(outcome)

        if outcome == 'player':
            return 'won'
        elif outcome == 'enemy':
            return 'lost'
        else:
            return 'battling'

    