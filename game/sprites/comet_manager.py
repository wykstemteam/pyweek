from game.sprites.comet import Comet
import pygame.sprite
import random

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.obstacle import Obstacle


class CometManager:
    def __init__(self, player_collision_group) -> None:
        self.comets = pygame.sprite.Group()
        self.player_collision_group = player_collision_group
        self.reached_checkpoint = False

    def add(self, difficulty):
        if random.randint(0, 1000) <= min(5, difficulty) and len(self.comets) <= MAX_COMETS:
            new_comet = Comet()
            self.player_collision_group.add(new_comet)
            self.comets.add(new_comet)

    def update(self, t: float, difficulty) -> None:
        self.comets.update(t, difficulty)

    def draw(self, window: pygame.Surface) -> None:
        for comet in self.comets:
            comet.draw(window)

    def kill(self) -> None:
        self.comets.empty()
