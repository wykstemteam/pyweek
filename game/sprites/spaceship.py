import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.bullet import Bullet


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, player_collision_group: pygame.sprite.Group) -> None:
        super().__init__()

        self.image = assets_manager.images['space_ship']

        self.laser_charge_ani = assets_manager.animations['laser_charge']
        self.lc_img = assets_manager.images['lc_charge_none']
        self.lc_rect = self.lc_img.get_rect()
        self.lc_rect.topleft = (800, (SCREEN_WIDTH / 2) - 100)
        self.lc_frame = 0.0
        self.is_charge = False

        self.laser_shoot_ani = assets_manager.animations['laser_shoot']
        self.ls_img = assets_manager.images['ls_shoot_none']
        self.ls_rect = self.ls_img.get_rect()
        self.ls_rect.topleft = (-100, 0)
        self.ls_frame = 0.0
        self.is_shoot = False

        self.x = 1500
        self.y = (SCREEN_HEIGHT / 2) - (self.image.get_height() / 2)

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.player_collision_group = player_collision_group

        self.dir = 0.0
        self.activated = False

        self.bullet_pattern = {}

    def update(self, t):
        if self.activated:
            if self.x > 1000:
                self.x -= 2
        else:
            if self.x < 1600:
                self.x += 2

        self.rect.topleft = (self.x, self.y)

        if self.is_charge == True:
            if self.lc_frame < len(self.laser_charge_ani):
                self.lc_img = self.laser_charge_ani[int(self.lc_frame)]
                self.lc_frame += 0.2
            else:
                self.ic_charge = False
                self.lc_frame = 0.0
                self.lc_img = assets_manager.images['lc_charge_none']

        if self.is_shoot == True:
            if self.ls_frame < len(self.laser_shoot_ani):
                self.ls_img = self.laser_shoot_ani[int(self.ls_frame)]
                self.ls_frame += 0.2
            else:
                self.is_shoot = False
                self.ls_frame = 0.0
                self.ls_img = assets_manager.images['ls_shoot_none']

    def draw(self, window):
        window.blit(self.lc_img, self.lc_rect)
        window.blit(self.ls_img, self.ls_rect)
        window.blit(self.image, self.rect)
