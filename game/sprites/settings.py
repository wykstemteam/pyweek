import numpy as np
import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import BuildingManager, ObstacleManager, Player, PoliceCar, Road, Warn

def Settings():
    running = True

    settings_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    return_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (10, 10), (100, 50)
        ),
        text='Return',
        manager=settings_screen
    )

    clock = pygame.time.Clock()

    while running:
        t = clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == return_button:
                        running = False

            settings_screen.process_events(event)
        settings_screen.update(t)

        # window.fill((100, 100, 100))
        # settings_screen.draw_ui(window)
        pygame.display.flip()

        clock.tick(60)
