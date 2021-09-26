import random

import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.bullet import Bullet


class Bomber(pygame.sprite.Sprite):
    def __init__(self, player_collision_group: pygame.sprite.Group) -> None:
        super().__init__()

        self.animation = assets_manager.animations['bomber']
        self.frame = 0

        self.image = self.animation[0]
        self.shadow = self.image.copy()
        alpha = 128
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

        self.x = -400

        self.rect = self.animation[0].get_rect()
        self.rect.topleft = (self.x, (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2))
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.topleft = self.shadow_rect.topleft + pygame.Vector2(-15, 15)

        self.bullets = pygame.sprite.Group()
        self.bullet_image = assets_manager.images['bomber_bullet']
        self.shoot_cooldown = BOMBER_SHOOT_COOLDOWN
        self.player_collision_group = player_collision_group

        self.dir = 0.0
        self.activated = False

    def aim(self, px: float, py: float) -> None:
        self.dir = np.arctan2(self.rect.centery - py, px - self.rect.centerx)

    def shoot(self, difficulty) -> None:
        if self.shoot_cooldown <= 0:
            new_bullet = Bullet(
                self.bullet_image, self.rect.center, BOMBER_BULLET_SPEED * np.cos(self.dir),
                                                     -BOMBER_BULLET_SPEED * np.sin(self.dir)
            )
            self.bullets.add(new_bullet)
            self.player_collision_group.add(new_bullet)
            self.shoot_cooldown = BOMBER_SHOOT_COOLDOWN / min(2, 1 + difficulty / 10)

    def random_activate(self, difficulty):
        if self.activated or difficulty == 1:
            return
        if random.randint(0, 1000) <= min(4, difficulty):
            self.activated = True

    def update(self, t: float, difficulty) -> None:
        if self.activated:
            self.x += 4
            self.shoot_cooldown -= t
            self.shoot(difficulty)
            if self.x >= SCREEN_WIDTH:
                self.activated = False
                self.x = -400

        if self.frame >= len(self.animation):
            self.frame = 0

        self.image = self.animation[self.frame]
        self.rect = self.animation[self.frame].get_rect()
        self.rect.topleft = (self.x, (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2))
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.topleft = self.shadow_rect.topleft + pygame.Vector2(-15, 15)
        self.frame += 1
        self.bullets.update(t)

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.shadow, self.shadow_rect)
        window.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(window)
