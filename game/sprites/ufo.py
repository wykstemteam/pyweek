import random

import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.bullet import Bullet
from game.sprites.player import Player


class UFO(pygame.sprite.Sprite):
    def __init__(self, player_collision_group: pygame.sprite.Group) -> None:
        super().__init__()

        self.image = assets_manager.images['UFO']
        self.bullet_image = assets_manager.images['UFO_bullet']

        self.cenx = 2050
        self.ceny = (SCREEN_HEIGHT / 2)

        self.rect = self.image.get_rect()
        self.rect.center = (self.cenx, self.ceny)

        self.player_collision_group = player_collision_group

        self.rotate_deg = 0.0
        self.rotate_rad = 0.0
        self.rotate_velocity = -1.0
        self.activated = False

        self.bullets = pygame.sprite.Group()
        self.bullet_pattern = 0
        self.pattern_dur = 0.0
        self.shoot_cooldown = UFO_SHOOT_COOLDOWN

        self.circle_flag = False
        self.player_collision_group.add(self)

    def shoot(self) -> None:
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = UFO_SHOOT_COOLDOWN
            new_bullets = []
            # weird
            if self.bullet_pattern == 1:
                new_bullets = [
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad), UFO_BULLET_SPEED * np.sin(self.rotate_rad)
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad), -UFO_BULLET_SPEED * np.sin(self.rotate_rad)
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        -UFO_BULLET_SPEED * np.cos(self.rotate_rad), UFO_BULLET_SPEED * np.sin(self.rotate_rad)
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        -UFO_BULLET_SPEED * np.cos(self.rotate_rad), -UFO_BULLET_SPEED * np.sin(self.rotate_rad)
                    )
                ]
            # spiral
            elif self.bullet_pattern == 2:
                new_bullets = [
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad - (np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad - (np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (3 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (3 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad - (3 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad - (3 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (5 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (5 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad - (5 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad - (5 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (7 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (7 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad - (7 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad - (7 * np.pi / 8))
                    )
                ]
            # double spiral
            elif self.bullet_pattern == 3:
                new_bullets = [
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad - (np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad - (np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (3 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (3 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad - (3 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad - (3 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (5 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (5 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad - (5 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad - (5 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad + (7 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad + (7 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(self.rotate_rad - (7 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(self.rotate_rad - (7 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(np.pi - self.rotate_rad + (np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(np.pi - self.rotate_rad + (np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(np.pi - self.rotate_rad - (np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(np.pi - self.rotate_rad - (np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(np.pi - self.rotate_rad + (3 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(np.pi - self.rotate_rad + (3 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(np.pi - self.rotate_rad - (3 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(np.pi - self.rotate_rad - (3 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(np.pi - self.rotate_rad + (5 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(np.pi - self.rotate_rad + (5 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(np.pi - self.rotate_rad - (5 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(np.pi - self.rotate_rad - (5 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(np.pi - self.rotate_rad + (7 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(np.pi - self.rotate_rad + (7 * np.pi / 8))
                    ),
                    Bullet(
                        self.bullet_image,
                        self.rect.center,
                        UFO_BULLET_SPEED * np.cos(np.pi - self.rotate_rad - (7 * np.pi / 8)),
                        UFO_BULLET_SPEED * np.sin(np.pi - self.rotate_rad - (7 * np.pi / 8))
                    )
                ]
            # circle
            elif self.bullet_pattern == 4:
                if self.circle_flag:
                    self.circle_flag = False
                    new_bullets = [
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED, UFO_BULLET_SPEED
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED, -UFO_BULLET_SPEED
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            -UFO_BULLET_SPEED, UFO_BULLET_SPEED
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            -UFO_BULLET_SPEED, -UFO_BULLET_SPEED
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED, 0.0
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            0.0, UFO_BULLET_SPEED
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            -UFO_BULLET_SPEED, 0.0
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            0.0, -UFO_BULLET_SPEED
                        )
                    ]
                else:
                    self.circle_flag = True
                    new_bullets = [
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED * np.cos(np.pi / 8),
                            UFO_BULLET_SPEED * np.sin(np.pi / 8)
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED * np.cos(-np.pi / 8),
                            UFO_BULLET_SPEED * np.sin(-np.pi / 8)
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED * np.cos(3 * np.pi / 8),
                            UFO_BULLET_SPEED * np.sin(3 * np.pi / 8)
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED * np.cos(-3 * np.pi / 8),
                            UFO_BULLET_SPEED * np.sin(-3 * np.pi / 8)
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED * np.cos(5 * np.pi / 8),
                            UFO_BULLET_SPEED * np.sin(5 * np.pi / 8)
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED * np.cos(-5 * np.pi / 8),
                            UFO_BULLET_SPEED * np.sin(-5 * np.pi / 8)
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED * np.cos(7 * np.pi / 8),
                            UFO_BULLET_SPEED * np.sin(7 * np.pi / 8)
                        ),
                        Bullet(
                            self.bullet_image,
                            self.rect.center,
                            UFO_BULLET_SPEED * np.cos(-7 * np.pi / 8),
                            UFO_BULLET_SPEED * np.sin(-7 * np.pi / 8)
                        )
                    ]
            for bullet in new_bullets:
                self.bullets.add(bullet)
                self.player_collision_group.add(bullet)

    def update(self, t: float) -> None:
        if not self.activated:
            if self.cenx < 2050:
                self.cenx += 5
        else:
            if self.cenx > 1450:
                self.cenx -= 5

        self.rotate_deg += self.rotate_velocity
        if self.rotate_deg <= -360:
            self.rotate_deg = 0.0
        self.rotate_rad = (self.rotate_deg / 360.0) * 2 * np.pi
        self.image = pygame.transform.rotate(assets_manager.images['UFO'], self.rotate_deg)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(self.cenx, self.ceny)).center)

        self.bullet_pattern = random.randint(1, 4)
        self.pattern_dur = random.uniform(10, 20)

        self.shoot_cooldown -= t
        self.shoot()
        self.bullets.update(t)

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(window)

