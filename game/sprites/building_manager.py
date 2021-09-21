import pygame.sprite

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Building


class BuildingManager:
    def __init__(self):
        assets_manager.images['buildings'] = pygame.transform.scale(assets_manager.images['buildings'],
                                                                    (BUILDING_WIDTH, BUILDING_HEIGHT))
        self.left = Building(assets_manager.images['buildings'], 0.0, SCREEN_WIDTH // 2 - BUILDING_WIDTH // 2)
        self.right = Building(assets_manager.images['buildings'], -BUILDING_WIDTH * (1 - BUILDING_RATIO),
                              SCREEN_WIDTH // 2 + BUILDING_WIDTH // 2)
        self.buildings = pygame.sprite.Group(
            self.left, self.right
        )

    def update(self, t: float):
        dx = BACKGROUND_VELOCITY * t
        self.buildings.update(dx)
        if self.left.rect.left + self.left.total_sheared + BUILDING_WIDTH * (1 + BUILDING_RATIO) / 2 < 0:
            self.buildings.remove(self.left)
            self.left = self.right
            self.right = Building(
                assets_manager.images['buildings'], self.left.total_sheared - BUILDING_WIDTH * (1 - BUILDING_RATIO),
                self.left.rect.right,
            )
            self.buildings.add(self.right)

    def draw(self, surface: pygame.Surface):
        self.buildings.draw(surface)
