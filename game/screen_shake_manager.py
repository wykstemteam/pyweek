import random
from typing import Tuple

import pygame


class ScreenShakeManager:
    def __init__(self) -> None:
        self.shaking = False

    @staticmethod
    def get_shake() -> Tuple[int, int]:
        return random.randint(-20, 20), random.randint(-20, 20)

    def shake(self, window: pygame.Surface) -> None:
        if self.shaking:
            window_copy = window.copy()
            window.fill((0, 0, 0))
            window.blit(window_copy, ScreenShakeManager.get_shake())
