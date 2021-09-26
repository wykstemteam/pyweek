import pygame
from pygame.math import Vector2
import numpy as np

from game.constants import *


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, dir:float = 0) -> None:
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*2, 50), pygame.SRCALPHA)
        self.image.fill((127, 0, 0))
        self.image = pygame.transform.rotate(self.image, -dir * 180 / 3.14159)
        self.image.set_alpha(0)
        pos = Vector2(pos)
        dx, dy = 0, 0
        if dir == 0:
            pass
        elif 3* 3.14159/4 >= abs(dir) >= 3.14159/4:
            dx = SCREEN_WIDTH/2 - pos.x
            dy = dx * np.tan(dir)
        else:
            dy = SCREEN_HEIGHT/2 - pos.y
            dx = dy / np.tan(dir)
        self.pos = pos + Vector2(dx,dy) 
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.last_laser_shoot = 0
        self.t = 0
        self.laser_amount = 0
        self.laser_blink_cooldown = LASERBLINK_COOLDOWN

    def update(self, t: float) -> None:
        self.t += t
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
