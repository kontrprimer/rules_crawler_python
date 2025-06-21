import pygame
import sys

from globals.constants.colours import BLACK
from globals.constants.controls import Controls
from globals.constants.sizes import SCREEN_WIDTH, SCREEN_HEIGHT

from assets.levels import TestLevel


def main():
    state = TestLevel()

    clock, screen = initialise()

    while True:
        # Event handling
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            pygame.quit()
            sys.exit()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == Controls.RESET:
                    state = TestLevel()
        state.update()

        # Drawing
        screen.fill(BLACK)  # Clear the screen
        state.draw(screen)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)


def initialise():
    # Initialize pygame
    pygame.init()
    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple 32x18 Grid Game")
    # Game loop
    clock = pygame.time.Clock()
    return clock, screen


if __name__ == "__main__":
    main()
