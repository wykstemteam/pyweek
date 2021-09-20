import math

import numpy as np
import pygame
from skimage import io, transform


class Building(pygame.sprite.Sprite):
    def shear(self, img: np.ndarray, bottom_shear_right: float):
        img = img.astype('float32') / 255.0
        img = img.swapaxes(0, 1)

        affine_transform = transform.AffineTransform(shear=math.atan(bottom_shear_right / self.height))
        modified_image = transform.warp(img, affine_transform) * 255.0
        io.imshow(modified_image)
        io.show()

        modified_image = modified_image.swapaxes(0, 1)
        return modified_image.astype('int32')

    def __init__(self, image: pygame.Surface, bottom_shear_right: float, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.height = image.get_height()

        pixels = np.dstack((
            pygame.surfarray.pixels_red(image),
            pygame.surfarray.pixels_green(image),
            pygame.surfarray.pixels_blue(image),
            pygame.surfarray.pixels_alpha(image),
        )).astype('float32')
        pixels /= 255.0
        pixels = pixels.swapaxes(0, 1)
        affine_transform = transform.AffineTransform(shear=math.atan(bottom_shear_right / self.height))

        modified_image = transform.warp(pixels, affine_transform)
        modified_image *= 255.0
        modified_image = modified_image.astype('int32')
        modified_image = modified_image.swapaxes(0, 1)

        self.image = pygame.surfarray.make_surface(modified_image[:, :, :-1])
        self.image.set_colorkey((0, 0, 0))  # black shits are transparent
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
