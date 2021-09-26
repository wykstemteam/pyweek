import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *


def settings(window: pygame.Surface):
    settings_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
    return_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 10), (100, 50)), text='Return', manager=settings_screen
    )
    music_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 25), (400, 10)),
        text='Music Volume',
        manager=settings_screen
    )
    music_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 15), (400, 30)),
        start_value=assets_manager.music_volume,
        value_range=(0.0, 1),
        manager=settings_screen
    )

    sound_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20), (400, 10)),
        text='Sound Volume',
        manager=settings_screen
    )
    sound_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 30), (400, 30)),
        start_value=assets_manager.sound_volume,
        value_range=(0.0, 1),
        manager=settings_screen
    )

    clock = pygame.time.Clock()

    running = True
    while running:
        t = clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if (
                event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED
                and event.ui_element == return_button
            ):
                running = False
            if (
                event.type == pygame.USEREVENT
                and event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED
            ):
                if event.ui_element == music_slider:
                    assets_manager.set_music_volume(event.value)
                elif event.ui_element == sound_slider:
                    assets_manager.set_sound_volume(event.value)

            settings_screen.process_events(event)
        settings_screen.update(t)

        window.fill((100, 100, 100))
        settings_screen.draw_ui(window)
        pygame.display.flip()

        clock.tick(60)
