from typing import Tuple

import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *


def get_audio_controls(
    manager: pygame_gui.UIManager
) -> Tuple[pygame_gui.elements.UILabel, pygame_gui.elements.UIHorizontalSlider,
           pygame_gui.elements.UILabel, pygame_gui.elements.UIHorizontalSlider]:
    music_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 25), (400, 10)),
        text='Music Volume',
        manager=manager
    )
    music_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 15), (400, 30)),
        start_value=assets_manager.music_volume,
        value_range=(0.0, 1.0),
        manager=manager
    )
    sound_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20), (400, 10)),
        text='Sound Volume',
        manager=manager
    )
    sound_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 30), (400, 30)),
        start_value=assets_manager.sound_volume,
        value_range=(0.0, 1.0),
        manager=manager
    )
    return music_label, music_slider, sound_label, sound_slider


def settings(window: pygame.Surface) -> None:
    settings_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
    return_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 75), (220, 50)), text='Return to Menu', manager=settings_screen
    )
    music_label, music_slider, sound_label, sound_slider = get_audio_controls(settings_screen)

    clock = pygame.time.Clock()

    running = True
    while running:
        t = clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.USEREVENT:
                if (
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED
                    and event.ui_element == return_button
                ):
                    running = False
                elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
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
