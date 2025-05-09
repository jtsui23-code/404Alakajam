from Player import Entity

class Skeleton(Entity):

    def __init__(self):

        self.hearts = 8
        self.playerClass = 'Skeleton'
        self.specialMoveName = ''
        self.specialMove = None
        self.item = None
        self.upgradedAttack = None