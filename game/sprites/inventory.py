from typing import List

import pygame

from game.constants import *


def _get_location(i, at_shop) -> pygame.Rect:
    if not at_shop:
        return pygame.Rect(
            INVENTORY_X + (ITEM_WIDTH + INVENTORY_BOX_SEPARATION) * i, INVENTORY_Y, ITEM_WIDTH,
            ITEM_HEIGHT
        )
    return pygame.Rect(
        INVENTORY_X_SHOP + (ITEM_WIDTH_SHOP + INVENTORY_BOX_SEPARATION) * i, INVENTORY_Y_SHOP,
        ITEM_WIDTH_SHOP, ITEM_HEIGHT_SHOP
    )


class Inventory:
    def __init__(self, images: List[pygame.Surface], game) -> None:
        self.images = images
        self.game = game
        self.at_shop = False

    def draw(self, window: pygame.Surface) -> None:
        for i in range(2):
            pygame.draw.rect(
                window,
                0xFF0000 if self.game.player.holding == i + 1 else 0xFFFFFF,
                _get_location(i, self.at_shop),
                INVENTORY_BOX_THICKNESS,
            )
        for i, j in self.game.player.items.items():
            window.blit(self.images[j], _get_location(i - 1, self.at_shop))
