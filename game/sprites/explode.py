import pygame

from game.constants import *
from game.assets_manager import assets_manager

class Explode(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()

        self.animation = assets_manager.animations['explode']
        self.image = self.animation[0]
        self.rect = self.animation[0].get_rect()
        self.rect.center = pos

    def update(self, t) -> bool:
        if self.animation[0]:
            self.image = self.animation[0]
            self.rect = self.animation[0].get_rect()
            self.animation.pop(0)
            return True
        return False

    def draw(self, window):
        window.blit(self.image, self.rect)