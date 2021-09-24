import random

import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.bullet import Bullet
from game.sprites.player import Player


class UFO(pygame.sprite.Sprite):
    def __init__(self, player_collision_group: pygame.sprite.Group) -> None:
        super().__init__()

        self.image = assets_manager.images['UFO']
        #       self.bullet_image = assets_manager.images['UFO_bullet']

        self.cenx = 2050
        self.ceny = (SCREEN_HEIGHT / 2)

        self.rect = self.image.get_rect()
        self.rect.center = (self.cenx, self.ceny)

        self.player_collision_group = player_collision_group

        self.rotate_deg = 0.0
        self.rotate_velocity = -1.0
        self.activated = False

        self.bullets = pygame.sprite.Group()
        self.bullet_pattern = 1
        self.pattern_dur = 0.0
        self.shoot_cooldown = SPACESHIP_SHOOT_COOLDOWN

        self.player_collision_group.add(self)

    # def shoot(self) -> None:
    #     if self.shoot_cooldown <= 0:
    #         new_bullets = []
    #         # spiral
    #         if self.bullet_pattern == 1:
    #             new_bullets = [
    #                 Bullet(
    #                     self.bullet_image,
    #                     pygame.Vector2(self.rect.centerx,
    #                                    self.rect.centery - 200), -SPACESHIP_BULLET_SPEED, 0
    #                 ),
    #                 Bullet(
    #                     self.bullet_image,
    #                     pygame.Vector2(self.rect.centerx,
    #                                    self.rect.centery - 100), -SPACESHIP_BULLET_SPEED, 0
    #                 ),
    #                 Bullet(
    #                     self.bullet_image,
    #                     pygame.Vector2(self.rect.centerx,
    #                                    self.rect.centery + 100), -SPACESHIP_BULLET_SPEED, 0
    #                 ),
    #                 Bullet(
    #                     self.bullet_image,
    #                     pygame.Vector2(self.rect.centerx,
    #                                    self.rect.centery + 200), -SPACESHIP_BULLET_SPEED, 0
    #                 )
    #             ]
    #         # flower
    #         elif self.bullet_pattern == 2:
    #             new_bullets = [
    #                 Bullet(
    #                     self.bullet_image,
    #                     pygame.Vector2(self.rect.centerx,
    #                                    self.rect.centery - 150), -SPACESHIP_BULLET_SPEED, 0
    #                 ),
    #                 Bullet(
    #                     self.bullet_image,
    #                     pygame.Vector2(self.rect.centerx,
    #                                    self.rect.centery + 150), -SPACESHIP_BULLET_SPEED, 0
    #                 )
    #             ]
    #         # random
    #         elif self.bullet_pattern == 3:
    #             pass
    #
    #         for bullet in new_bullets:
    #             self.bullets.add(bullet)
    #             self.player_collision_group.add(bullet)

    def update(self, t: float) -> None:
        if not self.activated:
            if self.cenx < 2050:
                self.cenx += 5
        elif self.cenx > 1450:
            self.cenx -= 5

        self.rotate_deg += self.rotate_velocity
        if self.rotate_deg <= -360:
            self.rotate_deg = 0.0
        self.image = pygame.transform.rotate(assets_manager.images['UFO'], self.rotate_deg)
        self.rect = self.image.get_rect(
            center=self.image.get_rect(center=(self.cenx, self.ceny)).center
        )

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
