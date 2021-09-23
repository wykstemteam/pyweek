import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *


class Bomber(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.animation = assets_manager.animations['bomber']
        self.frame = 0

        self.image = self.animation[0]
        self.shadow = self.image.copy()
        alpha = 128
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

        self.x = -400

        self.rect = self.animation[0].get_rect()
        self.rect.topleft = (self.x, (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2))
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.topleft = self.shadow_rect.topleft + pygame.Vector2(-15, 15)

        self.dir = 0.0

    def go_in(self):
        if self.x < -100:
            self.x += 1

    def go_out(self):
        if self.x > -400:
            self.x -= 1

    def update(self, t, shop: bool):
        if shop:
            self.rect.right = max(0, self.rect.right - 20 * t)
            self.shadow_rect = self.rect.copy()
            self.shadow_rect.topleft = self.shadow_rect.topleft + pygame.Vector2(-5, 5)
            return
        if self.frame < len(self.animation):
            self.image = self.animation[self.frame]
            self.rect = self.animation[self.frame].get_rect()
            self.rect.topleft = (self.x, (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2))
            self.shadow_rect = self.rect.copy()
            self.shadow_rect.topleft = self.shadow_rect.topleft + pygame.Vector2(-15, 15)
            self.frame += 1
        else:
            self.frame = 0

    def aim(self, px, py):
        self.dir = np.arctan2(self.rect.centery - py, px - self.rect.centerx)

    def draw(self, window):
        window.blit(self.shadow, self.shadow_rect)
        window.blit(self.image, self.rect)
