import pygame
import sys

from globals.constants.colours import BLACK
from globals.constants.controls import Controls
from globals.constants.sizes import SCREEN_WIDTH, SCREEN_HEIGHT

from assets.levels import TestLevel

LEVEL = TestLevel()

# Initialize pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple 32x18 Grid Game")

# Game loop
clock = pygame.time.Clock()


while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == Controls.RESET:
                LEVEL = TestLevel()
    LEVEL.update()

    # Drawing
    screen.fill(BLACK)  # Clear the screen
    LEVEL.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
