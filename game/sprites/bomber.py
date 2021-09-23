import pygame

from game.assets_manager import assets_manager
from game.constants import *


class Bomber(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.animation = assets_manager.animations['bomber']
        self.image = self.animation[0]
        self.rect = self.animation[0].get_rect()
        self.shadow = assets_manager.images['bomber_shadow']
        self.shadow_rect = self.shadow.get_rect()
        self.rect.topleft = (0, (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2))
        self.shadow_rect.topleft = (-15, (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2))
        self.frame = 0

    def update(self, t):
        if self.frame < len(self.animation):
            self.image = self.animation[self.frame]
            self.rect = self.animation[self.frame].get_rect()
            self.rect.topleft = (0, (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2))
            self.shadow_rect.topleft = (-15, (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2))
            self.frame += 1
        else:
            self.frame = 0

    def draw(self, window):
        window.blit(self.shadow, self.shadow_rect)
        window.blit(self.image, self.rect)
