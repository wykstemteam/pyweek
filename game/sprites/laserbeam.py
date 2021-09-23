import random

import pygame

from game.constants import *


class Laser(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface((SCREEN_WIDTH, 50))
        self.image.fill((127, 0, 0))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.last_laser_shoot = 0
        self.t = 0
        self.laser_amount = 0

    def update(self, dt):
        self.t += dt
        if self.t - self.last_laser_shoot >= LASER_COOLDOWN:
            self.last_laser_shoot = self.t
            self.rect.topleft = (0, random.randint(BUILDING_HEIGHT, SCREEN_HEIGHT - LASER_HEIGHT))

        if self.last_laser_shoot != 0 and self.t - self.last_laser_shoot <= LASERREMAINTIME:
            if (self.t - self.last_laser_shoot) % (LASERBLINK_COOLDOWN * 2) < LASERBLINK_COOLDOWN:
                self.image.set_alpha(127)
            else:
                self.image.set_alpha(0)

    def draw(self, window):
        window.blit(self.image, self.rect)
