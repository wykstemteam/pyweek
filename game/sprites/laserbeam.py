import pygame
import random

from game.constants import *

class Laser(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface((SCREEN_WIDTH, 50), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill((50, 0, 0, 0))
        self.laser_cooldown = LASER_COOLDOWN
        self.laserred_cooldown = LASERRED_COOLDOWN
        self.laserblink_cooldown = LASERBLINK_COOLDOWN
        self.laserremaintime = -1
        self.laserrandom = False

    def update(self, t):
        if self.laserrandom:
            self.rect.topleft = (0, random.randint(BUILDING_HEIGHT, SCREEN_HEIGHT - LASER_HEIGHT))
            self.laserrandom = False
            self.laserremaintime = LASERREMAINTIME
        if self.laser_cooldown <= 0:
            self.laser_cooldown = 999
            self.laserrandom = True
        else:
            self.laser_cooldown -= t
        if self.laserremaintime >= 0:
            self.laserremaintime -= t
            if self.laserred_cooldown >= 0:
                self.image.fill((50, 0, 0, 100))
                self.laserred_cooldown -= t
                self.laserblink_cooldown = LASERBLINK_COOLDOWN
            else:
                self.image.fill((50, 0, 0, 0))
                self.laserblink_cooldown -= t
                if self.laserblink_cooldown < 0:
                    self.laserred_cooldown = LASERRED_COOLDOWN
        elif self.laserremaintime < 0 and self.laser_cooldown > 900:
            self.image.fill((50, 0, 0, 0))
            self.laser_cooldown = LASER_COOLDOWN

    def draw(self, window):
        window.blit(self.image, self.rect)