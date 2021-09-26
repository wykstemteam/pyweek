import pygame

from game.assets_manager import assets_manager
from game.constants import *


class CoinGUI(pygame.sprite.Sprite):
    # TODO: Maybe consider another font
    font = pygame.font.SysFont('arial', 50)

    def __init__(self, pos, game) -> None:
        super().__init__()
        self.image = assets_manager.animations['coin'][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.text_rect = self.rect.move(COIN_WIDTH * 1.2, -16)
        self.game = game

    def update(self, t: float) -> None:
        self.text_image = self.font.render(
            f'{self.game.coins}', True, (255, 255, 0)
        )
        self.outline_image = self.font.render(
            f'{self.game.coins}', True, (0, 0, 0)
        )

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
        window.blit(self.outline_image, self.text_rect.move(-3, 3))
        window.blit(self.outline_image, self.text_rect.move(-3, -3))
        window.blit(self.outline_image, self.text_rect.move(3, -3))
        window.blit(self.outline_image, self.text_rect.move(3, 3))
        window.blit(self.text_image, self.text_rect)
