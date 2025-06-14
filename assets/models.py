from globals.constants.sizes import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT
from globals.constants.colours import BLACK, WHITE, RED

import pygame
import numpy as np

pygame.font.init()  # Ensure font system is initialized globally
global_font = pygame.font.SysFont(None, int(CELL_SIZE * 0.8))


class ModelBase:
    size = CELL_SIZE
    is_timeless = False
    is_move = False
    is_push = False
    is_block = False
    is_text = False
    linked_model = None
    # Initialize font with size adjusted to fit within the cell
    font = global_font
    color = WHITE

    def __init__(self, x, y, color=None):
        self._pos = np.array([x, y])
        if color is not None:
            self.color = color

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = np.clip(value, 0, np.array([GRID_WIDTH - 1, GRID_HEIGHT - 1]))

    def draw(self, screen):
        text_color = self.color if self.is_text else BLACK
        background_color = BLACK if self.is_text else self.color
        pygame.draw.rect(screen, background_color, (*(self.pos * self.size), self.size, self.size))
        # Use the class name as the text
        class_name = self.__class__.__name__.upper()
        class_name = class_name if not self.is_text else class_name[4:]
        # Render the text
        text_surface = self.font.render(class_name, True, text_color)
        # Scale text if it's too big for the cell
        text_rect = text_surface.get_rect()
        if text_rect.width > self.size or text_rect.height > self.size:
            scale_factor = min(self.size / text_rect.width, self.size / text_rect.height)
            new_size = (int(text_rect.width * scale_factor), int(text_rect.height * scale_factor))
            text_surface = pygame.transform.scale(text_surface, new_size)
            text_rect = text_surface.get_rect()
        # Center the text within the square
        text_rect.center = self.pos * self.size + (self.size // 2, self.size // 2)
        # Blit the text onto the screen
        screen.blit(text_surface, text_rect)


class Player(ModelBase):
    is_move = True
    is_push = True


class Wall(ModelBase):
    is_block = True


class Box(ModelBase):
    is_push = True


class Tile(ModelBase):
    pass


class Text(ModelBase):
    is_text = True
    is_push = True


class TextIs(Text):

    pass


class TextPlayer(Text):
    linked_model = Player


class TextBox(Text):
    linked_model = Box


class TextTimeless(Text):
    color = RED
