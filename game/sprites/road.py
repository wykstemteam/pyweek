import pygame

from game.constants import BACKGROUND_VELOCITY


class Road(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, t: float):
        self.rect.left += int(BACKGROUND_VELOCITY * t)
        if self.rect.right < 0:
            self.rect.left += self.width * 2
