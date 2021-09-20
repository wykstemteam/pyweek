import math

import numpy as np
import pygame

from game.assets_manager import AssetsManager
from game.constants import *
from game.sprites import Player, Road

assets_manager = AssetsManager()


def main():
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    assets_manager.images['road'] = pygame.transform.scale(
        assets_manager.images['road'], (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    roads = pygame.sprite.Group(
        Road(assets_manager.images['road'], 0, 0),
        Road(assets_manager.images['road'], SCREEN_WIDTH, 0),
    )
    assets_manager.images['player'] = pygame.transform.scale(
        assets_manager.images['player'],
        (PLAYER_WIDTH, PLAYER_HEIGHT)
    )
    player = Player(
        assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    clock = pygame.time.Clock()

    running = True
    while running:
        t = clock.get_time()
        t = t // 10

        roads.update(BACKGROUND_SPEED, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # FIXME: @Letser this is indistinguishable from losing
                # Press close button won't close the game and go to losing screen
                running = False

        player.update(t)  # code copied to player.py

        if not player.in_bounds():
            running = False

        roads.draw(window)
        window.blit(player.image, player.rect)
        pygame.display.flip()

        clock.tick(60)

    lose = True
    while lose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lose = False

        roads.draw(window)
        window.blit(player.image, player.rect)
        window.blit(assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
        pygame.display.flip()
