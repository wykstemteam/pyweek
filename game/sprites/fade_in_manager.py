import pygame

from game.constants import *


class FadeInManager:
    def __init__(self, gradient_strip: pygame.Surface):
        self.gradient_strip = gradient_strip
        self.x = -SCREEN_WIDTH
        self.fading_in = False

    def start_fade_in(self):
        self.x = -SCREEN_WIDTH
        self.fading_in = True

    def update(self, t: float):
        self.x += FADE_IN_VELOCITY * t

    def draw(self, window: pygame.Surface):
        if not self.fading_in:
            return
        if self.x < SCREEN_WIDTH:
            window.blit(self.gradient_strip, (self.x, 0))
            if self.x < 0:
                window.fill(
                    (0, 0, 0),
                    pygame.Rect(self.x + SCREEN_WIDTH, 0, SCREEN_WIDTH - self.x, SCREEN_HEIGHT)
                )
        else:
            self.fading_in = False
