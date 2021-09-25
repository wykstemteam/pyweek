from typing import List

import pygame

from game.constants import *


def _get_location(i) -> pygame.Rect:
    return pygame.Rect(INVENTORY_X + (ITEM_WIDTH + INVENTORY_BOX_SEPARATION) * i, INVENTORY_Y,
                       ITEM_WIDTH, ITEM_HEIGHT)


class Inventory:
    def __init__(self, images: List[pygame.Surface]) -> None:
        self.images = images
        self.current_items = []

    def add(self, index: int) -> None:
        self.current_items.append(index)

    def draw(self, window: pygame.Surface) -> None:
        for i in range(2):
            pygame.draw.rect(
                window, (255, 255, 255),
                _get_location(i),
                INVENTORY_BOX_THICKNESS,
            )
        for i, j in enumerate(self.current_items):
            window.blit(self.images[j], _get_location(i))
