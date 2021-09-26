import pygame
from pygame.rect import Rect

from game.constants import *


class ScoreManager(pygame.sprite.Sprite):
    # TODO: help i dunno how to do gui

    def __init__(self) -> None:
        super().__init__()
        self.score = 0
        self.highscore = self.score
        self.update(0)

    def update(self, t: float) -> None:
        self.score += (-BACKGROUND_VELOCITY * t / 100 * DIST_SPD) * 12
        

