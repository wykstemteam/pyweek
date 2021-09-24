import random

import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.laserbeam import Laser
from game.sprites.missile_aircraft import MissileAircraft


class LaserManager:
    def __init__(self, player_collision_group: pygame.sprite.Group) -> None:
        self.lasers = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.player_collision_group = player_collision_group
        self.last_laser_shoot = 0
        self.t = 0
        self.amounts = 0

    def add(self) -> None:
        pos = random.randint(BUILDING_HEIGHT, SCREEN_HEIGHT - LASER_HEIGHT)
        new_laser = Laser(pos)
        self.lasers.add(new_laser)
        new_missiles = MissileAircraft(assets_manager.images['missile_for_aircraft'], pos)
        self.missiles.add(new_missiles)
        self.player_collision_group.add(new_missiles)

    def update(self, t: float, shop: bool) -> None:
        if not shop:
            self.t += t
        if self.t < LASER_COOLDOWN:
            pass
        elif self.t < LASER_COOLDOWN * 2:
            self.amounts = 1
        elif self.t < LASER_COOLDOWN * 4:
            self.amounts = 2
        elif self.t < LASER_COOLDOWN * 7:
            self.amounts = 3
        if self.t - self.last_laser_shoot >= LASER_COOLDOWN:
            self.last_laser_shoot = self.t
            self.lasers.empty()
            for i in range(self.amounts):
                self.add()  # FIXME: ??? if don't use iterator then use _ instead of i
        self.lasers.update(t)
        self.missiles.update(t)

    def draw(self, window: pygame.Surface) -> None:
        self.lasers.draw(window)
        for missile in self.missiles:
            missile.draw(window)
