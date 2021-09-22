import pygame

from game.constants import *
from game.sprites.explode import Explode

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, v: float) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity = v

        self.explode = None

    def update(self, t) -> None:
        if not self.explode:
            self.rect.left += self.velocity * t
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.kill()
        else:
            if not self.explode.update(t):
                self.kill()

    def player_hit(self, player) -> None:  # should be called when collided by player
        if not self.explode:
            self.explode = Explode(self.rect.center)
