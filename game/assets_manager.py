import os

import pygame
from game.constants import *


class AssetsManager:
    def __init__(self):
        self.images = {}
        for fn in os.listdir(os.path.join('assets', 'images')):
            base_fn = os.path.splitext(fn)[0]
            self.images[base_fn] = pygame.image.load(os.path.join('assets', 'images', fn))
        
        self.images['policecar'] = pygame.transform.scale(
            self.images['policecar'],
            (POLICECAR_WIDTH, POLICECAR_HEIGHT)
        )
        self.images['road'] = pygame.transform.scale(
            self.images['road'], (SCREEN_WIDTH, SCREEN_HEIGHT - BUILDING_HEIGHT)
        )
        self.images['GameOver'] = pygame.transform.scale(
            self.images['GameOver'], (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.images['bullet'] = pygame.transform.scale(
            self.images['bullet'],
            (BULLET_WIDTH, BULLET_HEIGHT)
        )
        self.images['player'] = pygame.transform.scale(
            self.images['player'],
            (PLAYER_WIDTH, PLAYER_HEIGHT)
        )
