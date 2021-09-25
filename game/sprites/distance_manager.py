import pygame
from pygame.rect import Rect

from game.constants import *


class DistanceManager(pygame.sprite.Sprite):
    # TODO: Maybe consider another font
    font = pygame.font.SysFont('Comic Sans MS', 50)

    def __init__(self) -> None:
        super().__init__()
        self.dist = 0.0
        self.dist_to_next_country = INITIAL_DISTANCE_TO_NEXT_COUNTRY
        self.update(0)
        self.rect = Rect(0, 0, 0, 0)
        self.rect.topleft = (500, 20)

    def update(self, t: float) -> None:
        self.dist += -BACKGROUND_VELOCITY * t / 100 * DIST_SPD
        self.dist_to_next_country -= -BACKGROUND_VELOCITY * t / 100 * DIST_SPD
        self.dist_to_next_country = max(0.0, self.dist_to_next_country)
        self.image = self.font.render(
            f'Distance to shop: {self.dist_to_next_country: .0f} m', False, (255, 255, 0)
        )
        self.outline_image = self.font.render(
            f'Distance to shop: {self.dist_to_next_country: .0f} m', False, (0, 0, 0)
        )

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.outline_image, self.rect.move(-3, 3))
        window.blit(self.outline_image, self.rect.move(-3, -3))
        window.blit(self.outline_image, self.rect.move(3, -3))
        window.blit(self.outline_image, self.rect.move(3, 3))
        window.blit(self.image, self.rect)
