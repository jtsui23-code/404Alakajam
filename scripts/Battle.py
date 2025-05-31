import random
from scripts.Player import Knight
from scripts.Enemy import Skeleton
from scripts.Grid import GridLogic
from scripts.UI.battleui_dynamic import BattleScreen

class BattleData:
    def __init__(self, screen):
        self.done = False
        self.screen = BattleScreen(screen)
        self.screen.set_callback('attack', self.custom_attack)

        self.player = Knight()
        self.playerGrid = GridLogic.generateGrid()

        self.enemy = Skeleton()
        self.enemyGrid = GridLogic.generateGrid()

        self.screen.set_hearts(player_hearts=self.player.hearts, enemy_hearts=self.enemy.hearts, max_hearts=(self.player.hearts, self.enemy.hearts))

        self.screen.set_defeat_callback('player', lambda: self.game_over())
        self.screen.set_defeat_callback('enemy', lambda: self.victory_sequence())

        self.turn = [self.player]

    def getAll(self):
        return str(self.turn), str(self.player), str(self.enemy)
   
    def custom_attack(self):
        # Choose cells randomly for demonstration
        player_row, player_col = random.randint(0, 2), random.randint(0, 2)
        enemy_row, enemy_col = random.randint(0, 2), random.randint(0, 2)
        
        # Get the cell values
        playerCell = self.playerGrid[player_row][player_col]
        enemyCell = self.enemyGrid[enemy_row][enemy_col]
        
        # Show which cells were selected by highlighting them
        # Player grids: index 0 (1x1 hero), index 1 (3x3), index 2 (3x3)
        # Enemy grids: index 0 (1x1 enemy), index 1 (3x3), index 2 (3x3)
        # Use index 1 for player (left side) and index 1 for enemy (right side)
        self.screen.set_selected_cell(1, player_row, player_col, is_player=True)   # Player's 3x3 grid
        self.screen.set_selected_cell(1, enemy_row, enemy_col, is_player=False)    # Enemy's 3x3 grid
        
        print('-----------------------------------------------------------------------------')
        print(f"Player selected cell ({player_row}, {player_col}): {playerCell}")
        print(f"Enemy selected cell ({enemy_row}, {enemy_col}): {enemyCell}")
        
        # Player's turn
        if playerCell == 'B':
            print("Player did basic hit ")
            self.screen.remove_hearts(enemy=1)
        elif playerCell == 'S':
            print('Player did special attack')
            self.screen.remove_hearts(enemy=1)
        elif playerCell == 'U':
            print('Player did upgraded attack')
            self.screen.remove_hearts(enemy=1)
        elif playerCell == 'X':
            print('Player missed')

        # Enemy's turn
        if enemyCell == 'B':
            print("Enemy did basic hit ")
            self.screen.remove_hearts(player=1)
        elif enemyCell == 'S':
            print('Enemy did special attack')
            self.screen.remove_hearts(player=1)
        elif enemyCell == 'U':
            print('Enemy did upgraded attack')
            self.screen.remove_hearts(player=1)
        elif enemyCell == 'X':
            print('Enemy missed')

        print('-----------------------------------------------------------------------------\n\n')

    def open_inventory(self):
        print("Open")

    def attempt_escape(self):
        print("Escape")

    def game_over(self):
        self.done = 'enemy'
        print("Game Over")

    def checkWin(self):
        # Needs to return temp because the self.done has to be reset or the
        # next battle will instantly end.
        temp = self.done
        self.done = 'None'
        return temp
     
    def victory_sequence(self):
        self.done = 'player'
        print("You Won!")

    def clear_selections(self):
        """Clear all grid selections - useful for resetting between turns"""
        self.screen.clear_all_selections()

    def show_available_moves(self):
        """Highlight all available moves for the player"""
        # This could be expanded to show which cells the player can choose from
        # For now, it just clears selections to show all options are available
        self.clear_selections()