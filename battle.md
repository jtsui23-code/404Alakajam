# Battle System Documentation

## Battle.py - Core Battle Controller

### Overview
The `BattleData` class manages all battle logic, entities, and UI interactions. It serves as the central hub connecting player actions, enemy behavior, and UI updates.

### Key Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `custom_attack()` | None | Handles attack logic when player clicks Attack button |
| `open_inventory()` | None | Placeholder for inventory functionality (currently prints "Open") |
| `attempt_escape()` | None | Placeholder for escape functionality (currently prints "Escape") |
| `game_over()` | None | Triggers when player loses all hearts |
| `victory_sequence()` | None | Triggers when enemy loses all hearts |
| `checkWin()` | None | Checks battle outcome and resets state |

### Attack Logic
```python
def custom_attack(self):
    # Update UI hearts
    self.screen.remove_hearts(player=1)
    self.screen.remove_hearts(enemy=1)
    
    # Grid interaction
    cell = GridLogic.chooseCell(self.playerGrid)
    print(cell)  # Output: 'B', 'R', 'S', 'U', or 'X'
    print("Enemy hit!")
```

### Battle Resolution
```python
def game_over(self):
    self.done = 'enemy'  # Flag enemy victory
    print("Game Over")

def victory_sequence(self):
    self.done = 'player'  # Flag player victory
    print("You Won!")

def checkWin(self):
    temp = self.done
    self.done = 'None'  # Reset state
    return temp  # Returns 'player' or 'enemy'
```

---

## battleui_dynamic.py - UI Methods Reference

### Core UI Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `set_callback(button_name, callback)` | `button_name`: 'attack', 'bag', 'run'<br>`callback`: Function | Binds action to UI button |
| `set_defeat_callback(target, callback)` | `target`: 'player' or 'enemy'<br>`callback`: Function | Sets defeat handler |
| `set_hearts(player_hearts, enemy_hearts, max_hearts)` | `player_hearts`: Int<br>`enemy_hearts`: Int<br>`max_hearts`: (Int, Int) | Sets current/max hearts |
| `add_hearts(player, enemy)` | `player`: Hearts to add<br>`enemy`: Hearts to add | Increases heart count |
| `remove_hearts(player, enemy)` | `player`: Hearts to remove<br>`enemy`: Hearts to remove | Decreases heart count |
| `handle_events(event)` | `event`: Pygame event | Processes UI interactions |
| `draw()` | None | Renders all UI elements |

### Heart Management Examples
```python
# Set initial hearts (5 player, 3 enemy)
battle_ui.set_hearts(player_hearts=5, enemy_hearts=3, max_hearts=(5, 3))

# Damage enemy by 1 heart
battle_ui.remove_hearts(enemy=1)

# Heal player by 2 hearts
battle_ui.add_hearts(player=2)
```

### Callback Binding
```python
# Bind custom attack logic
battle_ui.set_callback('attack', custom_attack_function)

# Custom victory handler
battle_ui.set_defeat_callback('enemy', lambda: print("Victory!"))
```

---

## GridLogic Methods (Grid.py)

### Core Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `generateGrid()` | None | Creates 3x3 grid with random symbols |
| `chooseCell(grid)` | `grid`: 2D array | Selects random cell from grid |
| `displayGrid(grid, arr, font)` | `grid`: Grid object<br>`arr`: 2D symbol array<br>`font`: Pygame font | Populates grid UI with symbols |
| `setGridCallback(grid, row, col, callback)` | `grid`: Grid object<br>`row`: 0-2<br>`col`: 0-2<br>`callback`: Function | Sets cell click handler |

### Grid Symbols
- `B`: Basic attack
- `R`: Random effect
- `S`: Special attack
- `U`: Ultimate
- `X`: Empty

### Usage Example
```python
# Generate grid
grid = GridLogic.generateGrid()  # Returns 3x3 array

# Get random cell
cell = GridLogic.chooseCell(grid)  # Returns 'B', 'R', etc.

# Display grid in UI
GridLogic.displayGrid(ui_grid, grid, font)
```

### [Battle.py] Initialization
```python
def __init__(self, screen):
    self.done = False  # Battle completion flag
    self.screen = BattleScreen(screen)  # UI controller
    
    # Entity initialization
    self.player = Knight()  # Player character
    self.enemy = Skeleton()  # Enemy character
    
    # Grid systems
    self.playerGrid = GridLogic.generateGrid()  # 3x3 player grid
    self.enemyGrid = GridLogic.generateGrid()   # 3x3 enemy grid
    
    # UI setup
    self.screen.set_hearts(
        player_hearts=self.player.hearts,
        enemy_hearts=self.enemy.hearts,
        max_hearts=(self.player.hearts, self.enemy.hearts)
    )
    
    # Callback bindings
    self.screen.set_callback('attack', self.custom_attack)
    self.screen.set_defeat_callback('player', self.game_over)
    self.screen.set_defeat_callback('enemy', self.victory_sequence)
    
    self.turn = [self.player]  # Turn sequence
```
---

## Main Script Implementation Example
```python
import pygame
from Battle import BattleData

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create battle instance
battle = BattleData(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        battle.screen.handle_events(event)  # Process UI events
    
    # Render battle
    screen.fill((0, 0, 0))
    battle.screen.draw()
    pygame.display.flip()
    
    # Check battle status
    result = battle.checkWin()
    if result == 'player':
        print("Victory!")
        running = False
    elif result == 'enemy':
        print("Defeat!")
        running = False
    
    clock.tick(60)

pygame.quit()
```



## Key Integration Points
1. **Initialization**: Create `BattleData` with Pygame surface
2. **Event Handling**: Pass events to `battle.screen.handle_events()`
3. **Rendering**: Call `battle.screen.draw()` each frame
4. **Outcome Check**: Use `battle.checkWin()` to detect battle end
5. **Custom Logic**: Extend `custom_attack()` for game-specific mechanics
