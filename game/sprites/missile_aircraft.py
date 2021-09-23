import pygame

from game.sprites.explode import Explode
from game.constants import *


class MissileAircraft(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (-MISSILE_AIRCRAFT_WIDTH, pos)
        self.explode = None
        self.t = 0

    def update(self, t):
        if not self.explode:
            self.t += t
            if self.t >= LASERREMAINTIME:
                self.rect.left += MISSILE_AIRCRAFT_VELOCITY * t
            if self.rect.left >= SCREEN_WIDTH:
                self.kill()
        elif not self.explode.update(t):
            self.kill()

    def player_hit(self, player) -> None:  # should be called when collided by player
        if not self.explode:
            self.image = None
            self.explode = Explode(self.rect.center)
            player.hit()

    def draw(self, window):
        if self.image:
            window.blit(self.image, self.rect)
        elif self.explode and self.explode.image:
            window.blit(self.explode.image, self.explode.rect)

