import pygame

pygame.init()

import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.game import Game
from game.settings import settings
import game.introduction

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rock: The Criminal")


def gaming() -> None:
    game = Game()
    game.run(window)


def main() -> None:
    game.introduction.run(window)
    title_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
    settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100), (200, 50)),
        text='Settings',
        manager=title_screen
    )
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (200, 50)),
        text='Start',
        manager=title_screen
    )

    assets_manager.play_music("boys_summer_vacation")
    running = True
    cock = pygame.time.Clock()
    while running:
        t = cock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    gaming()
                    assets_manager.play_music("boys_summer_vacation")
                elif event.ui_element == settings_button:
                    settings(window)

            title_screen.process_events(event)
        title_screen.update(t / 1000)

        window.fill((100, 100, 100))
        title_screen.draw_ui(window)
        pygame.display.flip()

        cock.tick(60)
