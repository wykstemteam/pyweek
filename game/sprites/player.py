import numpy as np
import pygame

from game.constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vx = -BACKGROUND_VELOCITY
        self.vy = 0.0
        self.dir = 0.0

    def acc(self, dx, dy):
        self.vx = min(self.vx + dx, PLAYER_MAX_HORI_SPEED)
        self.vy += dy

    def update(self, t):
        x = pygame.mouse.get_pos()[0] - (self.rect.left + PLAYER_WIDTH / 2)
        y = (self.rect.top + PLAYER_HEIGHT / 2) - pygame.mouse.get_pos()[1]
        self.dir = np.arctan2(y, x)

        keys = pygame.key.get_pressed()
        if self.rect.left < 0:  # touches left border
            self.rect.left = 0
            self.vx = -BACKGROUND_VELOCITY
        if self.rect.left < SCREEN_WIDTH - PLAYER_WIDTH // 2:
            if keys[pygame.K_w]:
                self.acc(0, -PLAYER_ACC)
            if keys[pygame.K_s]:
                self.acc(0, PLAYER_ACC)
            if keys[pygame.K_d]:
                self.acc(PLAYER_ACC, 0)
            if keys[pygame.K_a]:
                self.acc(-PLAYER_ACC, 0)
        else:  # touches right border
            self.rect.left = SCREEN_WIDTH - PLAYER_WIDTH // 2
            self.vx = -BACKGROUND_VELOCITY

        if self.vx > 0:
            self.vx = max(0, self.vx - FRICTION_HORI)
        elif self.vx < 0:
            self.vx = min(0, self.vx + FRICTION_HORI)

        if self.vy > 0:
            self.vy = max(0, self.vy - FRICTION_VERT)
        elif self.vy < 0:
            self.vy = min(0, self.vy + FRICTION_VERT)

        self.rect.left += (self.vx + BACKGROUND_VELOCITY) * t
        self.rect.top += self.vy * t

    def in_bounds(self):
        return 0 < self.rect.top < SCREEN_HEIGHT - PLAYER_HEIGHT
