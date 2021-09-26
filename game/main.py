import pygame

pygame.init()

import os

from game.constants import *
from game.game import Game
from game.menu import menu

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

def main() -> None:
    highscore = 0
    if not os.path.isfile('highscore.txt'):
        open("highscore.txt", "x")
        with open("highscore.txt", 'w') as f:
            f.write('0')
    else:
        with open("highscore.txt", 'r') as f:
            highscore = int(f.read())
    while True:
        menu(window, highscore)
        game = Game(highscore)
        highscore = game.run(window)
        with open("highscore.txt", 'w') as f:
            f.write(str(highscore))
