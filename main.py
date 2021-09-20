import math

import numpy as np
import pygame
from skimage import io
from skimage import transform

from assets_manager import AssetsManager
from constants import *

assets_manager = AssetsManager()


class Road(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, dx: int, dy: int):
        self.rect.left += dx
        if self.rect.left > self.width:
            self.rect.left -= self.width * 2
        elif self.rect.right < 0:
            self.rect.left += self.width * 2
        self.rect.top += dy
        if self.rect.top > self.height:
            self.rect.top -= self.height * 2
        elif self.rect.bottom < 0:
            self.rect.top += self.height * 2


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


class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vx = 0.0
        self.vy = 0.0

    def acc(self, dx, dy):
        self.vx += dx
        self.vy += dy

    def friction(self):
        if self.vx > BACKGROUND_SPEED:
            self.vx = max(BACKGROUND_SPEED, self.vx - FRICTION)
        elif self.vx < BACKGROUND_SPEED:
            self.vx = min(BACKGROUND_SPEED, self.vx + FRICTION)

        if self.vy > 0:
            self.vy = max(0, self.vy - FRICTION)
        elif self.vy < 0:
            self.vy = min(0, self.vy + FRICTION)

    def update_pos(self, t):
        self.rect.left += self.vx * t
        self.rect.top += self.vy * t


def main():
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    assets_manager.images['road'] = pygame.transform.scale(
        assets_manager.images['road'], (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    roads = pygame.sprite.Group(
        Road(assets_manager.images['road'], 0, 0),
        Road(assets_manager.images['road'], SCREEN_WIDTH, 0),
    )
    assets_manager.images['player'] = pygame.transform.scale(
        assets_manager.images['player'],
        (PLAYER_WIDTH, PLAYER_HEIGHT)
    )
    player = Player(assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    clock = pygame.time.Clock()

    running = True
    while running:
        t = clock.get_time()
        t = t // 10

        roads.update(BACKGROUND_SPEED, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if player.rect.left < SCREEN_WIDTH - PLAYER_WIDTH // 2:
            if keys[pygame.K_w]:
                player.acc(0, -PLAYER_ACC)
            if keys[pygame.K_s]:
                player.acc(0, PLAYER_ACC)
            if keys[pygame.K_d]:
                player.acc(PLAYER_ACC, 0)
            if keys[pygame.K_a]:
                player.acc(-PLAYER_ACC, 0)
        else:
            player.rect.left = SCREEN_WIDTH - PLAYER_WIDTH // 2

        if player.rect.top <= 0:
            running = False
        elif player.rect.top >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            running = False

        player.friction()
        player.update_pos(t)

        roads.draw(window)
        window.blit(player.image, player.rect)
        pygame.display.flip()

        clock.tick(60)

    lose = True
    while lose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lose = False

        roads.draw(window)
        window.blit(player.image, player.rect)
        window.blit(assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
