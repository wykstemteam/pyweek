import pygame
import pygame_gui

from game.constants import *


class Shop:  # FIXME: Move outside of sprites if it is not a sprite
    def __init__(
        self, confirm_button: pygame.Surface, main_menu: pygame.Surface, darken: pygame.Surface
    ) -> None:
        self.confirm_button = confirm_button
        self.main_menu = main_menu
        self.darken = darken
        self.shop_screen = pygame_gui.UIManager(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 'shop_display_theme.json'
        )
        self.button_positions = [
            pygame.Rect((218, 125), (104, 110)),
            pygame.Rect((697, 125), (104, 110)),
            pygame.Rect((1178, 125), (104, 110)),
            pygame.Rect((218, 391), (104, 110)),
            pygame.Rect((698, 391), (104, 110)),
            pygame.Rect((1178, 391), (104, 110)),
        ]
        self.buttons = [
            pygame_gui.elements.UIButton(
                relative_rect=self.button_positions[i],
                text='',
                object_id=f'#button_{i+1}',
                manager=self.shop_screen
            ) for i in range(6)
        ]

    def appear(self, window: pygame.Surface) -> None:
        clock = pygame.time.Clock()
        running = True

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
                        print(f'#button_{self.buttons.index(button) + 1}')
                        self.confirm_menu(f'#button_{self.buttons.index(button) + 1}', window)

                self.shop_screen.process_events(event)

            self.shop_screen.update(t / 1000)
            window.blit(self.main_menu, (0, 0))
            self.shop_screen.draw_ui(window)
            pygame.display.flip()

            clock.tick(60)

    def confirm_menu(self, button_name: str, window: pygame.Surface) -> None:
        confirm_screen = pygame_gui.UIManager(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 'shop_confirm_theme.json'
        )
        button_display = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((678, 120), (145, 150)),
            text="",
            object_id=button_name,
            manager=confirm_screen
        )
        button_confirm = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((555, 301), (200, 60)),
            text='Confirm',
            manager=confirm_screen
        )
        button_cancel = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((755, 301), (200, 60)), text='Cancel', manager=confirm_screen
        )

        clock = pygame.time.Clock()
        run = True
        window.blit(self.darken, pygame.Rect(0, 0, 0, 0))

        while run:
            t = clock.get_time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        run = False
                elif event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element in (button_confirm, button_cancel):
                            run = False

                confirm_screen.process_events(event)

            window.blit(self.confirm_button, (0, 0))
            confirm_screen.update(t / 1000)
            confirm_screen.draw_ui(window)
            pygame.display.flip()

            clock.tick(60)
