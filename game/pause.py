import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.settings import get_audio_controls


def run(window: pygame.Surface, game):
    previous_screen = window.copy()
    pause_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
    pause = True
    music_label, music_slider, sound_label, sound_slider = get_audio_controls(manager=pause_screen)
    continue_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 172, SCREEN_HEIGHT // 2 + 80), (130, 50)),
        text='Continue',
        manager=pause_screen
    )
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 28, SCREEN_HEIGHT // 2 + 80), (200, 50)),
        object_id='#exit_button',
        text='Exit to Menu',
        manager=pause_screen
    )
    font = pygame.font.SysFont('arial', 40)
    cock = pygame.time.Clock()
    while pause:
        dt = cock.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == music_slider:
                        assets_manager.set_music_volume(event.value)
                    elif event.ui_element == sound_slider:
                        assets_manager.set_sound_volume(event.value)
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == continue_button:
                        return False
                    elif event.ui_element == exit_button:
                        return True
            elif event.type == pygame.QUIT:
                exit()

            pause_screen.process_events(event)

        pause_screen.update(dt)
        window.blit(previous_screen, (0, 0))
        window.blit(assets_manager.images['darken'], (0, 0))
        pause_screen.draw_ui(window)
        score_image = font.render(
            f'Score: {game.score}', True, (255, 255, 255)
        )
        score_rect = score_image.get_rect()
        score_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100)
        window.blit(score_image, score_rect)

        pygame.display.flip()

        cock.tick(60)
