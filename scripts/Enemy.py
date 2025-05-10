from scripts.Player import Entity

# Special inflicts status on player cell(s)
class Skeleton(Entity):

    def __init__(self):

        self.hearts = 6
        self.playerClass = 'Skeleton'
        # Randomly selects a player column and turns all of the cells to X cells for a turn.
        self.specialMoveName = 'Bone Barricade'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

# Special inflicts status on player cell(s)
class Bat(Entity):

    def __init__(self):

        self.hearts = 5
        self.playerClass = 'Bat'
        # Picks three random cells. If the cell seletect is a damaging cell, player takes 0.5 hearts. Meaning 
        # if all three of the randomly selected cells are damaging ones the player takes 1.5 hearts of damage.
        # If the player lands on any of these cells next turn, they take additional 0.5 hearts.
        self.specialMoveName = 'Swarm Frenzy'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

class Slime(Entity):

    def __init__(self):

        self.hearts = 7
        self.playerClass = 'Slime'
        # Gain additional B cell, if cannot gain anymore then applies DOT (1 heart/turn)
        self.specialMoveName = 'Swarm Frenzy'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

# Special inflicts status on player cell(s)
class Undead(Entity):

    def __init__(self):

        self.hearts = 8
        self.playerClass = 'Undead'
        # Infects player grid for battle. Every turn 1 Non-corner cell becomes a X cell.
        # Following attacks deal + 0.5 hearts for next 2 turns 
        self.specialMoveName = 'Necrotic Rot'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None

# Special inflicts status on player cell(s)
class Ghost(Entity):

    def __init__(self):

        self.hearts = 8
        self.playerClass = 'Ghost'
        # Curses 2 non speical cells(S, U) if the player lands on the cursed cell takes 1 heart damage 
        # and ghost heals 1 heart. Curse lasts for 2 turns.
        self.specialMoveName = 'Necrotic Rot'
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None