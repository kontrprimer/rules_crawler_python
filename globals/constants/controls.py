import pygame
import numpy as np


class Controls:
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    QUIT = pygame.K_ESCAPE
    SPACE = pygame.K_SPACE
    RESET = pygame.K_r
    REVERT = pygame.K_z

    ALL_KEYS = [
        UP,
        DOWN,
        LEFT,
        RIGHT,
        QUIT,
        SPACE,
        RESET,
        REVERT
    ]


KEY_DIRECTIONS = {
    Controls.UP: np.array([0, -1]),
    Controls.DOWN: np.array([0, 1]),
    Controls.LEFT: np.array([-1, 0]),
    Controls.RIGHT: np.array([1, 0])
}
