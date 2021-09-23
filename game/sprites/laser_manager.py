import random

import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Laser
from game.sprites import MissileAircraft


class LaserManager:
    def __init__(self):
        self.lasers = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.t = 0

    def add(self):
        pos = random.randint(BUILDING_HEIGHT, SCREEN_HEIGHT - LASER_HEIGHT)
        new_laser = Laser(pos)
        self.lasers.add(new_laser)
        new_missiles = MissileAircraft(assets_manager.images['missile_for_aircraft'], pos)
        self.missiles.add(new_missiles)

    def update(self, t):
        self.t += t
        if self.t < LASER_COOLDOWN * 2 + 5:
            if len(self.lasers) < 1:
                self.lasers.empty()
                self.add()
        elif self.t < LASER_COOLDOWN * 4 + 5:
            if len(self.lasers) < 2:
                self.lasers.empty()
                self.add()
                self.add()
        elif self.t < LASER_COOLDOWN * 7 + 5:
            if len(self.lasers) < 3:
                self.lasers.empty()
                self.add()
                self.add()
                self.add()
        self.lasers.update(t)
        self.missiles.update(t)

    def draw(self, window):
        self.lasers.draw(window)
        self.missiles.draw(window)

