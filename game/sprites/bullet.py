import pygame

from game.constants import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, v: float) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity = v

    def update(self, t) -> None:
        self.rect.left += self.velocity * t
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.kill()

    def player_hit(self, player) -> None:  # should be called when collided by player
        # animation
        #
        pass
