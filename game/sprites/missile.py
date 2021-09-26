import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.explode import Explode


class Missile(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, dir: float) -> None:
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.original_image = assets_manager.images['missile']
        self.image = assets_manager.images['missile']
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.dir = dir

        self.explode = None

    def update(self, t: float) -> None:
        if not self.explode:
            self.pos += (
                MISSILE_SPEED * t * np.cos(self.dir), -MISSILE_SPEED * t * np.sin(self.dir)
            )
            self.image = pygame.transform.rotate(
                assets_manager.images['missile'], self.dir * 360 // (2 * np.pi)
            )
            self.rect.center = self.pos
            if not self.in_bounds():
                self.kill()
        elif not self.explode.update(t):
            self.kill()

    def in_bounds(self) -> bool:
        return (
            self.rect.right > 0 and self.rect.left < SCREEN_WIDTH and self.rect.bottom > 0
            and self.rect.top < SCREEN_HEIGHT
        )

    def draw(self, window: pygame.Surface) -> None:
        if self.image:
            window.blit(self.image, self.rect)
        elif self.explode and self.explode.image:
            window.blit(self.explode.image, self.explode.rect)

    def hit(self):
        if not self.explode:
            self.image = None
            self.explode = Explode(self.rect.center)
            assets_manager.play_sound("explosion")
