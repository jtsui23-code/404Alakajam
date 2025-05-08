import random

from scripts.Player import Knight
from scripts.Enemy import Skeleton


class BattleData:
    def __init__(self):
        self.turn = [True]
        self.you = [True, False] 
        self.enemy = [True, False]

    def getAll(self):
        return str(self.turn), str(self.you), str(self.enemy)



class Info:
    def Random():
        odds = random.randint(1,5)
        print(f"Someone chose basic attack!! Your damage is ", {odds})
    def Odds():
        odds = random.randint(1,100)
        if odds > 66:
            print("Someone took the odds, but they missed!")
        else:
            print("Someone did a basic strike!")
            Info.Random()
    def output(num):
        print("Attack is underway!")
        match num:
            case 4:
                print("Someone did nothing!")
            case 0 | 6:
               Info.Random()
            case 1 | 3 | 5 | 7:
                Info.Odds()
            case 8:
                print("Someone chose an upgratable attack!")
            case 2:
                print("Someone used your special attack")


battle =  BattleData()
battle.you = Knight()
battle.enemy = Skeleton()

print(battle.getAll())

while True:
    chosen = input("\n Attack! Enter a grid number: ")
    Info.output(int(chosen))

    #Enemy's turn
    print("\n Now it's the enemy's turn! \n")
    Info.output(int(random.randint(0,8)))