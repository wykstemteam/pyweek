
import pygame

from game.constants import *


class MissileAircraft(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: int):
        super().__init__()

        self.image = image
        self.rect.topleft = (0, pos)
        self.rect = self.image.get_rect()

    def update(self, t):
        self.rect.left += MISSILE_AIRCRAFT_VELOCITY * t

        if self.rect.left >= SCREEN_WIDTH:
            self.kill()

    def draw(self, window):
        window.blit(self.image, self.rect)
