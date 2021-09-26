import pygame

pygame.init()

import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.game import Game
from game.menu import menu
from game.settings import settings

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rock: The Criminal")


def gaming() -> None:
    game = Game()
    game.run(window)


def main() -> None:
    while True:
        menu(window)
        gaming()
