import pygame

from game.constants import *


class RoundCounter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(FONT_PATH, 40)
        self.rounds_survived = 0
        self.image_shadow = None
        self.update()
        self.rect = self.image.get_rect()
        self.rect.topleft = (420, 50)

    def update(self):
        self.image = self.font.render(
            f'Rounds survived: {self.rounds_survived}', True, (255, 255, 0)
        )
        self.image_shadow = self.font.render(
            f'Rounds survived: {self.rounds_survived}', True, (0, 0, 0)
        )

    def draw(self, window: pygame.Surface):
        for di in range(-1, 2):
            for dj in range(-1, 2):
                window.blit(self.image_shadow, self.rect.move(di * 2, dj * 2))
        window.blit(self.image, self.rect)

    def increment(self):
        self.rounds_survived += 1
        self.update()
