import random

import pygame


class ScreenShakeManager:
    def __init__(self):
        self.shaking = False

    @staticmethod
    def get_shake():
        return random.randint(-20, 20), random.randint(-20, 20)

    def shake(self, window: pygame.Surface):
        if not self.shaking:
            pass
        tmp = window.copy()
        window.fill((0, 0, 0))
        window.blit(tmp, ScreenShakeManager.get_shake())
