import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.settings import settings
from game.sprites import *

title_font = pygame.font.SysFont('Castellar', 30, True)
instruction_font = pygame.font.SysFont('Comic Sans MS', 30)


def instruction(text: str):
    return instruction_font.render(text, False, (255, 255, 255))


def run(window: pygame.Surface):
    assets_manager.play_music("boys_summer_vacation")
    assets_manager.play_sound("hi")
    screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
    settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH - 200 - 50, SCREEN_HEIGHT - 50 - 50), (200, 50)),
        text='Settings',
        manager=screen,
    )

    running = True
    cock = pygame.time.Clock()
    buildings = BuildingManager()
    roads = pygame.sprite.Group(
        Road(assets_manager.images['road'], 0),
        Road(assets_manager.images['road'], SCREEN_WIDTH),
    )
    title = title_font.render(
        'ESCAPE FROM COPS 2021 HD DELUXE PRO MAX ULTRA REMASTERED', False, (255, 255, 0)
    )
    instructions = [
        instruction('WASD to move'),
        instruction('1 and 2 to select item in inventory'),
        instruction('Left click mouse to use item'),
        instruction('Press any key to start'),
    ]
    police_car = assets_manager.images['policecar']
    bomber = assets_manager.animations['bomber'][0]
    motorbike = assets_manager.images['motorbike']

    while running:
        dt = cock.get_time() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                settings(window)
            screen.process_events(event)

        buildings.update(dt)
        roads.update(dt)
        screen.update(dt)

        window.fill((0, 0, 0))
        buildings.draw(window)
        roads.draw(window)
        window.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 0))
        window.blit(
            police_car, (
                50, BUILDING_HEIGHT +
                (SCREEN_HEIGHT - BUILDING_HEIGHT) // 2 - police_car.get_height() // 2
            )
        )
        window.blit(
            bomber, (
                300, BUILDING_HEIGHT +
                (SCREEN_HEIGHT - BUILDING_HEIGHT) // 2 - bomber.get_height() // 2
            )
        )
        window.blit(
            motorbike, (
                1000, BUILDING_HEIGHT +
                (SCREEN_HEIGHT - BUILDING_HEIGHT) // 2 - motorbike.get_height() // 2
            )
        )
        for i in range(len(instructions)):
            window.blit(
                instructions[i], (
                    20, SCREEN_HEIGHT - 50 - instructions[i].get_height() *
                    (len(instructions) - i - 1)
                )
            )
        screen.draw_ui(window)

        pygame.display.flip()
        cock.tick(60)
