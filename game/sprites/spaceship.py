import random
from typing import List

import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.bullet import Bullet
from game.sprites.player import Player


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, player_collision_group: pygame.sprite.Group) -> None:
        super().__init__()

        self.image = assets_manager.images['space_ship']
        self.bullet_image = assets_manager.images['spaceship_bullet']

        # lc = laser charge
        self.laser_charge_ani = assets_manager.animations['laser_charge']
        self.lc_img = assets_manager.images['lc_charge_none']
        self.lc_rect = self.lc_img.get_rect()
        self.lc_rect.topleft = (800, (SCREEN_HEIGHT / 2) - 100)
        self.lc_frame = 0.0
        self.is_charge = False

        # ls = laser shoot
        self.laser_shoot_ani = assets_manager.animations['laser_shoot']
        self.ls_img = assets_manager.images['ls_shoot_none']
        self.ls_rect = self.ls_img.get_rect()
        self.ls_rect.topleft = (-100, 0)
        self.ls_frame = 0.0
        self.is_shoot = False

        self.x = 1600
        self.y = (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2)

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.player_collision_group = player_collision_group

        self.dir = 0.0
        self.activated = False
        self.activated_dur = 0.0

        self.bullets = pygame.sprite.Group()
        self.bullet_pattern = 0
        self.pattern_dur = 0.0
        self.shoot_cooldown = SPACESHIP_SHOOT_COOLDOWN

        self.player_collision_group.add(self)
        self.earthquake = False

    def get_bullet_pattern(self) -> List[Bullet]:
        if self.bullet_pattern == 0:
            return [
                Bullet(
                    self.bullet_image, pygame.Vector2(SCREEN_WIDTH, self.rect.centery - 300),
                    -SPACESHIP_BULLET_SPEED, 0
                ),
                Bullet(
                    self.bullet_image, pygame.Vector2(SCREEN_WIDTH, self.rect.centery - 200),
                    -SPACESHIP_BULLET_SPEED, 0
                ),
                Bullet(
                    self.bullet_image, pygame.Vector2(SCREEN_WIDTH, self.rect.centery - 100),
                    -SPACESHIP_BULLET_SPEED, 0
                ),
                Bullet(
                    self.bullet_image, pygame.Vector2(SCREEN_WIDTH, self.rect.centery + 100),
                    -SPACESHIP_BULLET_SPEED, 0
                ),
                Bullet(
                    self.bullet_image, pygame.Vector2(SCREEN_WIDTH, self.rect.centery + 200),
                    -SPACESHIP_BULLET_SPEED, 0
                ),
                Bullet(
                    self.bullet_image, pygame.Vector2(SCREEN_WIDTH, self.rect.centery + 300),
                    -SPACESHIP_BULLET_SPEED, 0
                )
            ]
        elif self.bullet_pattern == 1:
            return [
                Bullet(
                    self.bullet_image, pygame.Vector2(self.rect.centerx, self.rect.centery - 150),
                    -SPACESHIP_BULLET_SPEED, 0
                ),
                Bullet(
                    self.bullet_image, pygame.Vector2(self.rect.centerx, self.rect.centery + 150),
                    -SPACESHIP_BULLET_SPEED, 0
                ),
                Bullet(
                    self.bullet_image, pygame.Vector2(self.rect.centerx, self.rect.centery + 250),
                    -SPACESHIP_BULLET_SPEED, 0
                ),
                Bullet(
                    self.bullet_image, pygame.Vector2(self.rect.centerx, self.rect.centery - 250),
                    -SPACESHIP_BULLET_SPEED, 0
                )
            ]

    def shoot(self) -> None:
        if self.shoot_cooldown <= 0:
            for bullet in self.get_bullet_pattern():
                self.bullets.add(bullet)
                self.player_collision_group.add(bullet)

            self.shoot_cooldown = SPACESHIP_SHOOT_COOLDOWN

    def random_activate(self, difficulty):
        if self.activated:
            return
        if random.randint(0, 1000) <= difficulty:
            self.activated = True
            self.activated_dur = random.uniform(30.0, 50.0)

    def update(self, t: float) -> None:
        if not self.activated:
            self.x = min(1600, self.x + 5)
            self.activated_dur = 0.0
        else:
            self.activated_dur -= t
            if self.activated_dur <= 0:
                self.activated = False
            self.x = max(1000, self.x - 5)

        self.rect.topleft = (self.x, self.y)

        if self.is_shoot:
            if self.ls_frame < len(self.laser_shoot_ani):
                self.ls_img = self.laser_shoot_ani[int(self.ls_frame)]
                self.ls_frame += 0.2
            else:
                self.is_shoot = False
                self.ls_frame = 0.0
                self.ls_img = assets_manager.images['ls_shoot_none']
        elif self.is_charge:
            if self.lc_frame < len(self.laser_charge_ani):
                self.lc_img = self.laser_charge_ani[int(self.lc_frame)]
                self.lc_frame += 0.2
            else:
                self.is_charge = False
                self.is_shoot = True
                self.lc_frame = 0.0
                self.lc_img = assets_manager.images['lc_charge_none']

        if self.pattern_dur <= 0.1:
            self.bullet_pattern = (self.bullet_pattern + 1) % 2
            self.pattern_dur = random.uniform(2, 5)
        self.shoot_cooldown -= t
        self.pattern_dur -= t

        if self.activated:
            self.shoot()
        self.bullets.update(t)

    def draw(self, window: pygame.Surface) -> None:
        if not self.earthquake:
            window.blit(self.lc_img, self.lc_rect)
            window.blit(self.ls_img, self.ls_rect)
        window.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(window)

    def collision_player(self, player: Player):
        if (
                self.is_shoot and 2 <= self.ls_frame <= 18
                and player.rect.colliderect(pygame.Rect(0, 220, 1500, 200))
                and not self.earthquake
        ):
            print(self.earthquake)
            player.hit()

