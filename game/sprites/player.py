import pygame

from game.constants import *


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

    def update(self, t):
        keys = pygame.key.get_pressed()
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.left < SCREEN_WIDTH - PLAYER_WIDTH // 2:
            if keys[pygame.K_w]:
                self.acc(0, -PLAYER_ACC)
            if keys[pygame.K_s]:
                self.acc(0, PLAYER_ACC)
            if keys[pygame.K_d]:
                self.acc(PLAYER_ACC, 0)
            if keys[pygame.K_a]:
                self.acc(-PLAYER_ACC, 0)
        else:
            self.rect.left = SCREEN_WIDTH - PLAYER_WIDTH // 2

        if self.vx > BACKGROUND_SPEED:
            self.vx = max(BACKGROUND_SPEED, self.vx - FRICTION)
        elif self.vx < BACKGROUND_SPEED:
            self.vx = min(BACKGROUND_SPEED, self.vx + FRICTION)

        if self.vy > 0:
            self.vy = max(0, self.vy - FRICTION)
        elif self.vy < 0:
            self.vy = min(0, self.vy + FRICTION)

        self.rect.left += self.vx * t
        self.rect.top += self.vy * t

    def in_bounds(self):
        return 0 < self.rect.top < SCREEN_HEIGHT - PLAYER_HEIGHT
