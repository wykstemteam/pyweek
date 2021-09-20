import os

import pygame


class AssetsManager:
    def __init__(self):
        self.images = {}
        for fn in os.listdir(os.path.join('assets', 'images')):
            base_fn = os.path.splitext(fn)[1]
            self.images[base_fn] = pygame.image.load(os.path.join('assets', 'images', fn))
