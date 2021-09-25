import pygame
from game.constants import *

from game.assets_manager import assets_manager

class Shield(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.image = assets_manager.images['shield']
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.shield_time = SHIELD_REMAIN_TIME
        self.activate = False

        self.shield_hp = 3

    def update(self, t: float, pos: pygame.Vector2) -> None:
        if self.activate:
            if self.shield_time > 0:
                self.shield_time -= t
                self.rect.center = pos
            else:
                self.activate = False

    def turn_on(self) -> None:
        self.activate = True
        self.shield_time = SHIELD_REMAIN_TIME

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)

    def hit(self):
        self.shield_hp -= 1
        if self.shield_hp == 0:
            self.activate = False
        self.image = assets_manager.images['shield']
        

