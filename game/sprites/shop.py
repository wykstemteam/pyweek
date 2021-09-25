from typing import TYPE_CHECKING

import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *

if TYPE_CHECKING:
    from game.game import Game


class Shop:
    confirm_button = assets_manager.images['confirm_button']
    main_menu = assets_manager.images['main_menu']
    darken = assets_manager.images['darken']

    def __init__(self, game: "Game") -> None:
        self.shop_screen = pygame_gui.UIManager(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 'shop_display_theme.json'
        )
        self.shop_screen.preload_fonts(
            [
                {
                    'name': 'fira_code',
                    'point_size': 18,
                    'style': style
                } for style in ('regular', 'bold', 'italic')
            ]
        )
        self.button_positions = [
            pygame.Rect((218, 125), (104, 110)),
            pygame.Rect((697, 125), (104, 110)),
            pygame.Rect((1178, 125), (104, 110)),
            pygame.Rect((218, 391), (104, 110)),
            pygame.Rect((698, 391), (104, 110)),
            pygame.Rect((1178, 391), (104, 110)),
        ]
        self.price_tag_position = [
            pygame.Rect((191, 252), (160, 47)),
            pygame.Rect((670, 252), (160, 47)),
            pygame.Rect((1149, 252), (160, 47)),
            pygame.Rect((191, 520), (160, 47)),
            pygame.Rect((670, 520), (160, 47)),
            pygame.Rect((1149, 520), (160, 47)),
        ]
        self.price = ["$10", "$15", "$20", "$25", "$30", "$35"]
        self.button_text = [
            "Heal Potion",
            'Shield',
            'Superstar',
            'Bullet Time',
            'Missile',
            'Gravitation',
        ]
        self.button_text_effect = [
            '+1 life',
            '+3 shield (30s)',
            '5s invinciblility',
            '5s bullet time',  # TODO: Put more clear description
            'Attack the boss?',
            'Annihilation',
        ]
        self.button_text_effect = [" " * 3 + t for t in self.button_text_effect]
        self.buttons = [
            pygame_gui.elements.UIButton(
                relative_rect=self.button_positions[i],
                text='',
                object_id=f'#button_{i + 1}',
                tool_tip_text="<font face=fira_code color=normal_text size=5>"
                f" <b><u>{self.button_text[i]}</u></b>"
                "<br><br>"
                f"<i>{self.button_text_effect[i]}</i>",
                manager=self.shop_screen,
            ) for i in range(6)
        ]
        self.price_tag_button = [
            pygame_gui.elements.UIButton(
                relative_rect=self.price_tag_position[i],
                text=self.price[i],
                object_id="price_tag",
                manager=self.shop_screen,
            ) for i in range(6)
        ]
        self.confirm_screen = pygame_gui.UIManager(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 'shop_display_theme.json'
        )
        self.confirm_screen.preload_fonts(
            [
                {
                    'name': 'fira_code',
                    'point_size': 18,
                    'style': style
                } for style in ('regular', 'bold', 'italic')
            ]
        )
        self.display_buttons = [
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((678, 120), (145, 150)),
                text='',
                tool_tip_text="<font face=fira_code color=normal_text size=5>"
                f"<b><u>{self.button_text[i]}</u></b>"
                "<br><br>"
                f"<i>{self.button_text_effect[i]}</i>",
                object_id=f'#button_{i + 1}',
                manager=self.confirm_screen
            ) for i in range(6)
        ]
        for i in range(6):
            self.display_buttons[i].normal_image = pygame.transform.scale(
                self.display_buttons[i].normal_image, (145, 150)
            )
            self.display_buttons[i].hovered_image = pygame.transform.scale(
                self.display_buttons[i].hovered_image, (145, 150)
            )
            self.display_buttons[i].rebuild()
        self._hide()

        self.button_confirm = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((555, 301), (200, 60)),
            text='Confirm',
            manager=self.confirm_screen
        )
        self.button_cancel = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((755, 301), (200, 60)),
            text='Cancel',
            manager=self.confirm_screen
        )
        self.game = game
        self.coins = self.game.coins

    def appear(self, window: pygame.Surface) -> None:
        clock = pygame.time.Clock()
        running = True
        confirmation = False

        while running:
            t = clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print("Shop closed")
                        running = False
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        button = event.ui_element
                        if button in (self.button_cancel, self.button_confirm):
                            if button == self.button_confirm:
                                assets_manager.play_sound("select2")
                            self._hide()
                            for i in range(6):
                                self.price_tag_button[i].enable()
                            confirmation = False
                        elif button in self.price_tag_button:
                            assets_manager.play_sound("select1")
                            button_number = self.price_tag_button.index(button)
                            for i in range(6):
                                self.price_tag_button[i].disable()
                            self.display_buttons[button_number].show()
                            confirmation = True

                self.shop_screen.process_events(event)
                self.confirm_screen.process_events(event)

            if confirmation:
                self.confirm_screen.update(t / 1000)
            else:
                self.shop_screen.update(t / 1000)

            window.blit(self.main_menu, (0, 0))  # draws background
            self.shop_screen.draw_ui(window)

            if confirmation:  # have thing selected
                window.blit(self.darken, (0, 0))
                window.blit(self.confirm_button, (0, 0))
                self.confirm_screen.draw_ui(window)

            pygame.display.flip()

            clock.tick(60)

    def _hide(self):
        for button in self.display_buttons:
            button.hide()
