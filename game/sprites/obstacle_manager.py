import random

import pygame.sprite

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Obstacle


class ObstacleManager:
    def __init__(self) -> None:
        self.obstacles = pygame.sprite.Group()
        self.cooldown = OBSTACLE_COOLDOWN

    def add(self):
        obstacle_num = random.randint(1, 3)
        self.obstacles.add(
            Obstacle(
                assets_manager.images[f'obstacle{obstacle_num}'], (
                    SCREEN_WIDTH - OBSTACLE_WIDTH / 2 - 1,
                    random.randint(
                        BUILDING_HEIGHT + OBSTACLE_HEIGHT / 2, SCREEN_HEIGHT - OBSTACLE_WIDTH / 2
                    )
                )
            )
        )

    def update(self, t):
        if self.cooldown <= 0:
            self.add()
            self.cooldown = OBSTACLE_COOLDOWN
        else:
            self.cooldown -= t
        self.obstacles.update(t)

    def draw(self, window):
        for obstacle in self.obstacles:
            window.blit(obstacle.image, obstacle.rect)

    def kill(self):
        self.obstacles.empty()
