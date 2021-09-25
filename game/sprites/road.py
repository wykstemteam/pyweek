import pygame

from game.constants import *


class Road(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, BUILDING_HEIGHT)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x

        self.stop_moving = False

    def update(self, t):
        if self.stop_moving:
            return
        self.x += BACKGROUND_VELOCITY * t
        self.rect.left = int(self.x)
        if self.rect.right <= 0:
            self.x += 2 * SCREEN_WIDTH
