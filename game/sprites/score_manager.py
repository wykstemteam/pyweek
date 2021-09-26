import pygame
from pygame.rect import Rect

from game.constants import *


class ScoreManager(pygame.sprite.Sprite):
    # TODO: help i dunno how to do gui

    def __init__(self) -> None:
        super().__init__()
        self.score = 0
        self.highscore = self.score
        self.reached_checkpoint = False
        self.checkpoint_count = 0
        self.update(0)

    def update(self, t: float) -> None:
        #if self.reached_checkpoint:
        #    self.score += 1000 + (500 * self.checkpoint_count)
        self.score += (-BACKGROUND_VELOCITY * t / 100 * DIST_SPD) * 12
        
        

