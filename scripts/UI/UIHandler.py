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
                triggered_action = MainMenu.render(self.screen)
            case 'shop':
                pass
 #               self.Shop.render(self.screen)
            case 'character':
                triggered_action = Character.draw(self.screen)
                #self.Character(screen)
            case 'difficulty':
                pass
<<<<<<< HEAD

        return triggered_action 
=======
            
>>>>>>> 294a718ce4c10a1214caffb0fcada4c2a336daaa
    def stop(self, atr):
        match atr:
            case'menu':
                MainMenu.stop()
            case 'character':
                Character.stop()

    
