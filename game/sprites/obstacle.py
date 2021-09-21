import pygame

from game.constants import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, t):
        self.rect.left += BACKGROUND_VELOCITY * t
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.kill()
            return

    def hit(self):  # should be called when collided by someone
        # animation
        pass
