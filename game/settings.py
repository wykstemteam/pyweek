import json
from typing import Tuple

import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *


def get_controls(
    manager: pygame_gui.UIManager
) -> Tuple[pygame_gui.elements.UILabel, pygame_gui.elements.UIHorizontalSlider,
           pygame_gui.elements.UILabel, pygame_gui.elements.UIHorizontalSlider]:
    music_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 75), (400, 20)),
        text='Music Volume',
        manager=manager
    )
    music_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 57), (400, 30)),
        start_value=assets_manager.music_volume,
        value_range=(0.0, 1.0),
        manager=manager
    )
    sound_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 20), (400, 20)),
        text='Sound Volume',
        manager=manager
    )
    sound_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 2), (400, 30)),
        start_value=assets_manager.sound_volume,
        value_range=(0.0, 1.0),
        manager=manager
    )
    quotes_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 185, SCREEN_HEIGHT // 2 + 35), (370, 50)),
        object_id='#quotes',
        text="President Xi quotes: Disabled",
        manager=manager
    )

    update_quotes_button(quotes_button)
    return music_label, music_slider, sound_label, sound_slider, quotes_button


def update_quotes_button(button: pygame_gui.elements.UIButton) -> None:
    with open("menu_theme.json") as f:
        data = json.load(f)

    if assets_manager.play_quotes:
        button.set_text("President Xi quotes: Enabled")
        data["#quotes"]["colours"]["normal_bg"] = "#3465a4"
        data["#quotes"]["colours"]["hovered_bg"] = "#2f5b94"
    else:
        button.set_text("President Xi quotes: Disabled")
        with open("menu_theme.json") as f:
            data = json.load(f)
        data["#quotes"]["colours"]["normal_bg"] = "#e43d40"
        data["#quotes"]["colours"]["hovered_bg"] = "#e23034"

    with open("menu_theme.json", "w") as f:
        json.dump(data, f, indent=4)


def settings(window: pygame.Surface) -> None:
    settings_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
    return_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 90), (220, 50)),
        text='Return to Menu',
        manager=settings_screen
    )
    music_label, music_slider, sound_label, sound_slider, quotes_button = get_controls(
        manager=settings_screen
    )

    clock = pygame.time.Clock()

    running = True
    while running:
        t = clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == return_button:
                        running = False
                    elif event.ui_element == quotes_button:
                        assets_manager.play_quotes = not assets_manager.play_quotes
                        update_quotes_button(quotes_button)
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
