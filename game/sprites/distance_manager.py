import pygame

from game.constants import *


class DistanceManager(pygame.sprite.Sprite):
    font = pygame.font.SysFont('Comic Sans MS', 50)

    def __init__(self):
        super().__init__()
        self.dist = 0.0
        self.dist_to_next_country = INITIAL_DISTANCE_TO_NEXT_COUNTRY
        self.update(0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (500, 20)

    def update(self, t):
        self.dist += -BACKGROUND_VELOCITY * t / 100
        self.dist_to_next_country -= -BACKGROUND_VELOCITY * t / 100
        self.dist_to_next_country = max(0.0, self.dist_to_next_country)
        self.image = self.font.render(
            f'Distance to next country: {self.dist_to_next_country: .0f} m', False, (255, 255, 0)
        )

    def draw(self, window: pygame.Surface):
        window.blit(self.image, self.rect)