from scripts.UI.main_menu import MainMenu
#from scripts.UI.shop import Shop
from scripts.UI.char_select import Character
from scripts.UI.shop import Shop





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
                triggered_action = Shop.render(self.screen)

            case 'character':
                triggered_action = Character.draw(self.screen)
                #self.Character(screen)
            case 'difficulty':
                pass
            
        return triggered_action 


    def handleEvent(self, state, event):
        match state:
            case 'shop':
                Shop.handle_event(event)
            case 'character':
                Character.handle_event(event)


    def stop(self, atr):
        match atr:
            case'menu':
                MainMenu.stop()
            case 'character':
                Character.stop()

    
