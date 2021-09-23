import pygame
pygame.init()

import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.game import Game
from game.settings import settings

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def gaming() -> None:
    game = Game()
    clock = pygame.time.Clock()

    running = True
    while running:
        t = clock.get_time()

        if game.event_process(window):  # Returns True if stop gaming
            running = False

        game.update(t / 1000)
        game.draw(window)
        pygame.display.flip()
        clock.tick(60)

        if SHOW_FPS:
            print(f'fps = {0 if t == 0 else 1000 / t}')


def main() -> None:
    title_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    assets_manager.play_music("tanukichis_adventure")
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
                    assets_manager.play_music("tanukichis_adventure")
                elif event.ui_element == settings_button:
                    settings(window)

            title_screen.process_events(event)
        title_screen.update(t / 1000)

        window.fill((100, 100, 100))
        title_screen.draw_ui(window)
        pygame.display.flip()

        cock.tick(60)
