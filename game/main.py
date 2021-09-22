import math

import numpy as np
import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Player, PoliceCar, Road, ObstacleManager, BuildingManager, Warn, Game

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def gaming():
    game = Game()

    clock = pygame.time.Clock()

    running = True
    lose = False
    while running:
        t = clock.get_time()

        # event process
        game.event_process()

        # update
        game.update(t/1000)

        # draw
        game.draw(window)
        pygame.display.flip()

        clock.tick(60)
        if SHOW_FPS:
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

    assets_manager.play_music("tanukichis_adventure")
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
