import pygame
import pygame_gui

from game.constants import *


def settings(window: pygame.Surface):
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

            if (
                event.type == pygame.USEREVENT
                and event.user_type == pygame_gui.UI_BUTTON_PRESSED
                and event.ui_element == return_button
            ):
                running = False

            settings_screen.process_events(event)
        settings_screen.update(t)

        window.fill((100, 100, 100))
        settings_screen.draw_ui(window)
        pygame.display.flip()

        clock.tick(60)
