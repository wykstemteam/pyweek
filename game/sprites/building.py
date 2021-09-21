import numpy as np
import pygame
from skimage import transform

from game.constants import *


class Building(pygame.sprite.Sprite):
    def shear(self, bottom_shear_right: float):
        image = np.dstack((
            pygame.surfarray.pixels_red(self.image),
            pygame.surfarray.pixels_green(self.image),
            pygame.surfarray.pixels_blue(self.image),
        )).astype('float32') / 255.0
        image = image.swapaxes(0, 1)
        shear_matrix = np.array([[1, abs(bottom_shear_right) / self.image.get_height(), 0],
                                 [0, 1, 0],
                                 [0, 0, 1]])
        image = transform.warp(
            image, np.linalg.inv(shear_matrix), output_shape=(
                self.image.get_height(), self.image.get_width() + int(abs(bottom_shear_right)))
        ) * 255.0
        image = image.swapaxes(0, 1)
        self.image = pygame.surfarray.make_surface(image.astype('int32'))
        if bottom_shear_right < 0:
            self.image = pygame.transform.flip(self.image, True, False)  # flips image horizontally

    def __init__(self, image: pygame.Surface, bottom_shear_right: float, x: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.shear(bottom_shear_right)
        self.image.set_colorkey((0, 0, 0))  # black shits are transparent
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)
        if bottom_shear_right < 0:
            self.rect.left += bottom_shear_right

    def update(self, dx: int, rightmost: int):
        self.shear(dx * BUILDING_RATIO)
        self.rect.left += dx
        # if self.rect.right < 0:



