import pygame

from game.constants import *


class Shield(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: float, y: float):
        super().__init__()

        self.image = image
        self.topleft = (x, y)
        self.rect = self.image.get_rect()
        self.shield_time = SHIELD_REMAIN_TIME
        self.activate = True

    def update(self, t: float, x: float, y: float):
        if self.shield_time > 0:
            self.shield_time -= t
            self.topleft = (x, y)
        else:
            self.activate = False

    def turn_on(self):
        return self.activate

    def draw(self, window):
        window.image(self.image, self.rect)

