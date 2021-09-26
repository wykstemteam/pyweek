import pygame
from pygame.rect import Rect

from game.constants import *


class DistanceManager(pygame.sprite.Sprite):
    font = pygame.font.Font(FONT_PATH, 40)

    def __init__(self, game) -> None:
        super().__init__()
        self.dist = 0.0
        self.dist_to_next_country = INITIAL_DISTANCE_TO_NEXT_COUNTRY
        self.last_dist = 0
        self.rect = Rect(0, 0, 0, 0)
        self.rect.topleft = (420, 0)
        self.game = game

    def update(self, t: float) -> None:
        self.dist += -BACKGROUND_VELOCITY * t / 100 * DIST_SPD
        if self.last_dist < int(self.dist):
            self.game.add_dist_score(int(self.dist) - self.last_dist)
            self.last_dist = int(self.dist)
        self.dist_to_next_country -= -BACKGROUND_VELOCITY * t / 100 * DIST_SPD
        self.dist_to_next_country = max(0.0, self.dist_to_next_country)
        self.image = self.font.render(
            f'Next shop in {self.dist_to_next_country:.0f} m', True, (255, 255, 0)
        )
        self.outline_image = self.font.render(
            f'Next shop in {self.dist_to_next_country:.0f} m', True, (0, 0, 0)
        )

    def draw(self, window: pygame.Surface) -> None:
        di = -1
        while di <= 1:
            dj = -1
            while dj <= 1:
                window.blit(self.outline_image, self.rect.move(di * 3, dj * 3))
                dj += 1
            di += 1
        window.blit(self.image, self.rect)
