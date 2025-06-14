from globals.constants.controls import Controls, KEY_DIRECTIONS
from globals.constants.sizes import GRID_WIDTH, GRID_HEIGHT
from globals.helpers.caching import cache_method
from assets.models import Player, ModelBase, Wall, Box, Tile, TextIs, TextBox, TextPlayer, TextTimeless
import pygame
from time import time
from copy import deepcopy
from typing import Tuple, Dict, List


class TestLevel:

    def __init__(self):
        self.content = [
            Player(14, 14),
            Wall(10, 10),
            Box(5, 5),
            Tile(5, 10),
            TextIs(15, 10),
            TextBox(15, 9),
            TextPlayer(15, 12),
            TextTimeless(15, 14)
        ]
        self.MAX_CACHE_SIZE = 2 ** 10
        self.cache = []
        self.key_hold_time = {}
        self.move_delay = 0.5  # Delay before smooth movement in seconds

    @property
    def snapshot(self):
        return deepcopy([(type(model), model.pos, model.color) for model in self.content])

    def restore(self, snapshot):
        timeless_content = [model for model in self.content if model.is_timeless]
        restored_content = [model(pos[0], pos[1], color) for model, pos, color in snapshot if not model.is_timeless]
        self.content = timeless_content + restored_content

    @property
    def map(self) -> Dict[Tuple, List[ModelBase]]:
        mapping = {}
        for model in self.content:
            mapping[tuple(model.pos)] = mapping.get(tuple(model.pos), []) + [model]
        return mapping

    def extract_rules_from_a_list(self, list_of_objects: List[List[ModelBase]]) -> list:
        rules_in_a_list = []
        # Find "A is B" rules
        for i in range(1, len(list_of_objects)-1):
            current_object = list_of_objects[i]
            if not any(isinstance(x, TextIs) for x in current_object):
                continue
            starters = []
            for initial_object in list_of_objects[i-1]:
                if initial_object.linked_model is not None:
                    starters.append(initial_object)
            finishers = []
            for final_object in list_of_objects[i+1]:
                if final_object.is_text:
                    finishers.append(final_object)

            for s in starters:
                for f in finishers:
                    if f.linked_model is not None:
                        rules_in_a_list.append(self.create_is_rule(s.linked_model, f.linked_model))
                    if isinstance(f, TextTimeless):
                        rules_in_a_list.append(self.create_is_property(s.linked_model, f))

        return rules_in_a_list

    @staticmethod
    def create_is_rule(start: type, finish: type):

        def is_rule(model: ModelBase) -> ModelBase:
            if isinstance(model, start):
                return finish(*model.pos)
            return model
        return is_rule

    @staticmethod
    def create_is_property(start: type, finish: ModelBase):

        def timeless_rule(model) -> ModelBase:
            if isinstance(model, start):
                type(model).is_timeless = True
            return model

        if isinstance(finish, TextTimeless):
            return timeless_rule
        else:
            raise TypeError(f"Unknown model property type: {finish}.")

    def get_rules(self):
        all_rules = []
        for row in range(GRID_HEIGHT):
            all_rules += self.extract_rules_from_a_list([self.map.get((col, row), []) for col in range(GRID_WIDTH)])
        for col in range(GRID_WIDTH):
            all_rules += self.extract_rules_from_a_list([self.map.get((col, row), []) for row in range(GRID_HEIGHT)])
        return all_rules

    def apply_rules(self, rules):
        for model in self.content:
            type(model).is_timeless = False
        for rule in rules:
            self.content = [rule(model) for model in self.content]


    @staticmethod
    def valid_pos(pos: Tuple[int, int]) -> bool:
        return 0 <= pos[0] < GRID_WIDTH and 0 <= pos[1] < GRID_HEIGHT

    @cache_method
    def try_move(self, model: ModelBase, direction: Tuple[int, int]) -> Tuple[bool, List[ModelBase]]:
        new_pos = model.pos + direction
        if not self.valid_pos(new_pos):
            return False, [model]
        if model.is_move or model.is_push:
            if tuple(new_pos) not in self.map:
                return True, [model]
            next_success, next_list = True, []
            for m in self.map[tuple(new_pos)]:
                next_success_partial, next_list_partial = self.try_move(m, direction)
                next_success = next_success and next_success_partial
                next_list = list(set(next_list + next_list_partial))
            return next_success, next_list + [model]
        if model.is_block:
            return False, []
        return True, []

    def moveable_models(self, direction: Tuple[int, int]) -> List[ModelBase]:
        self.try_move.clear_cache(self)
        all_models_to_move = set()
        for model in self.content:
            if not model.is_move:
                continue
            success, moved_list = self.try_move(model, direction)
            if not success:
                continue
            all_models_to_move.update(moved_list)
        self.try_move.clear_cache(self)
        return list(all_models_to_move)

    def update(self):
        self.perform_action()
        self.apply_rules(self.get_rules())

    def perform_action(self):
        keys = pygame.key.get_pressed()
        current_time = self.update_key_hold_time(keys)
        if len(self.key_hold_time) == 0:
            return
        last_pressed_key = max(self.key_hold_time, key=self.key_hold_time.get)
        if 0 < current_time - self.key_hold_time[last_pressed_key] < self.move_delay:
            return
        if last_pressed_key == Controls.REVERT:
            if len(self.cache) == 0:
                return
            self.restore(self.cache.pop(-1))
            return
        if len(self.cache) >= self.MAX_CACHE_SIZE:
            self.cache = self.cache[self.MAX_CACHE_SIZE // 2:]
        self.cache.append(self.snapshot)
        if last_pressed_key in KEY_DIRECTIONS:
            direction = KEY_DIRECTIONS[last_pressed_key]
            for model in self.moveable_models(direction):
                model.pos += direction

    def update_key_hold_time(self, keys):
        current_time = time()
        for key in Controls.ALL_KEYS:
            if keys[key]:
                if key not in self.key_hold_time:
                    self.key_hold_time[key] = current_time
            else:
                self.key_hold_time.pop(key, None)
        return current_time

    def draw(self, screen):
        for model in self.content:
            model.draw(screen)
