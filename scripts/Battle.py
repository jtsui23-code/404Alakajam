import random

from scripts.Player import Knight
from scripts.Enemy import Skeleton
from scripts.Grid import GridLogic
from scripts.UI.battleui_dynamic import BattleScreen


class BattleData:
    def __init__(self, screen):
        self.screen = BattleScreen(screen)
        self.screen.set_callback('attack', self.custom_attack)

        self.player = Knight()
        self.playerGrid = GridLogic.generateGrid()

        self.enemy = Skeleton()
        self.enemyGrid = GridLogic.generateGrid()
 

        self.screen.set_hearts(player_hearts=self.player.hearts, enemy_hearts= self.enemy.hearts, max_hearts=(self.player.hearts,self.enemy.hearts))

        self.screen.set_defeat_callback('player', lambda: self.game_over())
        self.screen.set_defeat_callback('enemy', lambda: self. victory_sequence())

        self.turn = [self.player]

    def getAll(self):
        return str(self.turn), str(self.you), str(self.enemy)
    
    def custom_attack(self):
        self.screen.remove_hearts(enemy=1)
        print("Enemy hit!")

    def open_inventory(self):
        print("Open")

    def attempt_escape(self):
        print("Escape")

    def game_over(self):
        print("Game Over")
    
    def victory_sequence(self):
        print("You Won!")

"""
Ignore everything past here. Old code
"""



"""
class GridLogic:
    def __init__(self):
        self.grid = ['B', 'R', 'S', 'R', 'X', 'R', 'B' , 'R', 'U']
        self.chosenCell = 0

        self.randomizeGrid()

    def randomizeGrid(self):
        self.grid[1] = self.Odds()
        self.grid[3] = self.Odds()
        self.grid[5] = self.Odds()
        self.grid[7] = self.Odds()

    def Odds(self):
        odds = random.randint(1,100)
        if odds > 66:
            return 'B'
        else:
            return 'X'
        
    def BasicAttack(self):
        odds = random.randint(1,5)
        print(f"Someone chose basic attack!! Your damage is ", {odds})

        
    def output(self):
        print("Attack is underway!")
        self.chosenCell = random.randint(0,8)
        match self.grid[self.chosenCell]:
            case 'X':
                print("Someone did nothing!")
            case 'B':
               print("You did a basic attack!")
               self.BasicAttack()
            case 'U':
                print("Someone chose an upgratable attack!")
            case 'S':
                print("Someone used your special attack")

"""
"""
playerGrid = GridLogic()
enemyGrid = GridLogic()
battle =  BattleData()
battle.you = Knight()
battle.enemy = Skeleton()

print(playerGrid.grid)
print(enemyGrid.grid)

#print(battle.getAll())
"""

"""
while True:
    chosen = input("Attack! Press any key to continue: ")
    print("Player is performing.")

    playerGrid.output()

    #Enemy's turn
    print("\n Now it's the enemy's turn!")
    enemyGrid.output()

    print('---------------------------------------------')
"""