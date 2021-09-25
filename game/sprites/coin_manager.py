import random

import pygame

from game.constants import *
from game.sprites.coin import Coin


class CoinManager(pygame.sprite.Sprite):
    def __init__(self, player_collision_group) -> None:
        super().__init__()

        self.coins = pygame.sprite.Group()
        self.coin_t = COIN_APPEAR_INTERVAL / 2

        self.player_collision_group = player_collision_group
        self.reached_checkpoint = False

    def update(self, t: float) -> None:
        self.coin_t -= t
        if self.coin_t <= 0 and not self.reached_checkpoint:
            new_coin = Coin(
                (
                    SCREEN_WIDTH + COIN_WIDTH,
                    random.randint(
                        BUILDING_HEIGHT + COIN_WIDTH / 2, SCREEN_HEIGHT - COIN_WIDTH / 2
                    )
                )
            )
            self.coins.add(new_coin)
            self.player_collision_group.add(new_coin)
            self.coin_t = COIN_APPEAR_INTERVAL
        self.coins.update(t)

    def draw(self, window: pygame.Surface) -> None:
        for coin in self.coins:
            coin.draw(window)
