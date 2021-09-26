from typing import TYPE_CHECKING

import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import CoinGUI, HPManager, Inventory

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
            pygame.Rect((212, 97), (104, 110)),
            pygame.Rect((691, 98), (104, 110)),
            pygame.Rect((1172, 97), (104, 110)),
            pygame.Rect((209, 351), (104, 110)),
            pygame.Rect((691, 351), (104, 110)),
            pygame.Rect((1172, 351), (104, 110)),
        ]
        self.price_tag_position = [
            pygame.Rect((184, 225), (160, 47)),
            pygame.Rect((663, 225), (160, 47)),
            pygame.Rect((1142, 225), (160, 47)),
            pygame.Rect((184, 475), (160, 47)),
            pygame.Rect((663, 475), (160, 47)),
            pygame.Rect((1142, 475), (160, 47)),
        ]
        self.price = ["4", "10", "13", "15", "16", "18"]
        self.button_text = [
            "Heal Potion",
            'Shield',
            'Superstar',
            'Bullet Time',
            'Missile',
            'Earthquake',
        ]
        self.button_text_effect = [
            'Restores 1 HP, instantly used if currently damaged',
            f'Shield that blocks 3 hits for {SHIELD_REMAIN_TIME}s',
            f'{ITEM_INVINCIBILITY_TIME}s invincibility',
            f'Time slows down for {ITEM_BULLET_TIME_DURATION}s',
            'Attack enemies',
            'Annihilation',
        ]
        self.button_text_effect = [f'   {t}' for t in self.button_text_effect]
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
        self.button_exit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((53, 40), (74, 43)),
            text='Exit',
            manager=self.shop_screen,
        )
        self.price_tag_button = [
            pygame_gui.elements.UIButton(
                relative_rect=self.price_tag_position[i],
                text="$" + self.price[i],
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
            button = self.display_buttons[i]
            button.normal_image = pygame.transform.scale(button.normal_image, (145, 150))
            button.hovered_image = pygame.transform.scale(button.hovered_image, (145, 150))
            button.selected_image = pygame.transform.scale(button.selected_image, (145, 150))
            button.rebuild()
        self._hide()

        self.button_confirm = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((555, 301), (200, 60)),
            text='Confirm',
            tool_tip_text="<font face=fira_code color=#8e1b1b size=6>"
            "<b><u>WARNING:</u></b>"
            "<br><br>"
            "<font color=#000000 size=5><i>If your inventory is full, your current selected item will be overwritten.</i></font>",
            object_id="#button_confirm",
            manager=self.confirm_screen
        )
        self.button_cancel = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((755, 301), (200, 60)),
            text='Cancel',
            manager=self.confirm_screen
        )
        self.button_number: int = 0
        self.price_count = 0
        self.game = game
        self.running = False
        self.coin_gui = CoinGUI((960, 36), self.game)
        self.hp_manager = HPManager(pygame.Vector2(380, 25), self.game)
        self.hp_manager.at_shop = True
        self.inventory = Inventory(
            [
                assets_manager.images[f'{item_name}_shop'] for item_name in (
                    'item_blank', 'item_healpotion', 'item_shield', 'item_star', 'item_clock',
                    'item_missile', 'item_earthquake'
                )
            ], self.game
        )
        self.inventory.at_shop = True

    def appear(self, window: pygame.Surface) -> None:
        clock = pygame.time.Clock()
        self.running = True
        confirmation = False
        while self.running:
            t = clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        button = event.ui_element
                        if button == self.button_exit:
                            self.running = False
                        elif button in (self.button_cancel, self.button_confirm) and confirmation:
                            if button == self.button_confirm:
                                assets_manager.play_sound("select2")
                                self.game.coins -= int(self.price_count)
                                if self.button_number == 0 and self.game.player.hp < 4:
                                    self.game.player.hp += 1
                                    #potion sound
                                elif self.game.player.items[self.game.player.holding] != 0:
                                    if self.game.player.items[3 - self.game.player.holding] == 0:
                                        self.game.player.holding = 3 - self.game.player.holding
                                    else:
                                        #warning message
                                        pass
                                    self.game.player.items[self.game.player.holding
                                                           ] = self.button_number + 1
                                else:
                                    self.game.player.items[self.game.player.holding
                                                           ] = self.button_number + 1
                            self._hide()
                            for i in range(6):
                                self.price_tag_button[i].enable()
                            confirmation = False
                        elif button in self.price_tag_button and not confirmation:
                            assets_manager.play_sound("select1")
                            self.button_number = self.price_tag_button.index(button)
                            for i in range(6):
                                self.price_tag_button[i].disable()
                            self.display_buttons[self.button_number].show()
                            self.price_count = self.price[self.button_number]
                            confirmation = True

                self.shop_screen.process_events(event)
                self.confirm_screen.process_events(event)

            if confirmation:
                self.confirm_screen.update(t / 1000)
            else:
                self.shop_screen.update(t / 1000)

            window.blit(self.main_menu, (0, 0))  # draws background
            self.shop_screen.draw_ui(window)
            self.coin_gui.update(t / 1000)
            self.coin_gui.draw(window)
            self.hp_manager.update(t / 1000)
            self.hp_manager.draw(window)
            self.game.player.update(0, 0)
            self.inventory.draw(window)
            self.checkcoins()

            if confirmation:  # have thing selected
                window.blit(self.darken, (0, 0))
                window.blit(self.confirm_button, (0, 0))
                self.confirm_screen.draw_ui(window)

            pygame.display.flip()

            clock.tick(60)

    def _hide(self):
        for button in self.display_buttons:
            button.hide()

    def checkcoins(self):
        for i in range(6):
            if self.game.coins < int(self.price[i]):
                self.price_tag_button[i].disable()
            else:
                self.price_tag_button[i].enable()
