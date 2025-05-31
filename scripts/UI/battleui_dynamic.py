import pygame
import pygame.font
# import os # os is imported but not used in the provided snippet
from scripts.Grid import Grid, GridLogic # Assuming this path is correct


class BattleScreen:
    """Battle screen UI component with configurable callbacks and heart management.
    (Omitted rest of the docstring for brevity)
    """
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        
        self.colors = {
            'background': (20, 20, 40),
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

        # --- MODIFICATION: Define target heart size and load/scale sprite ---
        self.target_heart_diameter = 30  # Original circle diameter (radius 15 * 2)
        self.heart_sprite_full_scaled = None # Will store the scaled sprite

        try:
            # Load the original full heart sprite
            original_heart_sprite = pygame.image.load("Media/cell/Heart.png").convert_alpha()
            # Scale it to the target diameter
            self.heart_sprite_full_scaled = pygame.transform.scale(
                original_heart_sprite,
                (self.target_heart_diameter, self.target_heart_diameter)
            )
            # Optional: If you have an empty heart sprite, load and scale it here similarly:
            # original_empty_heart_sprite = pygame.image.load("Media/cell/EmptyHeart.png").convert_alpha()
            # self.heart_sprite_empty_scaled = pygame.transform.scale(
            #     original_empty_heart_sprite,
            #     (self.target_heart_diameter, self.target_heart_diameter)
            # )
        except pygame.error as e:
            print(f"Warning: Could not load or scale heart sprite 'Media/cell/Heart.png': {e}. Hearts will be drawn as circles.")
            self.heart_sprite_full_scaled = None
        # --- END OF MODIFICATION ---
        
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

    # (Keep _create_grids, _create_buttons, set_callback, and other heart/selection management methods as they are)
    # ... previous methods ...
    # Grid Creation ------------------------------------------------------------
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
            
            if i == 0 and not left:  # Enemy side, first grid
                try:
                    skeletonImg = pygame.image.load('Media/enemy/Dragon.png').convert_alpha()
                    grid.fill_cell_with_image(0, 0, skeletonImg, lambda: grid.set_selected_cell(0, 0))
                except pygame.error as e:
                    print(f"Could not load skeleton image: {e}")
                    grid.fill_cell(0, 0, "SKEL", self.font, lambda: grid.set_selected_cell(0, 0))
            elif i == 0 and left:  # Player side, first grid
                grid.fill_cell(0, 0, "HERO", self.font, lambda: grid.set_selected_cell(0, 0))
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

    # --- MODIFIED DRAW_HEARTS METHOD ---
    def draw_hearts(self, count, max_count, left=True):
        """Draw heart indicators showing current/max health.
        Uses scaled sprites if available, otherwise falls back to circles.
        """
        # Y position for the top of the heart sprites (original circle top was 40-15=25)
        y_pos_sprite_top = 25 
        edge_padding = 30      # Padding from the screen edges

        if self.heart_sprite_full_scaled: # Check if the SCALED sprite is available
            # Use scaled sprites for hearts
            sprite_width = self.target_heart_diameter # Width of the scaled sprite
            sprite_height = self.target_heart_diameter # Height of the scaled sprite
            
            gap_between_sprites = 5  # Gap between each heart sprite
            spacing_per_heart = sprite_width + gap_between_sprites 

            total_hearts_display_width = (max_count * sprite_width) + (max(0, max_count - 1) * gap_between_sprites)
            
            current_x_start: int
            if left:
                current_x_start = edge_padding
            else:
                current_x_start = self.width - edge_padding - total_hearts_display_width
                
            for i in range(max_count):
                x_pos_for_this_heart = current_x_start + i * spacing_per_heart
                
                if i < count:  # This is a "full" heart
                    self.screen.blit(self.heart_sprite_full_scaled, (x_pos_for_this_heart, y_pos_sprite_top))
                else:  # This is an "empty" heart slot
                    # Fallback: Draw a grey circle, sized like the original dots
                    # Position the circle centered where the sprite would be
                    circle_center_x = x_pos_for_this_heart + sprite_width // 2
                    circle_center_y = y_pos_sprite_top + sprite_height // 2 # Should be 40
                    original_radius = self.target_heart_diameter // 2 # Should be 15
                    pygame.draw.circle(self.screen, self.colors['empty_heart'], 
                                       (circle_center_x, circle_center_y), original_radius)
        else:
            # Fallback: Draw circles if heart_sprite_full_scaled couldn't be created (original method)
            original_radius = 15 # This is the target radius
            original_spacing_between_centers = 35 
            original_y_center = 40 # Y position for the center of the circles

            for i in range(max_count):
                center_x: int
                if left:
                    center_x = edge_padding + original_radius + i * original_spacing_between_centers
                else:
                    center_x = (self.width - edge_padding - original_radius) - \
                               (max_count - 1 - i) * original_spacing_between_centers
                
                color = self.colors['heart'] if i < count else self.colors['empty_heart']
                pygame.draw.circle(self.screen, color, (center_x, original_y_center), original_radius)
    # --- END OF MODIFICATION ---

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
        dt = self.clock.tick(60) / 1000.0 
        for grid_item in self.player_grids + self.enemy_grids:
            grid_item.update_glow_animation(dt)
        
        panel_widths = [self.width * 0.35, self.width * 0.3, self.width * 0.35]
        for i, w in enumerate(panel_widths):
            x = sum(panel_widths[:i])
            pygame.draw.rect(self.screen, self.colors['panel'], (x, 0, w, self.height))
        
        self.draw_hearts(self.player_hearts, self.max_player_hearts, left=True)
        self.draw_hearts(self.enemy_hearts, self.max_enemy_hearts, left=False)
        
        for grid_item in self.player_grids + self.enemy_grids:
            grid_item.draw(self.screen, self.font)
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            color = self.colors['button_hover' if is_hover else 'button']
            
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, (100, 100, 100), button["rect"], 2)
            
            text_surf = self.font.render(button["text"], True, self.colors['text'])
            self.screen.blit(text_surf, text_surf.get_rect(center=button["rect"].center))