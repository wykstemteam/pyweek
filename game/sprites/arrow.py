import numpy as np
import pygame

from game.constants import *
from game.sprites.player import Player


class Arrow(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, player: Player) -> None:
        super().__init__()
        self.original_image = image
        self.player = player
        self.update()

    def update(self) -> None:
        if self.player.items[self.player.holding] != 5:
            return
        self.image = pygame.transform.rotate(
            self.original_image, self.player.dir * 360 // (2 * np.pi)
        )
        self.rect = self.image.get_rect(
            center=self.original_image.get_rect(
                center=(
                    self.player.rect.left + (PLAYER_WIDTH / 2),
                    self.player.rect.top + (PLAYER_HEIGHT / 2)
                )
            ).center
        )
        self.rect.left += np.cos(self.player.dir) * 150
        self.rect.top -= np.sin(self.player.dir) * 150

    def draw(self, window: pygame.Surface) -> None:
        if self.player.items[self.player.holding] != 5:
            return
        window.blit(self.image, self.rect)
