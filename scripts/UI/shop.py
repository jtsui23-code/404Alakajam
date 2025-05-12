# shop.py - Contains only the Shop class definition with a clean interface

class Shop:
    # Static variables to track UI elements
    _is_rendered = False
    _elements = []
    _selected_item = 0
    _items = [
        {"name": "Rusty Sword", "price": 5, "description": "A worn blade that has seen better days."},
        {"name": "Health Potion", "price": 10, "description": "Restores a small amount of health."},
        {"name": "Torch", "price": 3, "description": "Provides light in dark dungeons."},
        {"name": "Chain Mail", "price": 25, "description": "Offers decent protection against attacks."},
        {"name": "Magic Scroll", "price": 30, "description": "Contains a random spell."}
    ]
    
    @staticmethod
    def render(screen):
        """Render the shop UI to the provided screen"""
        import pygame
        
        # Clear previous elements
        Shop._elements = []
        
        # Get screen dimensions
        width, height = screen.get_size()
        
        # Define colors with a medieval/dungeon theme
        BLACK = (0, 0, 0)
        DARK_GRAY = (40, 40, 40)
        GRAY = (80, 80, 80)
        LIGHT_GRAY = (160, 160, 160)
        WHITE = (220, 220, 220)
        
        BROWN_DARK = (60, 40, 20)
        BROWN = (80, 60, 40)
        BROWN_LIGHT = (120, 90, 60)
        
        RED = (120, 30, 30)
        GOLD = (180, 150, 50)
        
        # Fill the background with a solid color
        screen.fill(DARK_GRAY)
        
        # Draw a simple border around the screen
        border_width = 8
        pygame.draw.rect(screen, BLACK, (0, 0, width, height), border_width)
        
        # Draw title
        try:
            title_font = pygame.font.Font(None, 36)
            font = pygame.font.Font(None, 24)
            small_font = pygame.font.Font(None, 20)
        except:
            title_font = pygame.font.SysFont('Arial', 36)
            font = pygame.font.SysFont('Arial', 24)
            small_font = pygame.font.SysFont('Arial', 20)
        
        # Draw shop title
        title = title_font.render("DUNGEON SHOP", True, GOLD)
        screen.blit(title, (width // 2 - title.get_width() // 2, 20))
        
        # Draw subtitle
        subtitle = font.render("Buy what you need and leave", True, LIGHT_GRAY)
        screen.blit(subtitle, (width // 2 - subtitle.get_width() // 2, 60))
        
        # Draw horizontal separator
        pygame.draw.rect(screen, BROWN_DARK, (50, 90, width - 100, 4))
        pygame.draw.rect(screen, BROWN_LIGHT, (50, 91, width - 100, 1))
        
        # Draw items
        item_y = 120
        item_height = 60
        item_spacing = 10
        item_width = width - 100
        
        for i, item in enumerate(Shop._items):
            # Item background
            item_rect = pygame.Rect(50, item_y, item_width, item_height)
            
            # Draw item background
            if i == Shop._selected_item:
                pygame.draw.rect(screen, BROWN, item_rect)
                pygame.draw.rect(screen, GOLD, item_rect, 2)
            else:
                pygame.draw.rect(screen, BROWN_DARK, item_rect)
                pygame.draw.rect(screen, BROWN, item_rect, 1)
            
            # Draw selection indicator
            if i == Shop._selected_item:
                # Simple arrow indicator
                arrow_x = item_rect.x - 20
                arrow_y = item_rect.y + item_rect.height // 2
                pygame.draw.polygon(screen, GOLD, [
                    (arrow_x, arrow_y),
                    (arrow_x + 10, arrow_y - 8),
                    (arrow_x + 10, arrow_y + 8)
                ])
            
            # Draw item name
            name_text = font.render(item["name"], True, WHITE)
            screen.blit(name_text, (item_rect.x + 15, item_rect.y + 10))
            
            # Draw item description
            desc_text = small_font.render(item["description"], True, LIGHT_GRAY)
            screen.blit(desc_text, (item_rect.x + 15, item_rect.y + 35))
            
            # Draw price
            price_text = font.render(f"{item['price']} gold", True, GOLD)
            price_width = price_text.get_width()
            screen.blit(price_text, (item_rect.x + item_rect.width - price_width - 15, item_rect.y + 20))
            
            # Store the item rect for interaction
            Shop._elements.append({"type": "item", "rect": item_rect, "index": i})
            
            item_y += item_height + item_spacing
        
        # Draw bottom separator
        bottom_y = height - 50
        pygame.draw.rect(screen, BROWN_DARK, (50, bottom_y, width - 100, 4))
        pygame.draw.rect(screen, BROWN_LIGHT, (50, bottom_y + 1, width - 100, 1))
        
        # Draw instructions
        instructions = small_font.render("UP/DOWN: Select   ENTER: Buy   ESC: Exit", True, LIGHT_GRAY)
        screen.blit(instructions, (width // 2 - instructions.get_width() // 2, height - 30))
        
        # Mark as rendered
        Shop._is_rendered = True
    
    @staticmethod
    def handle_event(event):
        """Handle pygame events for the shop"""
        import pygame
        
        if not Shop._is_rendered:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Shop._selected_item = max(0, Shop._selected_item - 1)
                return True
            elif event.key == pygame.K_DOWN:
                Shop._selected_item = min(len(Shop._items) - 1, Shop._selected_item + 1)
                return True
            elif event.key == pygame.K_RETURN:
                # Buy selected item (would implement actual purchase logic here)
                selected_item = Shop._items[Shop._selected_item]
                print(f"Purchased {selected_item['name']} for {selected_item['price']} gold!")
                return True
            elif event.key == pygame.K_ESCAPE:
                # Exit shop
                Shop._is_rendered = False
                return True
                
        return False
    
    @staticmethod
    def clear(screen):
        """Clear the shop from the screen"""
        if Shop._is_rendered:
            screen.fill((0, 0, 0))  # Fill with black
            Shop._is_rendered = False
            Shop._elements = []