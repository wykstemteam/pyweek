import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *


class Missle(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, dir: float) -> None:
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.original_image = assets_manager.images['missle']
        self.image = assets_manager.images['missle']
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.dir = dir

        self.explode = None

    def update(self, t) -> None:
        self.pos += (MISSLE_SPEED * t * np.cos(self.dir), -MISSLE_SPEED * t * np.sin(self.dir))
        self.image = pygame.transform.rotate(
            assets_manager.images['missle'], self.dir * 360 // (2 * np.pi)
        )
        self.rect.center = self.pos

    # def player_hit(self, player) -> None:  # should be called when collided by player
    #     if not self.explode:
    #         self.image = None
    #         self.explode = Explode(self.rect.center)

    def draw(self, window):
        if self.image:
            window.blit(self.image, self.rect)
        elif self.explode and self.explode.image:
            window.blit(self.explode.image, self.explode.rect)
