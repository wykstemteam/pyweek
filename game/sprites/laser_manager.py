import random

import pygame

from game.constants import *
from game.sprites import Laser


class LaserManager:
    def __init__(self):
        self.lasers = pygame.sprite.Group()
        self.t = 0

    def number(self):
        return len(self.lasers)

    def add(self):
        new_laser = Laser()
        self.lasers.add(new_laser)

    def update(self, t):    
        self.t += t
        if self.t < LASER_COOLDOWN * 2:
            if len(self.lasers) < 1:
                self.add()
        elif self.t < LASER_COOLDOWN * 4:
            if len(self.lasers) < 2:
                self.add()
        elif self.t < LASER_COOLDOWN * 7:
            if len(self.lasers) < 3:
                self.add()
        self.lasers.update(t)
        print(self.lasers)

    def draw(self, window):
        self.lasers.draw(window)

