import pygame

from game.constants import *
from game.sprites.explode import Explode
from game.sprites.player import Player


class MissileAircraft(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: int) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (-MISSILE_AIRCRAFT_WIDTH, pos)
        self.explode = None
        self.t = 0.0

    def update(self, t: float) -> None:
        if not self.explode:
            self.t += t
            if self.t >= LASERREMAINTIME:
                self.rect.left += MISSILE_AIRCRAFT_VELOCITY * t
            if self.rect.left >= SCREEN_WIDTH:
                self.kill()
        elif not self.explode.update(t):
            self.kill()

    def player_hit(self, player: Player) -> None:  # should be called when collided by player
        if not self.explode and player.hit():
            self.image = None
            self.explode = Explode(self.rect.center)

    def draw(self, window: pygame.Surface) -> None:
        if self.image:
            window.blit(self.image, self.rect)
        elif self.explode and self.explode.image:
            window.blit(self.explode.image, self.explode.rect)
