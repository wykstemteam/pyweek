import math

import numpy as np
import pygame
import pygame_gui

from game.assets_manager import AssetsManager
from game.constants import *
from game.sprites import Player, Road

assets_manager = AssetsManager()

def main():
    pygame.init()
    
    # gui
    gui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=gui_manager)

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    assets_manager.images['road'] = pygame.transform.scale(
        assets_manager.images['road'], (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    roads = pygame.sprite.Group(
        Road(assets_manager.images['road'], 0, 0),
        Road(assets_manager.images['road'], SCREEN_WIDTH, 0),
    )
    assets_manager.images['player'] = pygame.transform.scale(
        assets_manager.images['player'],
        (PLAYER_WIDTH, PLAYER_HEIGHT)
    )
    player = Player(
        assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    clock = pygame.time.Clock()


    running = True
    lose = False
    while running:
        t = clock.get_time()

        # event process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            gui_manager.process_events(event)

        # update
        keys = pygame.key.get_pressed()
        if lose == True:
            if keys[pygame.K_f]:
                player = Player(
                    assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                lose = False
        else:
            roads.update(BACKGROUND_SPEED, 0)
            player.update(t//10)  # code copied to player.py

            if not player.in_bounds():
                lose = True
        gui_manager.update(t // 1000.0)

        # draw
        roads.draw(window)
        window.blit(player.image, player.rect)
        if lose == True:
            window.blit(assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
        gui_manager.draw_ui(window)
        pygame.display.flip()

        clock.tick(60)
