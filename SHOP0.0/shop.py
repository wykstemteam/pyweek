import pygame
import sys
import pygame_gui

def shop_confirm_menu(button_name, window: pygame.Surface):
    SCREEN_WIDTH, SCREEN_HIGHT = 1500, 600
    CONFIRM_MENU = pygame.image.load('SHOP_confirm_menu.png')
    DARKEN = pygame.image.load('Darken.png')
    confirm_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HIGHT), 'confirm_theme.json')

    button_display = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((678, 120), (145, 150)),
                                                  text="",
                                                  object_id = button_name,
                                                  manager=confirm_screen)
    button_confirm = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((555, 301), (200, 60)),
                                                  text='Confirm',
                                                  manager=confirm_screen)
    button_cancel = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((755, 301), (200, 60)),
                                                 text='Cancel',
                                                 manager=confirm_screen)

    clock = pygame.time.Clock()
    run = True
    window.blit(DARKEN, pygame.Rect(0, 0, 0, 0))
    while run:
        t = clock.get_time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    run = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == button_confirm:
                        print(button + ' is bought')
                        run = False
                    if event.ui_element == button_cancel:
                        run = False

            confirm_screen.process_events(event)

        window.blit(CONFIRM_MENU, (0, 0))
        confirm_screen.update(t / 1000)
        confirm_screen.draw_ui(window)
        pygame.display.flip()

        clock.tick(60)


def shop_main_menu(window: pygame.Surface):
    SCREEN_WIDTH, SCREEN_HIGHT = 1500, 600
    SHOP_MAIN_MANU_IMAGE = pygame.image.load('SHOP_main_menu.png')
    SHOP_MAIN_MANU = pygame.transform.scale(SHOP_MAIN_MANU_IMAGE, (SCREEN_WIDTH, SCREEN_HIGHT))

    shop_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HIGHT), 'display_theme.json')
    button_1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((218, 125), (104, 110)),
                                            text='',
                                            object_id="#button_1",
                                            manager=shop_screen)
    button_2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((698, 125), (104, 110)),
                                            text='',
                                            object_id="#button_2",
                                            manager=shop_screen)
    button_3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1178, 125), (104, 110)),
                                            text='',
                                            object_id="#button_3",
                                            manager=shop_screen)
    button_4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((218, 391), (104, 110)),
                                            text='',
                                            object_id="#button_2",
                                            manager=shop_screen)
    button_5 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((698, 391), (104, 110)),
                                            text='',
                                            object_id="#button_2",
                                            manager=shop_screen)
    button_6 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1178, 391), (104, 110)),
                                            text='',
                                            object_id="#button_2",
                                            manager=shop_screen)

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

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == button_1:
                        shop_confirm_menu("#button_1", window)
                    if event.ui_element == button_2:
                        shop_confirm_menu("#button_2", window)
                    if event.ui_element == button_3:
                        shop_confirm_menu("#button_3", window)
                    if event.ui_element == button_4:
                        shop_confirm_menu("#button_4", window)
                    if event.ui_element == button_5:
                        shop_confirm_menu("#button_5", window)
                    if event.ui_element == button_6:
                        shop_confirm_menu("#button_6", window)

            shop_screen.process_events(event)

        shop_screen.update(t / 1000)
        window.blit(SHOP_MAIN_MANU, (0, 0))
        shop_screen.draw_ui(window)
        pygame.display.flip()

        clock.tick(60)



