import random
from typing import List

import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.bullet import Bullet


class UFO(pygame.sprite.Sprite):
    image = assets_manager.images['UFO']
    bullet_image = assets_manager.images['UFO_bullet']

    def __init__(self, player_collision_group: pygame.sprite.Group) -> None:
        super().__init__()

        self.cenx = 2050
        self.ceny = (SCREEN_HEIGHT / 2)

        self.rect = self.image.get_rect()
        self.rect.center = (self.cenx, self.ceny)

        self.player_collision_group = player_collision_group

        self.rotate_deg = 0.0
        self.rotate_rad = 0.0
        self.rotate_velocity = -1.0
        self.activated = False
        self.activated_dur = 0.0

        self.bullets = pygame.sprite.Group()
        self.bullet_pattern = 0
        self.pattern_dur = 0.0
        self.shoot_cooldown = UFO_SHOOT_COOLDOWN

        self.circle_flag = False
        self.player_collision_group.add(self)

    def bullet(self, *args, **kwargs):
        return Bullet(self.bullet_image, self.rect.center, *args, **kwargs)

    def get_bullet_pattern(self) -> List[Bullet]:
        new_bullet = []
        if self.bullet_pattern == 0:  # weird
            new_bullet = [
                self.bullet(
                    UFO_BULLET_SPEED * np.cos(self.rotate_rad),
                    UFO_BULLET_SPEED * np.sin(self.rotate_rad)
                ),
                self.bullet(
                    UFO_BULLET_SPEED * np.cos(self.rotate_rad),
                    -UFO_BULLET_SPEED * np.sin(self.rotate_rad)
                ),
                self.bullet(
                    -UFO_BULLET_SPEED * np.cos(self.rotate_rad),
                    UFO_BULLET_SPEED * np.sin(self.rotate_rad)
                ),
                self.bullet(
                    -UFO_BULLET_SPEED * np.cos(self.rotate_rad),
                    -UFO_BULLET_SPEED * np.sin(self.rotate_rad)
                )
            ]
        elif self.bullet_pattern == 1:  # spiral
            for i in range(1, 16, 2):
                new_bullet.append(
                    self.bullet(
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (i * 2 * np.pi / 16)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (i * 2 * np.pi / 16))
                    )
                )
        elif self.bullet_pattern == 3:  # double spiral
            for i in range(1, 16, 2):
                new_bullet.append(
                    self.bullet(
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (i * 2 * np.pi / 16)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (i * 2 * np.pi / 16))
                    )
                )
            for i in range(1, 16, 2):
                new_bullet.append(
                    self.bullet(
                        UFO_BULLET_SPEED * np.cos(np.pi - (self.rotate_rad + (i * 2 * np.pi / 16))),
                        UFO_BULLET_SPEED * np.sin(np.pi - (self.rotate_rad + (i * 2 * np.pi / 16)))
                    )
                )
        elif self.bullet_pattern == 2:  # sun
            if self.circle_flag:
                self.circle_flag = False
                for i in range(1, 32, 2):
                    new_bullet.append(
                        self.bullet(
                            UFO_BULLET_SPEED * np.cos(i * 2 * np.pi / 32),
                            UFO_BULLET_SPEED * np.sin(i * 2 * np.pi / 32)
                        )
                    )
            else:
                self.circle_flag = True
                for i in range(0, 32, 2):
                    new_bullet.append(
                        self.bullet(
                            UFO_BULLET_SPEED * np.cos(i * 2 * np.pi / 32),
                            UFO_BULLET_SPEED * np.sin(i * 2 * np.pi / 32)
                        )
                    )
        return new_bullet

    def shoot(self) -> None:
        if self.shoot_cooldown > 0:
            return

        self.shoot_cooldown = UFO_SHOOT_COOLDOWN
        for bullet in self.get_bullet_pattern():
            self.bullets.add(bullet)
            self.player_collision_group.add(bullet)

    def random_activate(self, difficulty):
        if self.activated:
            return
        if random.randint(0, 1000) <= difficulty:
            self.activated = True
            self.activated_dur = random.uniform(30.0, 50.0)

    def update(self, t: float, difficulty) -> None:
        if not self.activated:
            self.cenx = min(2050, self.cenx + 5)
            self.activated_dur = 0.0
        else:
            self.activated_dur -= t
            if self.activated_dur <= 0:
                self.activated = False
            self.cenx = max(1450, self.cenx - 5)

        self.rotate_deg += self.rotate_velocity
        if self.rotate_deg <= -360:
            self.rotate_deg = 0.0
        self.rotate_rad = (self.rotate_deg / 360.0) * 2 * np.pi
        self.image = pygame.transform.rotate(assets_manager.images['UFO'], self.rotate_deg)
        self.rect = self.image.get_rect(
            center=self.image.get_rect(center=(self.cenx, self.ceny)).center
        )

        if self.pattern_dur <= 0.0:
            self.bullet_pattern = random.randint(0, 3)
            if difficulty < 4:
                self.bullet_pattern = random.randint(0, 2)
            self.pattern_dur = random.uniform(5, 10)

        self.shoot_cooldown -= t
        self.pattern_dur -= t
        self.shoot()
        self.bullets.update(t)

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(window)

    def missile_hit(self, missile):
        self.activated = False
        missile.hit()
