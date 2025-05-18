import pygame
import pygame.font
from scripts.Grid import Grid, GridLogic

class BattleScreen:
    """Battle screen UI component with configurable callbacks and heart management.
    
    Features:
    - Left and right panels with grids
    - Center panel with action buttons
    - Heart-based health display
    - Fully configurable button callbacks
    - Methods for heart management
    - Tracks battle outcome (who lost)
    """
    
    def __init__(self, screen):
        """Initialize the battle screen.
        
        Args:
            screen (pygame.Surface): The main display surface
        """
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.width, self.height = screen.get_size()
        
        # UI Colors
        self.colors = {
            'background': (20, 20, 40),
            'panel': (30, 30, 60),
            'button': (70, 70, 120),
            'button_hover': (100, 100, 150),
            'text': (255, 255, 255),
            'heart': (255, 50, 50),
            'empty_heart': (80, 80, 80)
        }
        
        # Health tracking
        self.player_hearts = 5
        self.max_player_hearts = 5
        self.enemy_hearts = 3
        self.max_enemy_hearts = 3
        
        # Battle outcome tracking
        self.battle_outcome = None  # None = ongoing, 'player' = player lost, 'enemy' = enemy lost
        
        # Initialize UI components
        self.player_grids = self._create_grids(left=True)
        self.enemy_grids = self._create_grids(left=False)
        self.buttons = self._create_buttons()
        
        # Default button callbacks (can be overwritten)
        self.callbacks = {
            'attack': lambda: print("Attack pressed"),
            'bag': lambda: print("Bag pressed"),
            'run': lambda: print("Run pressed"),
            'player_defeated': lambda: self._set_outcome('player'),
            'enemy_defeated': lambda: self._set_outcome('enemy')
        }

    def _set_outcome(self, loser):
        """Internal method to set the battle outcome.
        
        Args:
            loser (str): 'player' or 'enemy' indicating who lost
        """
        self.battle_outcome = loser
        print(f"Battle over! {loser.capitalize()} was defeated!")

    def get_outcome(self):
        """Get the current battle outcome.
        
        Returns:
            str: None if battle ongoing, 'player' if player lost, 'enemy' if enemy lost
        """
        return self.battle_outcome

    def reset_battle(self):
        """Reset the battle state for a new battle."""
        self.player_hearts = self.max_player_hearts
        self.enemy_hearts = self.max_enemy_hearts
        self.battle_outcome = None

    # Grid Creation ------------------------------------------------------------
    def _create_grids(self, left):
        """Create player or enemy grids.
        
        Args:
            left (bool): True for player (left side), False for enemy (right side)
            
        Returns:
            list: List of Grid objects
        """
        grids = []
        grid_size = min(self.width * 0.28, self.height * 0.2)
        start_x = self.width * 0.1 if left else self.width * 0.9 - grid_size
        
        for i in range(3):
            rows, cols = (1, 1) if i == 0 else (3, 3)
            y = 100 + i * (grid_size + 20)
            grid = Grid(start_x, y, grid_size, grid_size, rows, cols)
            GridLogic.displayGrid(grid, GridLogic.generateGrid(), self.font)
            grids.append(grid)
        return grids

    # Button Management --------------------------------------------------------
    def _create_buttons(self):
        """Create the action buttons in the center panel.
        
        Returns:
            list: List of button dictionaries with rect and text
        """
        buttons = []
        center_x = self.width * 0.5
        button_width = self.width * 0.18
        
        button_data = [
            ("Attack", 'attack', -70),
            ("Bag", 'bag', 0),
            ("Run", 'run', 70)
        ]
        
        for text, callback_key, y_offset in button_data:
            rect = pygame.Rect(0, 0, button_width, 50)
            rect.center = (center_x, self.height/2 + y_offset)
            buttons.append({
                "rect": rect,
                "text": text,
                "callback_key": callback_key
            })
        return buttons
    
    def set_callback(self, button_name, callback):
        """Set a callback for a specific button.
        
        Args:
            button_name (str): 'attack', 'bag', or 'run'
            callback (function): Function to call when button is pressed
        """
        if button_name in self.callbacks:
            self.callbacks[button_name] = callback
        else:
            raise ValueError(f"Unknown button: {button_name}")

    # Heart Management --------------------------------------------------------
    def set_hearts(self, player_hearts=None, enemy_hearts=None, max_hearts=None):
        """Set heart counts for player and/or enemy.
        
        Args:
            player_hearts (int, optional): Current player hearts
            enemy_hearts (int, optional): Current enemy hearts
            max_hearts (tuple, optional): (max_player, max_enemy) hearts
        """
        if player_hearts is not None:
            self.player_hearts = player_hearts
        if enemy_hearts is not None:
            self.enemy_hearts = enemy_hearts
        if max_hearts:
            self.max_player_hearts, self.max_enemy_hearts = max_hearts
        
        # Check for defeat conditions after setting hearts
        self._check_heart_depletion()
    
    def add_hearts(self, player=0, enemy=0):
        """Add hearts to player or enemy.
        
        Args:
            player (int): Hearts to add to player
            enemy (int): Hearts to add to enemy
        """
        self.player_hearts = min(self.player_hearts + player, self.max_player_hearts)
        self.enemy_hearts = min(self.enemy_hearts + enemy, self.max_enemy_hearts)
        
        # Check for defeat conditions after adding hearts
        self._check_heart_depletion()
    
    def remove_hearts(self, player=0, enemy=0):
        """Remove hearts from player or enemy.
        
        Args:
            player (int): Hearts to remove from player
            enemy (int): Hearts to remove from enemy
        """
        self.player_hearts = max(0, self.player_hearts - player)
        self.enemy_hearts = max(0, self.enemy_hearts - enemy)
        
        # Check for defeat conditions after removing hearts
        self._check_heart_depletion()

    def _check_heart_depletion(self):
        """Check if either party has run out of hearts and trigger callbacks."""
        if self.player_hearts <= 0 and self.battle_outcome is None:
            self.callbacks['player_defeated']()
        if self.enemy_hearts <= 0 and self.battle_outcome is None:
            self.callbacks['enemy_defeated']()

    def set_defeat_callback(self, target, callback):
        """Set a callback for when a target runs out of hearts.
        
        Args:
            target (str): 'player' or 'enemy'
            callback (function): Function to call when target is defeated
        """
        if target == 'player':
            self.callbacks['player_defeated'] = callback
        elif target == 'enemy':
            self.callbacks['enemy_defeated'] = callback
        else:
            raise ValueError("Target must be either 'player' or 'enemy'")

    # Drawing Methods ---------------------------------------------------------
    def draw_hearts(self, count, max_count, left=True):
        """Draw heart indicators showing current/max health.
        
        Args:
            count (int): Current heart count
            max_count (int): Maximum heart count
            left (bool): True for player (left side), False for enemy (right side)
        """
        radius, spacing = 15, 35
        start_x = 30 if left else self.width - 30 - max_count * spacing
        
        for i in range(max_count):
            x = start_x + i * spacing
            color = self.colors['heart'] if i < count else self.colors['empty_heart']
            pygame.draw.circle(self.screen, color, (x, 40), radius)

    # Event Handling ----------------------------------------------------------
    def handle_events(self, event):
        """Handle pygame events for UI interaction.
        
        Args:
            event (pygame.Event): The event to handle
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle button clicks
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    self.callbacks[button["callback_key"]]()
            
            # Pass events to grids
            for grid in self.player_grids + self.enemy_grids:
                grid.handle_event(event)

    # Main Drawing Method -----------------------------------------------------
    def draw(self):
        """Draw all UI elements to the screen."""
        # Draw side panels
        panel_widths = [self.width * 0.35, self.width * 0.3, self.width * 0.35]
        for i, w in enumerate(panel_widths):
            x = sum(panel_widths[:i])
            pygame.draw.rect(self.screen, self.colors['panel'], (x, 0, w, self.height))
        
        # Draw hearts
        self.draw_hearts(self.player_hearts, self.max_player_hearts)
        self.draw_hearts(self.enemy_hearts, self.max_enemy_hearts, left=False)
        
        # Draw grids
        for grid in self.player_grids + self.enemy_grids:
            grid.draw(self.screen, self.font)
        
        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            color = self.colors['button_hover' if is_hover else 'button']
            
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, (100, 100, 100), button["rect"], 2)
            
            text = self.font.render(button["text"], True, self.colors['text'])
            self.screen.blit(text, text.get_rect(center=button["rect"].center))