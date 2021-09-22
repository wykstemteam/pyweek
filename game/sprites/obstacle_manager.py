import random

import pygame.sprite

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Obstacle


class ObstacleManager:
    def __init__(self, player_collision_group) -> None:
        self.obstacles = pygame.sprite.Group()
        self.cooldown = OBSTACLE_COOLDOWN
        self.player_collision_group = player_collision_group

    def add(self) -> None:
        obstacle_num = random.randint(1, 3)
        new_obstacle = Obstacle(
                assets_manager.images[f'obstacle{obstacle_num}'], (
                    SCREEN_WIDTH - OBSTACLE_WIDTH / 2 - 1,
                    random.randint(
                        BUILDING_HEIGHT + OBSTACLE_HEIGHT / 2, SCREEN_HEIGHT - OBSTACLE_WIDTH / 2
                    )
                )
            )
        self.obstacles.add(new_obstacle)
        self.player_collision_group.add(new_obstacle)

    def update(self, t: float) -> None:
        if self.cooldown <= 0:
            self.add()
            self.cooldown = OBSTACLE_COOLDOWN
        else:
            self.cooldown -= t
        self.obstacles.update(t)

    def draw(self, window: pygame.Surface) -> None:
        for obstacle in self.obstacles:
            window.blit(obstacle.image, obstacle.rect)

    def kill(self) -> None:
        self.obstacles.empty()
