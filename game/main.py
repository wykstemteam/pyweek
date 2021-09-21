import math

import numpy as np
import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Player, PoliceCar, Road, ObstacleManager, BuildingManager

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
    policecar = PoliceCar(
        assets_manager.images['policecar'], (20, 280), assets_manager.images['bullet'])
    player = Player(
        assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    buildings = BuildingManager()  # copied code to building.py
    obstacle_manager = ObstacleManager()
    clock = pygame.time.Clock()

    running = True
    lose = False
    while running:
        t = clock.get_time()

        # event process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == restart_button:
                        player = Player(
                            assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        lose = False
            lose_screen.process_events(event)

        # update
        if not lose:
            roads.update(t / 1000)
            player.update(t / 1000)
            policecar.update(t / 1000)
            buildings.update(t / 1000)
            obstacle_manager.update(t/1000)

        if not player.in_bounds():
            lose = True
        lose_screen.update(t / 1000.0)

        rotated_arrow = pygame.transform.rotate(assets_manager.images['arrow'], player.dir * 360 // (2 * np.pi) )
        new_arrow = rotated_arrow.get_rect(center = assets_manager.images['arrow'].get_rect(center = (player.rect.left + (PLAYER_WIDTH / 2) , player.rect.top + (PLAYER_HEIGHT / 2))).center)
        new_arrow.left += np.cos(player.dir) * 150
        new_arrow.top -= np.sin(player.dir) * 150

        # draw
        roads.draw(window)
        buildings.draw(window)
        policecar.draw(window)
        obstacle_manager.draw(window)
        window.blit(player.image, player.rect)
        window.blit(rotated_arrow, new_arrow)
        if lose:
            window.blit(
                assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
            window.blit(
                assets_manager.images['GameOver'], pygame.Rect(0, 0, 0, 0))
            lose_screen.draw_ui(window)
        pygame.display.flip()

        clock.tick(60)
        print(f'fps = {0 if t == 0 else 1000/t}')


def main():
    title_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100),
            (200, 50)
        ),
        text='Start',
        manager=title_screen
    )

    running = True
    cock = pygame.time.Clock()
    while running:
        t = cock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        gaming()
        title_screen.process_events(event)
        title_screen.update(t / 1000.0)

        window.fill((100, 100, 100))
        title_screen.draw_ui(window)
        pygame.display.flip()

        cock.tick(60)
