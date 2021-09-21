import os

import pygame

from game.constants import *


class AssetsManager:
    def __init__(self):
        self.images = {}
        for fn in os.listdir(os.path.join('assets', 'images')):
            base_fn = os.path.splitext(fn)[0]
            self.images[base_fn] = pygame.image.load(os.path.join('assets', 'images', fn))
        self.images['warning sign'] = pygame.transform.scale(
            self.images['warning sign'], (WARN_WIDTH, WARN_HEIGHT)
        )
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
        self.images['arrow'] = pygame.transform.scale(
            self.images['arrow'],
            (80, 100)
        )

        for i in range(1, 4):  # building 1-3
            self.images[f'building{i}'] = pygame.transform.scale(
                self.images[f'building{i}'],
                (BUILDING_WIDTH, BUILDING_HEIGHT),
            )
        for i in range(1, 4):  # obstacle 1-3
            self.images[f'obstacle{i}'] = pygame.transform.scale(
                self.images[f'obstacle{i}'],
                (OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
            )


assets_manager = AssetsManager()
