import pygame
import pygame.font
from scripts.Grid import Grid, GridLogic

ENEMY_TYPES = {
    "Slime": "Media/enemy/Slime.png",
    "Ghost": "Media/enemy/Ghost.png",
    "Zombie": "Media/enemy/Zombie.png",
    "Skeleton": "Media/enemy/Skeleton.png",
    "bat": "Media/enemy/Bat.png",
}

class BattleScreen:
    """Battle screen UI component with configurable callbacks and heart management."""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        
        self.enemy_type = None
        
        self.colors = {
            'panel': (30, 30, 60),
            'button': (70, 70, 120),
            'button_hover': (100, 100, 150),
            'text': (255, 255, 255),
            'heart': (255, 50, 50),
            'empty_heart': (80, 80, 80)
        }
        
        self.player_hearts = 5
        self.max_player_hearts = 5
        self.enemy_hearts = 3
        self.max_enemy_hearts = 3

        # Heart sprite setup
        self.target_heart_diameter = 30
        self.heart_sprite_full_scaled = None
        try:
            original_heart_sprite = pygame.image.load("Media/cell/Heart.png").convert_alpha()
            self.heart_sprite_full_scaled = pygame.transform.scale(
                original_heart_sprite,
                (self.target_heart_diameter, self.target_heart_diameter)
            )
        except pygame.error as e:
            print(f"Warning: Could not load or scale heart sprite: {e}")
            self.heart_sprite_full_scaled = None
        
        # Background setup
        try:
            self.bg_image = pygame.image.load("Media/background/battle.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        except pygame.error as e:
            print(f"Warning: Could not load background image: {e}")
            self.bg_image = None
        
        self.player_grids = self._create_grids(left=True)
        self.enemy_grids = self._create_grids(left=False)
        self.buttons = self._create_buttons()
        
        self.callbacks = {
            'attack': lambda: print("Attack pressed"),
            'bag': lambda: print("Bag pressed"),
            'run': lambda: print("Run pressed"),
            'player_defeated': lambda: print("Player was defeated!"),
            'enemy_defeated': lambda: print("Enemy was defeated!")
        }

        if self.enemy_type:
            self.update_enemy_grid()

    def set_enemy(self, encounter_data):
        """Set the enemy based on encounter data"""
        if encounter_data.get('type') == 'enemy':
            self.enemy_type = encounter_data.get('name', 'Slime')
            if hasattr(self, 'enemy_grids') and self.enemy_grids:
                self.update_enemy_grid()

    def update_enemy_grid(self):
        """Update the enemy grid with the current enemy type"""
        if not self.enemy_type or not self.enemy_grids:
            return
            
        try:
            enemy_img = pygame.image.load(ENEMY_TYPES[self.enemy_type]).convert_alpha()
            scaled_img = pygame.transform.scale(
                enemy_img,
                (self.enemy_grids[0].cell_width - 10, self.enemy_grids[0].cell_height - 10)
            )
            self.enemy_grids[0].fill_cell_with_image(0, 0, scaled_img, 
                                                     lambda: self.enemy_grids[0].set_selected_cell(0,0))
        except Exception as e:
            print(f"Error loading enemy image: {e}")
            self.enemy_grids[0].fill_cell(0, 0, self.enemy_type, self.font, 
                                          lambda: self.enemy_grids[0].set_selected_cell(0,0))

    def _create_grids(self, left):
        grids = []
        grid_size = min(self.width * 0.28, self.height * 0.2)
        start_x = self.width * 0.1 if left else self.width * 0.9 - grid_size
        
        for i in range(3):
            if i == 0:
                rows, cols = (1, 1)
            else:
                rows, cols = (3, 3)

            y = 100 + i * (grid_size + 20)
            grid = Grid(start_x, y, grid_size, grid_size, rows, cols)
            
            if i == 0 and not left:  # Enemy side
                grid.fill_cell(0, 0, "???", self.font, lambda: grid.set_selected_cell(0,0))
            elif i == 0 and left:  # Player side
                grid.fill_cell(0, 0, "HERO", self.font, lambda: grid.set_selected_cell(0,0))
            else:
                GridLogic.displayGrid(grid, GridLogic.generateGrid(), self.font)
            
            grids.append(grid)

        return grids
    
    # Button Management --------------------------------------------------------
    def _create_buttons(self):
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
        if button_name in self.callbacks:
            self.callbacks[button_name] = callback
        else:
            raise ValueError(f"Unknown button: {button_name}")

    # Heart Management --------------------------------------------------------
    def set_hearts(self, player_hearts=None, enemy_hearts=None, max_hearts=None):
        if player_hearts is not None:
            self.player_hearts = player_hearts
        if enemy_hearts is not None:
            self.enemy_hearts = enemy_hearts
        if max_hearts:
            self.max_player_hearts, self.max_enemy_hearts = max_hearts
        self._check_heart_depletion()
    
    def add_hearts(self, player=0, enemy=0):
        self.player_hearts = min(self.player_hearts + player, self.max_player_hearts)
        self.enemy_hearts = min(self.enemy_hearts + enemy, self.max_enemy_hearts)
        self._check_heart_depletion()
    
    def remove_hearts(self, player=0, enemy=0):
        self.player_hearts = max(0, self.player_hearts - player)
        self.enemy_hearts = max(0, self.enemy_hearts - enemy)
        self._check_heart_depletion()

    # Selection Management ----------------------------------------------------
    def clear_all_selections(self):
        for grid_item in self.player_grids + self.enemy_grids: 
            grid_item.clear_selection()
    
    def set_selected_cell(self, grid_index, row, col, is_player=True):
        grids = self.player_grids if is_player else self.enemy_grids
        if 0 <= grid_index < len(grids):
            grids[grid_index].set_selected_cell(row, col)

    # Heart Drawing -----------------------------------------------------------
    def draw_hearts(self, count, max_count, left=True):
        """Draw heart indicators using sprites or circles"""
        y_pos_sprite_top = 25 
        edge_padding = 30

        if self.heart_sprite_full_scaled:
            sprite_width = self.target_heart_diameter
            gap = 5
            spacing = sprite_width + gap
            total_width = (max_count * sprite_width) + (max(0, max_count - 1)) * gap
            
            start_x = edge_padding if left else self.width - edge_padding - total_width
                
            for i in range(max_count):
                x_pos = start_x + i * spacing
                if i < count:
                    self.screen.blit(self.heart_sprite_full_scaled, (x_pos, y_pos_sprite_top))
                else:
                    circle_center_x = x_pos + sprite_width // 2
                    circle_center_y = y_pos_sprite_top + sprite_width // 2
                    pygame.draw.circle(self.screen, self.colors['empty_heart'], 
                                       (circle_center_x, circle_center_y), sprite_width // 2)
        else:
            radius = 15
            spacing = 35
            y_center = 40
            for i in range(max_count):
                if left:
                    center_x = edge_padding + radius + i * spacing
                else:
                    center_x = (self.width - edge_padding - radius) - (max_count - 1 - i) * spacing
                
                color = self.colors['heart'] if i < count else self.colors['empty_heart']
                pygame.draw.circle(self.screen, color, (center_x, y_center), radius)

    def _check_heart_depletion(self):
        if self.player_hearts <= 0:
            self.callbacks['player_defeated']()
        if self.enemy_hearts <= 0:
            self.callbacks['enemy_defeated']()
    
    def set_defeat_callback(self, target, callback):
        if target == 'player':
            self.callbacks['player_defeated'] = callback
        elif target == 'enemy':
            self.callbacks['enemy_defeated'] = callback
        else:
            raise ValueError("Target must be either 'player' or 'enemy'")

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    self.callbacks[button["callback_key"]]()
            
            for grid_item in self.player_grids + self.enemy_grids:
                grid_item.handle_event(event)

    def draw(self):
        # Draw background
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((20, 20, 40))

        # Update animations
        dt = self.clock.tick(60) / 1000.0 
        for grid_item in self.player_grids + self.enemy_grids:
            grid_item.update_glow_animation(dt)
        
        # Draw hearts
        self.draw_hearts(self.player_hearts, self.max_player_hearts, left=True)
        self.draw_hearts(self.enemy_hearts, self.max_enemy_hearts, left=False)
        
        # Draw grids
        for grid_item in self.player_grids + self.enemy_grids:
            grid_item.draw(self.screen, self.font)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            color = self.colors['button_hover' if is_hover else 'button']
            
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, (100, 100, 100), button["rect"], 2)
            
            text_surf = self.font.render(button["text"], True, self.colors['text'])
            self.screen.blit(text_surf, text_surf.get_rect(center=button["rect"].center))