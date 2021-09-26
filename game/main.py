import pygame

pygame.init()

import os

from game.constants import *
from game.game import Game
from game.menu import menu

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rock: The Criminal")

def main() -> None:
    highscore = 0
    if not os.path.isfile('highscore.txt'):
        open("highscore.txt", "x")
    else:
        with open("highscore.txt", 'r') as f:
            highscore = int(f.read())
    while True:
        menu(window, highscore)
        game = Game(highscore)
        highscore = game.run(window)
        with open("highscore.txt", 'w') as f:
            f.write(str(highscore))
