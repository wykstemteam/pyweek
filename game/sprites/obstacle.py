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
        self.pos = pygame.Vector2(pos)

    def update(self, t) -> None:
        self.pos.x += BACKGROUND_VELOCITY * t
        self.rect.left = self.pos.x
        if self.rect.left <= 0:
            self.kill()
            return

    def player_hit(self, player) -> None:  # should be called when collided by player
        # animation
        #
        pass
