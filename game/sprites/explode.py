import pygame

from game.constants import *
from game.assets_manager import assets_manager

class Explode(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()

        self.animation = assets_manager.animations['explode']
        self.image = self.animation[0]
        self.rect = self.animation[0].get_rect()
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos
        self.explode_frame = 0

    def update(self, t) -> bool:
        if self.explode_frame < len(self.animation):
            self.image = self.animation[self.explode_frame]
            self.rect = self.animation[self.explode_frame].get_rect()
            self.rect.center = self.pos
            self.explode_frame += 1
            return True
        return False

    def draw(self, window):
        window.blit(self.image, self.rect)