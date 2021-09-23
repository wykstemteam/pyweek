import numpy as np
import pygame

from game.constants import *
from game.sprites.player import Player


class Arrow(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, player: Player) -> None:
        super().__init__()
        self.original_image = image
        self.update(player)

    def update(self, player: Player) -> None:
        self.image = pygame.transform.rotate(self.original_image, player.dir * 360 // (2 * np.pi))
        self.rect = self.image.get_rect(
            center=self.original_image.get_rect(
                center=(
                    player.rect.left + (PLAYER_WIDTH / 2), player.rect.top + (PLAYER_HEIGHT / 2)
                )
            ).center
        )
        self.rect.left += np.cos(player.dir) * 150
        self.rect.top -= np.sin(player.dir) * 150

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
