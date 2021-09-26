from typing import Tuple

import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.settings import settings
from game.sprites import *

title_font = pygame.font.SysFont('Corbel', 60, True)
instruction_font = pygame.font.SysFont('Comic Sans MS', 30)
instruction_height = instruction_font.render("test", True, (0, 0, 0)).get_height()

instructions = [
    'Move: WASD',
    'Select inventory slots: 1 and 2',
    'Use item: mouse left click',
    'Press any key to start',
]


def blit_outlined_text(
    window: pygame.Surface,
    font: pygame.font.SysFont,
    text: str,
    outline_size: int,
    outline_color: Tuple[int, int, int],
    color: Tuple[int, int, int],
    x: int,
    y: int,
    center: bool = False
) -> None:
    outline = font.render(text, True, outline_color)
    actual = font.render(text, True, color)
    if center:
        x -= actual.get_width() // 2
    window.blit(outline, (x - outline_size, y - outline_size))
    window.blit(outline, (x - outline_size, y + outline_size))
    window.blit(outline, (x + outline_size, y - outline_size))
    window.blit(outline, (x + outline_size, y + outline_size))
    window.blit(actual, (x, y))


def menu(window: pygame.Surface):
    assets_manager.play_music("tanukichis_adventure")
    if assets_manager.play_quotes:
        assets_manager.play_sound("hi")
    screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
    settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH - 200 - 50, SCREEN_HEIGHT - 50 - 50), (200, 50)),
        text='Settings',
        manager=screen
    )

    running = True
    cock = pygame.time.Clock()
    buildings = BuildingManager()
    roads = pygame.sprite.Group(
        Road(assets_manager.images['road'], 0),
        Road(assets_manager.images['road'], SCREEN_WIDTH),
    )
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
        blit_outlined_text(
            window=window,
            font=title_font,
            text="Rock: The Criminal",
            outline_size=2,
            outline_color=(0, 0, 0),
            color=(255, 255, 0),
            x=SCREEN_WIDTH // 2,
            y=10,
            center=True
        )
        for i in range(len(instructions)):
            blit_outlined_text(
                window=window,
                font=instruction_font,
                text=instructions[i],
                outline_size=1,
                outline_color=(0, 0, 0),
                color=(255, 255, 255),
                x=20,
                y=SCREEN_HEIGHT - 50 - instruction_height * (len(instructions) - i - 1)
            )
        screen.draw_ui(window)

        pygame.display.flip()
        cock.tick(60)
