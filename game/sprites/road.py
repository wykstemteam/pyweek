import pygame

from game.constants import *


class Road(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, t):
        self.rect.left += int(BACKGROUND_VELOCITY * t)
        if self.rect.right <= 0:
            self.rect.left += 2*SCREEN_WIDTH
        
