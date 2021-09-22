import pygame.sprite

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Building


class BuildingManager:
    def __init__(self):
        if DISABLE_BUILDINGS:
            return
        assets_manager.images['buildings'] = pygame.transform.scale(assets_manager.images['buildings'],
                                                                    (BUILDING_WIDTH, BUILDING_HEIGHT))
        self.left = Building(assets_manager.images['buildings'], SCREEN_WIDTH // 2 - BUILDING_WIDTH // 2)
        self.right = Building(assets_manager.images['buildings'], SCREEN_WIDTH // 2 + BUILDING_WIDTH // 2)
        self.buildings = pygame.sprite.Group(self.left, self.right)

    def update(self, t: float):
        if DISABLE_BUILDINGS:
            return
        dx = BACKGROUND_VELOCITY * t
        self.buildings.update(int(dx / BUILDING_RATIO))
        if self.left.rect.left + self.left.sx + BUILDING_WIDTH * (1 + BUILDING_RATIO) / 2 < 0:
            self.buildings.remove(self.left)
            self.left = self.right
            self.right = Building(assets_manager.images['buildings'], self.left.rect.right)
            self.buildings.add(self.right)

    def draw(self, surface: pygame.Surface):
        if DISABLE_BUILDINGS:
            return
        self.buildings.draw(surface)
