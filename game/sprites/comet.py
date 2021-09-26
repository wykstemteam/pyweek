import numpy as np
import random

import pygame

from game.assets_manager import assets_manager
from game.constants import *


class Comet(pygame.sprite.Sprite):
    def __init__(self, player_collision_group: pygame.sprite.Group) -> None:
        super().__init__()
        self.dir = random.uniform(-np.pi, np.pi)
        self.x = random.uniform(0.0, float(SCREEN_WIDTH))
        self.y = random.uniform(0.0, float(SCREEN_HEIGHT))
        self.x += 3000 * -np.cos(self.dir)
        self.y += 3000 * -np.sin(self.dir)

        self.image = pygame.transform.rotate(assets_manager.images['comet'], ((np.pi - self.dir) * 360) / (2*np.pi))
        self.rect = self.image.get_rect(
            center=self.image.get_rect(center=(self.x, self.y)).center
        )
        self.hitbox = pygame.Rect((self.x - 15 + 70 * np.cos(self.dir), self.y - 15 + 70 * np.sin(self.dir)), (30, 30))
        self.remaining_time = 30.0

    def update(self, t: float, difficulty) -> None:
        self.x += t * np.cos(self.dir) * 200 * min(5, difficulty)
        self.y += t * np.sin(self.dir) * 200 * min(5, difficulty)
        self.hitbox = pygame.Rect((self.x - 15 + 70 * np.cos(self.dir), self.y - 15 + 70 * np.sin(self.dir)), (30, 30))
        self.image = pygame.transform.rotate(assets_manager.images['comet'], ((np.pi - self.dir) * 360) / (2*np.pi))
        self.rect = self.image.get_rect(
            center=self.image.get_rect(center=(self.x, self.y)).center
        )
        self.remaining_time -= t

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, (255, 255, 255), self.hitbox)
