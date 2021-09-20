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
