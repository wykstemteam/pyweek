from typing import List

import pygame

from game.constants import *


def _get_location(i) -> pygame.Rect:
    return pygame.Rect(INVENTORY_X + (ITEM_WIDTH + INVENTORY_BOX_SEPARATION) * i, INVENTORY_Y,
                       ITEM_WIDTH, ITEM_HEIGHT)


class Inventory:
    def __init__(self, images: List[pygame.Surface], game) -> None:
        self.images = images
        self.game = game

    def draw(self, window: pygame.Surface) -> None:
        for i in range(2):
            pygame.draw.rect(
                window, 0xFF0000 if self.game.player.holding == i+1 else 0xFFFFFF,
                _get_location(i),
                INVENTORY_BOX_THICKNESS,
            )
        for i, j in self.game.player.items.items():
            window.blit(self.images[j], _get_location(i-1))
