import math

import numpy as np
import pygame
from pygame.constants import K_SPACE
import pygame_gui

from game.assets_manager import AssetsManager
from game.constants import *
from game.sprites import Player, Road, PoliceCar, Building

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

    for i in range(1, 4):  # building 1-3
        assets_manager.images[f'building{i}'] = pygame.transform.scale(
            assets_manager.images[f'building{i}'],
            (BUILDING_WIDTH, BUILDING_HEIGHT),
        )
    buildings = pygame.sprite.Group()
    x = SCREEN_WIDTH // 2 - BUILDING_WIDTH // 2
    shear = 0
    tp = 0
    while x + BUILDING_WIDTH + shear >= 0:
        buildings.add(Building(assets_manager.images[f'building{tp+1}'], shear, x, 0))
        shear += 2 * BUILDING_WIDTH / 3
        x -= BUILDING_WIDTH
        tp = (tp + 1) % 3

    x = SCREEN_WIDTH // 2 + BUILDING_WIDTH // 2
    shear = -2 * BUILDING_WIDTH / 3
    tp = 2
    while x + shear < SCREEN_WIDTH:
        buildings.add(Building(assets_manager.images[f'building{tp+1}'], shear, x, 0))
        shear -= 2 * BUILDING_WIDTH / 3
        x += BUILDING_WIDTH
        tp = (tp - 1) % 3

    clock = pygame.time.Clock()

    running = True
    while running:
        t = clock.get_time()

        # event process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == restart_button:
                        player = Player(
                            assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        lose = False
            lose_screen.process_events(event)

        # update
        if lose == False:
            roads.update(BACKGROUND_SPEED, 0)
            player.update(t//10)  # code copied to player.py

            if not player.in_bounds():
                lose = True
        lose_screen.update(t // 1000.0)

        # draw
        roads.draw(window)
        buildings.draw(window)
        window.blit(policecar.image, policecar.rect)
        window.blit(player.image, player.rect)
        pygame.display.flip()

        clock.tick(60)


def main():

    running = True
    cock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lose = False

        roads.draw(window)
        window.blit(player.image, player.rect)
        window.blit(assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
        pygame.display.flip()
