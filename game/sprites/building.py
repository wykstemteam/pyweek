import cv2 as cv
import numpy as np
import pygame
from matplotlib import pyplot as plt

from game.constants import *


class Building(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int):
        super().__init__()
        self.original_image = image
        self.flipped_image = pygame.transform.flip(image, True, False)
        self.image = image
        self.mid_x = x + BUILDING_WIDTH // 2
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)
        if self.sx < 0:
            self.rect.left += self.sx
        self.shear()

    @property
    def sx(self):
        return -(self.mid_x - SCREEN_WIDTH // 2) * (1 - BUILDING_RATIO)

    def shear(self):
        image = self.original_image if self.sx > 0 else self.flipped_image
        plt.imshow(pygame.surfarray.pixels3d(image))
        image = np.dstack((
            pygame.surfarray.pixels_red(image),
            pygame.surfarray.pixels_green(image),
            pygame.surfarray.pixels_blue(image),
        ))
        image = image.swapaxes(0, 1)
        shear_matrix = np.array([[1, abs(self.sx) / self.original_image.get_height(), 0],
                                 [0, 1, 0],
                                 [0, 0, 1]])
        image = cv.warpPerspective(image, shear_matrix, (
            self.original_image.get_width() + int(abs(self.sx)), self.original_image.get_height()))

        image = image.swapaxes(0, 1)

        self.image = pygame.surfarray.make_surface(image)
        if self.sx < 0:
            self.image = pygame.transform.flip(
                self.image, True, False)  # flips image horizontally
        self.image.set_colorkey((0, 0, 0))  # black shits are transparent
        self.rect.size = self.image.get_size()

    def update(self, dx: int):
        self.mid_x += dx
        self.shear()
        if self.sx > 0:
            self.rect.left += dx
        else:
            self.rect.left += int(dx * BUILDING_RATIO)
