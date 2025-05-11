import pygame
import random

class Shop:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.should_quit = False
        
        # Player state
        self.player_gold = 100
        self.player_inventory = []
        
        # Shop configuration
        self.colors = {
            'dark_brown': (54, 36, 24),
            'light_brown': (101, 67, 33),
            'gray': (80, 80, 80),
            'dark_red': (120, 20, 20),
            'gold': (212, 175, 55),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'torch_yellow': (230, 180, 50)
        }
        
        self.items = [
            {"name": "Rusty Sword", "price": 15, "description": "Barely sharp, but better than nothing."},
            {"name": "Leather Armor", "price": 25, "description": "Offers minimal protection from the horrors."},
            {"name": "Health Potion", "price": 10, "description": "Heals wounds, tastes terrible."},
            {"name": "Torch", "price": 5, "description": "Keeps the darkness at bay... for a while."},
            {"name": "Silver Dagger", "price": 35, "description": "Effective against the undead."},
            {"name": "Scroll of Escape", "price": 50, "description": "Your last hope when all else fails."}
        ]
        
        self.selected_item = 0
        self.item_icons = self._create_icons()
        self.current_dialogue = random.choice(self.shopkeeper_dialogues)
        self.dialogue_timer = 0
        self.torch_intensity = 100
        self.torch_direction = -1
        
        # Fonts
        self.pixel_font = pygame.font.SysFont("monospace", 20)
        self.title_font = pygame.font.SysFont("monospace", 32)
        self.title_font.set_bold(True)

        # Start the shop loop immediately
        self._run()

    @property
    def shopkeeper_dialogues(self):
        return [
            "Welcome to my humble shop, traveler...",
            "Don't touch anything unless you're buying it!",
            "The dungeon grows more dangerous by the day...",
            "I don't offer refunds. Ever.",
            "Many enter the dungeon, few return...",
            "These items might save your life, if you're lucky."
        ]

    def _create_icons(self):
        return [self._create_icon(c) for c in [
            self.colors['dark_red'],
            self.colors['light_brown'],
            (200, 0, 0),
            self.colors['torch_yellow'],
            (192, 192, 192),
            (100, 100, 255)
        ]]

    def _create_icon(self, color):
        icon = pygame.Surface((48, 48))
        icon.fill(self.colors['black'])
        pixel_size = 6
        for y in range(0, 48, pixel_size):
            for x in range(0, 48, pixel_size):
                if random.random() > 0.5:
                    pygame.draw.rect(icon, color, (x, y, pixel_size, pixel_size))
                else:
                    darkened = (color[0]//2, color[1]//2, color[2]//2)
                    pygame.draw.rect(icon, darkened, (x, y, pixel_size, pixel_size))
        pygame.draw.rect(icon, self.colors['light_brown'], (0, 0, 48, 48), 2)
        return icon

    def _run(self):
        clock = pygame.time.Clock()
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            pygame.display.flip()
            clock.tick(60)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.should_quit = True
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_UP:
            self.selected_item = (self.selected_item - 1) % len(self.items)
            self._update_dialogue()
        elif event.key == pygame.K_DOWN:
            self.selected_item = (self.selected_item + 1) % len(self.items)
            self._update_dialogue()
        elif event.key == pygame.K_RETURN:
            self._handle_purchase()

    def _update_dialogue(self):
        item = self.items[self.selected_item]
        self.current_dialogue = f"Ah, the {item['name']}. {item['description']}"
        self.dialogue_timer = 0

    def _handle_purchase(self):
        item = self.items[self.selected_item]
        if self.player_gold >= item['price']:
            self.player_gold -= item['price']
            self.player_inventory.append(item['name'])
            self.current_dialogue = f"The {item['name']} is yours. Use it wisely..."
        else:
            self.current_dialogue = "You don't have enough gold, beggar!"
        self.dialogue_timer = 0

    def _update(self):
        self._update_torch()
        self._update_dialogue_timer()

    def _update_torch(self):
        self.torch_intensity += self.torch_direction * random.uniform(0.5, 1.5)
        self.torch_intensity = max(70, min(100, self.torch_intensity))
        self.torch_direction = 1 if self.torch_intensity <= 70 else -1 if self.torch_intensity >= 100 else self.torch_direction

    def _update_dialogue_timer(self):
        self.dialogue_timer += 1
        if self.dialogue_timer > 300:
            self.dialogue_timer = 0
            self.current_dialogue = random.choice(self.shopkeeper_dialogues)

    def _render(self):
        self.screen.fill(self.colors['dark_brown'])
        self._draw_shop_frame()
        self._draw_torches()
        self._draw_title()
        self._draw_dialogue()
        self._draw_items()
        self._draw_player_info()
        self._draw_controls()

    def _draw_shop_frame(self):
        pygame.draw.rect(self.screen, self.colors['black'], (50, 50, 700, 500))
        pygame.draw.rect(self.screen, self.colors['light_brown'], (50, 50, 700, 500), 4)

    def _draw_torches(self):
        torch_color = (
            min(255, int(self.colors['torch_yellow'][0] * self.torch_intensity / 100)),
            min(255, int(self.colors['torch_yellow'][1] * self.torch_intensity / 100)),
            min(255, int(self.colors['torch_yellow'][2] * self.torch_intensity / 100))
        )
        pygame.draw.circle(self.screen, torch_color, (70, 70), 15)
        pygame.draw.circle(self.screen, torch_color, (730, 70), 15)

    def _draw_title(self):
        title = self.title_font.render("DUNGEON MERCHANT", True, self.colors['gold'])
        self.screen.blit(title, (400 - title.get_width() // 2, 70))

    def _draw_dialogue(self):
        pygame.draw.rect(self.screen, self.colors['black'], (100, 120, 600, 60))
        pygame.draw.rect(self.screen, self.colors['light_brown'], (100, 120, 600, 60), 2)
        text = self.pixel_font.render(self.current_dialogue, True, self.colors['white'])
        self.screen.blit(text, (110, 140))

    def _draw_items(self):
        for i, item in enumerate(self.items):
            y = 200 + i * 60
            rect = pygame.Rect(100, y, 600, 50)
            color = self.colors['dark_red'] if i == self.selected_item else self.colors['black']
            border = self.colors['gold'] if i == self.selected_item else self.colors['light_brown']
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, border, rect, 2)
            self.screen.blit(self.item_icons[i], (110, y + 1))
            
            name = self.pixel_font.render(item['name'], True, self.colors['white'])
            price = self.pixel_font.render(f"{item['price']} gold", True, self.colors['gold'])
            self.screen.blit(name, (170, y + 15))
            self.screen.blit(price, (650 - price.get_width(), y + 15))

    def _draw_player_info(self):
        pygame.draw.rect(self.screen, self.colors['black'], (100, 500, 600, 50))
        pygame.draw.rect(self.screen, self.colors['light_brown'], (100, 500, 600, 50), 2)
        
        gold_text = self.pixel_font.render(f"Gold: {self.player_gold}", True, self.colors['gold'])
        inv_text = self.pixel_font.render(f"Inventory: {', '.join(self.player_inventory) or 'Empty'}", True, self.colors['white'])
        
        self.screen.blit(gold_text, (120, 515))
        self.screen.blit(inv_text, (250, 515))

    def _draw_controls(self):
        text = self.pixel_font.render("UP/DOWN: Select   ENTER: Buy   ESC: Exit", True, self.colors['gray'])
        self.screen.blit(text, (400 - text.get_width() // 2, 570))