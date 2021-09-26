from game.sprites.laser import Laser
import random

import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.explode import Explode


class Comet(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.dir = random.uniform(-np.pi, np.pi)
        self.x = random.uniform(0.0, float(SCREEN_WIDTH))
        self.y = random.uniform(0.0, float(SCREEN_HEIGHT))
        self.x += 3000 * -np.cos(self.dir)
        self.y += 3000 * -np.sin(self.dir)

        self.image = pygame.transform.rotate(
            assets_manager.images['comet'], ((
                np.pi - self.dir) * 360) / (2 * np.pi)
        )
        self.rect = self.image.get_rect(
            center=self.image.get_rect(center=(self.x, self.y)).center)
        self.hitbox = pygame.Rect(
            (self.x - 15 + 70 * np.cos(self.dir),
             self.y - 15 + 70 * np.sin(self.dir)), (30, 30)
        )
        self.remaining_time = 30.0
        self.explode = None
        self.laser = None

    def hitbox_inbounds(self):
        return (self.hitbox.bottom <= SCREEN_HEIGHT + 20 and self.hitbox.top >= -20 and
                self.hitbox.right <= SCREEN_WIDTH + 20 and self.hitbox.left >= -20)

    def update(self, t: float, difficulty) -> None:
        if self.hitbox_inbounds():
            if not self.laser:
                self.laser = Laser(self.hitbox.center, self.dir)
            self.laser.update(t)
            if self.laser.t > LASERREMAINTIME:
                if not self.explode:
                    self.x += t * np.cos(self.dir) * 200 * min(2, difficulty)
                    self.y += t * np.sin(self.dir) * 200 * min(2, difficulty)
                    self.hitbox = pygame.Rect(
                        (self.x - 15 + 70 * np.cos(self.dir),
                        self.y - 15 + 70 * np.sin(self.dir)), (30, 30)
                    )
                    self.image = pygame.transform.rotate(
                        assets_manager.images['comet'], ((
                            np.pi - self.dir) * 360) / (2 * np.pi)
                    )
                    self.rect = self.image.get_rect(
                        center=self.image.get_rect(center=(self.x, self.y)).center)
                    self.remaining_time -= t
                    if self.remaining_time <= 0:
                        self.kill()
                elif not self.explode.update(t):
                    self.kill()
        else:
            self.x += t * np.cos(self.dir) * 200 * min(2, difficulty)
            self.y += t * np.sin(self.dir) * 200 * min(2, difficulty)
            self.hitbox = pygame.Rect(
                (self.x - 15 + 70 * np.cos(self.dir),
                self.y - 15 + 70 * np.sin(self.dir)), (30, 30)
            )

    def draw(self, window: pygame.Surface) -> None:
        if self.hitbox_inbounds():
            if not self.laser:
                self.laser = Laser(self.hitbox.center, self.dir)
                self.laser.update(0)
            self.laser.draw(window)
            if self.image:
                window.blit(self.image, self.rect)
                # pygame.draw.rect(window, (255, 255, 255), self.hitbox)
            elif self.explode and self.explode.image:
                window.blit(self.explode.image, self.explode.rect)

    def collision_player(self, player):
        if player.rect.colliderect(self.hitbox):
            if not self.explode:
                if player.hit():
                    self.image = None
                    self.explode = Explode(self.rect.center)
