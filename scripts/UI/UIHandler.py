from scripts.UI.main_menu import MainMenu
#from scripts.UI.shop import Shop
from scripts.UI.char_select import Character




class UIHandler:
    def __init__(self, screen):
        self.screen = screen
        
       # self.Shop = Shop()
       # self.Character = Character()
    def render(self,atr):
        match atr:
            case 'menu':
                MainMenu.render(self.screen)
            case 'shop':
                pass
 #               self.Shop.render(self.screen)
            case 'character':
                Character.draw(self.screen)
                #self.Character(screen)
            case 'difficulty':
<<<<<<< HEAD
                DifficultySelector.initialize(self.screen)
                DifficultySelector.draw(self.screen)
        
=======
                pass
>>>>>>> e7dd87962495958ae05dc335d3c08ee130fc5b3a
    def stop(self, atr):
        match atr:
            case'menu':
                MainMenu.stop()
            case 'character':
                Character.stop()
<<<<<<< HEAD
            case _:
                MainMenu.stop()
                Character.stop()
    def setAction(self):
        pass
=======

    
>>>>>>> e7dd87962495958ae05dc335d3c08ee130fc5b3a
