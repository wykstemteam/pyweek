import math

import numpy as np
import pygame
import pygame_gui

from game.assets_manager import AssetsManager
from game.constants import *
from game.sprites import Building, Player, PoliceCar, Road

assets_manager = AssetsManager()
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def gaming():
    lose_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    restart_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100),
            (100, 50)
        ),
        text='Restart',
        manager=lose_screen
    )

    roads = pygame.sprite.Group(
        Road(assets_manager.images['road'], 0, BUILDING_HEIGHT),
        Road(assets_manager.images['road'], SCREEN_WIDTH, BUILDING_HEIGHT),
    )
    policecar = PoliceCar(assets_manager.images['policecar'], (20, 280), assets_manager.images['bullet'])
    player = Player(
        assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # should not be put in main
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
        buildings.add(Building(assets_manager.images[f'building{tp + 1}'], shear, x))
        shear += 2 * BUILDING_WIDTH / 3
        x -= BUILDING_WIDTH
        tp = (tp + 1) % 3

    x = SCREEN_WIDTH // 2 + BUILDING_WIDTH // 2
    shear = -2 * BUILDING_WIDTH / 3
    tp = 2
    while x + shear < SCREEN_WIDTH:
        buildings.add(Building(assets_manager.images[f'building{tp + 1}'], shear, x))
        shear -= 2 * BUILDING_WIDTH / 3
        x += BUILDING_WIDTH
        tp = (tp - 1) % 3
    # /should not be put in main

    clock = pygame.time.Clock()

    running = True
    lose = False
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
        if not lose:
            roads.update(t/1000)
            player.update(t/1000)
            policecar.update(t/1000)

            if not player.in_bounds():
                lose = True
        lose_screen.update(t / 1000.0)

        # draw
        roads.draw(window)
        buildings.draw(window)
        policecar.draw(window)
        window.blit(player.image, player.rect)
        if lose:
            window.blit(assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
            window.blit(assets_manager.images['GameOver'], pygame.Rect(0, 0, 0, 0))
            lose_screen.draw_ui(window)
        pygame.display.flip()

        clock.tick(60)


def main():

    running = True
    cock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            gaming()
        cock.tick(60)

        window.fill((0, 0, 0))
        pygame.display.flip()

