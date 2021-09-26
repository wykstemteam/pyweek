import pygame

pygame.init()

import os

from game.constants import *
from game.game import Game
from game.highscore import read_highscore
from game.menu import menu

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)


def main() -> None:
    highscore = read_highscore()

    while True:
        menu(window, highscore)
        game = Game(highscore)
        highscore = game.run(window)
        with open("highscore.txt", 'w') as f:
            f.write(str(highscore))
