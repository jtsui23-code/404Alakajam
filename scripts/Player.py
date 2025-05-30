#import Item as item

class Entity():

    def __init__(self):
        
        self.hearts = 8
        self.name = ''
        self.specialMoveName = ''
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
        self.name = 'Knight'
        # Deals 150 % more damage next turn but take 50% more damage next turn.
        self.specialMoveName = 'Dulist\'s Gambit'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

class Wizard(Entity):

    def __init__(self):

        self.hearts = 6
        self.name = 'Wizard'

        # Deals 2 heart of damage and applies burning status to 3 enemy cells. If the enemy lands on burned 
        # cells gain burn DOT (1 heart/turn).
        self.specialMoveName = 'Incinerate'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

        
class Goblin(Entity):

    def __init__(self):

        self.hearts = 4
        self.name = 'Goblin'

        # Permanty reduces enemy dmg by 50% per hit. 
        self.specialMoveName = 'Rusty Shiv'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

class Rat(Entity):

    def __init__(self):

        self.hearts = 4
        self.name = 'Rat'

        # Life steals 1 heart and turns 1 enemy B cell to a X cell for 2 turns.
        self.specialMoveName = 'Vermin Fangs' 
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None


class Thief(Entity):

    def __init__(self):

        self.hearts = 5
        self.name = 'Thief'

        # Encore (forces enmey to use the last move for 2 turns)
        self.specialMoveName = 'Pressure Point' 
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None




    
 





