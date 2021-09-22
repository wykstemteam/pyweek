import os

import pygame

from game.constants import *


class AssetsManager:
    def __init__(self):
        pygame.mixer.init()

        self.images = {}
        self.sounds = {}

        self.init_images()
        # self.init_sounds()

    def init_images(self):
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

    def init_sounds(self):
        for fn in os.listdir(os.path.join('assets', 'sounds')):
            base_fn = os.path.splitext(fn)[0]
            self.sounds[base_fn] = pygame.mixer.Sound(os.path.join('assets', 'sounds', fn))

    def play_music(self, name):
        for fn in os.listdir(os.path.join('assets', 'music')):
            base_fn = os.path.splitext(fn)[0]
            if base_fn == name:
                pygame.mixer.music.load(os.path.join('assets', 'music', fn))
                pygame.mixer.music.play(-1)
                break
        else:
            raise ValueError(f"No music '{name}' found")

    def stop_music(self):
        pygame.mixer.music.stop()


assets_manager = AssetsManager()
