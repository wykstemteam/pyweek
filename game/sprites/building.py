import random
import numpy as np
import pygame
from skimage import io, transform

from game.assets_manager import assets_manager
from game.constants import *


class Building(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, bottom_shear_right: float, x: int):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.shear(bottom_shear_right)
        self.total_sheared = bottom_shear_right
        self.rect.topleft = (x, 0)
        if bottom_shear_right < 0:
            self.rect.left += bottom_shear_right

    def shear(self, bottom_shear_right: float):
        image = np.dstack((
            pygame.surfarray.pixels_red(self.original_image),
            pygame.surfarray.pixels_green(self.original_image),
            pygame.surfarray.pixels_blue(self.original_image),
        )).astype('float32') / 255.0
        image = image.swapaxes(0, 1)
        shear_matrix = np.array([[1, abs(bottom_shear_right) / self.original_image.get_height(), 0],
                                 [0, 1, 0],
                                 [0, 0, 1]])
        image = transform.warp(
            image, np.linalg.inv(shear_matrix), output_shape=(
                self.original_image.get_height(), self.original_image.get_width() + int(abs(bottom_shear_right)))
        ) * 255.0
        image = image.swapaxes(0, 1)
        self.image = pygame.surfarray.make_surface(image.astype('int8'))
        if bottom_shear_right < 0:
            self.image = pygame.transform.flip(
                self.image, True, False)  # flips image horizontally
        self.image.set_colorkey((0, 0, 0))  # black shits are transparent
        self.rect.size = self.image.get_size()

    def update(self, dx: int):
        self.total_sheared -= dx * BUILDING_RATIO
        self.shear(self.total_sheared)
        if self.total_sheared < 0:
            self.rect.left += dx
        else:
            self.rect.left += dx * (1 + BUILDING_RATIO)
        if self.rect.right < 0:
            self.kill()
