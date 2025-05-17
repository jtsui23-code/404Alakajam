import pygame
from scripts.UI.room import Room
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))

# Initialize room and fill content
Room.initialize(screen)  # Must be called first

# Run the room screen
Room.running = True
while Room.running:
    for event in pygame.event.get():
        Room.update(event)
    
    Room.draw(screen)
    pygame.display.flip()