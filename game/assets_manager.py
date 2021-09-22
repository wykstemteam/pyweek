import os

import pygame

from game.constants import *


class AssetsManager:
    def __init__(self) -> None:
        pygame.mixer.init()

        self.images = {}
        self.sounds = {}
        self.animations = {}

        self.init_images()
        # self.init_sounds()

    def init_images(self) -> None:
        for fn in os.listdir(os.path.join('assets', 'images')):
            base_fn = os.path.splitext(fn)[0]
            self.images[base_fn] = pygame.image.load(os.path.join('assets', 'images', fn))
        self.images['warning sign'] = pygame.transform.scale(
            self.images['warning sign'], (WARN_WIDTH, WARN_HEIGHT)
        )
        self.images['policecar'] = pygame.transform.scale(
            self.images['policecar'], (POLICECAR_WIDTH, POLICECAR_HEIGHT)
        )
        self.images['road'] = pygame.transform.scale(
            self.images['road'], (SCREEN_WIDTH, SCREEN_HEIGHT - BUILDING_HEIGHT)
        )
        self.images['GameOver'] = pygame.transform.scale(
            self.images['GameOver'], (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.images['bullet'] = pygame.transform.scale(
            self.images['bullet'], (BULLET_WIDTH, BULLET_HEIGHT)
        )
        self.images['3buildings'] = pygame.transform.scale(
            self.images['3buildings'], (BUILDING_WIDTH, BUILDING_HEIGHT)
        )
        self.images['motorbike'] = pygame.transform.scale(
            self.images['motorbike'], (PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        self.images['arrow'] = pygame.transform.scale(self.images['arrow'], (80, 100))
        for i in range(1, 4):
            self.images[f'obstacle{i}'] = pygame.transform.scale(
                self.images[f'obstacle{i}'], (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            )

    def init_sounds(self) -> None:
        for fn in os.listdir(os.path.join('assets', 'sounds')):
            base_fn = os.path.splitext(fn)[0]
            self.sounds[base_fn] = pygame.mixer.Sound(os.path.join('assets', 'sounds', fn))

    def init_animations(self) -> None:
        for dirname in os.listdir(os.path.join('assets', 'animations')):
            self.animations[dirname] = []
            for fn in os.listdir(dirname):
                self.animations[dirname].append(
                    pygame.transform.scale(
                        pygame.image.load(os.path.join('assets', 'animations', dirname, fn)),
                        (EXPLODE_WIDTH, EXPLODE_HEIGHT)
                    )
                )

    def play_music(self, name: str) -> None:
        for fn in os.listdir(os.path.join('assets', 'music')):
            base_fn = os.path.splitext(fn)[0]
            if base_fn == name:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(os.path.join('assets', 'music', fn))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)  # is work???
                break
        else:
            raise ValueError(f"No music '{name}' found")


assets_manager = AssetsManager()
