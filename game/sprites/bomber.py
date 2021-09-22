import pygame

from game.assets_manager import assets_manager
from game.constants import *


class Bomber(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.animation = assets_manager.animations['bomber']
        self.image = self.animation[0]
        self.rect = self.animation[0].get_rect()
        self.rect.topleft = (400, 400)
        self.frame = 0

    def update(self, t):
        if self.frame < len(self.animation):
            self.image = self.animation[self.frame]
            self.rect = self.animation[self.frame].get_rect()
            self.frame += 1
        else:
            self.frame = 0

    def draw(self, window):
        window.blit(self.image, self.rect)
