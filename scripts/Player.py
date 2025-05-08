import Item as item

class Entity():

    def __init__(self):
        
        self.hearts = 8
        self.playerClass = ''
        self.speicalMoveName = ''
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

    def takeDmg(self, dmg):
        self.hearts -= dmg
        print(f"Player took "+ {dmg} + " and has " + {self.hearts} + "remaining hearts")

    def heal(self, amount):
        temp = self.hearts
        self.hearts += amount
        print(f"Player had " + {temp} + "amount of hearts but healed so now has " + {self.hearts})


class Knight(Entity):

    def __init__(self):

        self.hearts = 8
        self.playerClass = 'Knight'
        self.speicalMoveName = 'Dulist\'s Gamebit'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

class Wizard(Entity):

    def __init__(self):

        self.hearts = 6
        self.playerClass = 'Wizard'

         # Deals 1 heart of dmg and applies burn 60% of the time(1 heart per turn)
        self.speicalMoveName = 'Incinerate'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

        
class Goblin(Entity):

    def __init__(self):

        self.hearts = 4
        self.playerClass = 'Goblin'

         # Permanty reduces enemy dmg by 50% per hit. 
        self.speicalMoveName = 'Rusty Shiv'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

class Rat(Entity):

    def __init__(self):

        self.hearts = 4
        self.playerClass = 'Rat'

        # Life steals 1 heart
        self.speicalMoveName = 'Vermin Fangs' 
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None


class Thief(Entity):

    def __init__(self):

        self.hearts = 5
        self.playerClass = 'Thief'

        # Encore (forces enmey to use the last move for 2 turns)
        self.speicalMoveName = 'Pressure Point' 
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None




    
 





