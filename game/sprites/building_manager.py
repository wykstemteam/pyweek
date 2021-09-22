from collections import deque

import pygame.sprite

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Building


class BuildingManager:
    def __init__(self):
        if DISABLE_BUILDINGS:
            return

        self.buildings = deque()
        self.xs = deque()
        self.xs.append(SCREEN_WIDTH // 2 - BUILDING_WIDTH // 2)
        self.buildings.append(Building(assets_manager.images['3buildings'], self.xs[0]))
        while self.xs[0] + (1 - BUILDING_RATIO) * BUILDING_WIDTH / 2 + self.buildings[0].sx > 0:
            self.xs.appendleft(self.xs[0] - BUILDING_WIDTH)
            self.buildings.appendleft(Building(assets_manager.images['3buildings'], self.xs[0]))
        while self.xs[-1] + BUILDING_WIDTH + self.buildings[-1].sx < SCREEN_WIDTH:
            self.xs.append(self.xs[-1] + BUILDING_WIDTH)
            self.buildings.append(Building(assets_manager.images['3buildings'], self.xs[-1]))
        self.xs.append(self.xs[-1] + BUILDING_WIDTH)
        self.buildings.append(Building(assets_manager.images['3buildings'], self.xs[-1]))

    def update(self, t: float):
        if DISABLE_BUILDINGS:
            return

        dx = BACKGROUND_VELOCITY * t / BUILDING_RATIO
        for i in range(len(self.xs)):
            self.xs[i] += dx
            self.buildings[i].update(self.xs[i])

        if self.xs[0] + self.buildings[0].sx + BUILDING_WIDTH < 0:
            self.xs.popleft()
            self.xs.append(self.xs[-1] + BUILDING_WIDTH)

    def draw(self, window: pygame.Surface):
        if DISABLE_BUILDINGS:
            return
        for i in range(len(self.xs)):
            window.blit(self.buildings[i].image, self.buildings[i].rect)
