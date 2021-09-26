import pygame
from pygame.math import Vector2

from game.constants import *


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, dir:float = 0) -> None:
        super().__init__()

        self.image = pygame.Surface((SCREEN_WIDTH*2, 50))
        self.image = pygame.transform.rotate(self.image, dir * 180 / 3.14159)
        self.image.fill((127, 0, 0))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.last_laser_shoot = 0
        self.pos = Vector2(pos)
        self.t = 0
        self.laser_amount = 0
        self.laser_blink_cooldown = LASERBLINK_COOLDOWN

    def update(self, t: float) -> None:
        self.t += t
        self.rect.topleft = self.pos
        if self.t <= LASERREMAINTIME:
            if self.t % (self.laser_blink_cooldown * 2) < self.laser_blink_cooldown:
                self.image.set_alpha(127)
            else:
                self.image.set_alpha(0)
                self.laser_blink_cooldown -= t / 5
        else:
            self.image.set_alpha(0)

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
