
import pygame

from game.constants import *


class MissileAircraft(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (-MISSILE_AIRCRAFT_WIDTH, pos)
        self.t = 0

    def update(self, t):
        self.t += t
        if self.t >= LASERREMAINTIME:
            self.rect.left += MISSILE_AIRCRAFT_VELOCITY * t
        if self.rect.left >= SCREEN_WIDTH:
            self.kill()

    def draw(self, window):
        window.blit(self.image, self.rect)
