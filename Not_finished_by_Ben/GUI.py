import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

button_layout_rect = pygame.Rect(30, 20, 100, 20)
button_layout_rect.bottomright = (-30, -20)

hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
          text='Hello', manager=manager,
          anchors={'left': 'right',
                   'right': 'right',
                   'top': 'bottom',
                   'bottom': 'bottom'})

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        key_pressed= pygame.key.get_pressed()
        if key_pressed[pygame.K_p]:
            manager.set_visual_debug_mode(True)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()