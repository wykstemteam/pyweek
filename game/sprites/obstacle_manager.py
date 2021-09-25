import random

import pygame.sprite

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.obstacle import Obstacle


class ObstacleManager:
    def __init__(self, player_collision_group) -> None:
        self.obstacles = pygame.sprite.Group()
        self.cooldown = OBSTACLE_COOLDOWN
        self.player_collision_group = player_collision_group
        self.reached_checkpoint = False

    def add(self) -> None:
        obstacle_num = random.randint(1, 3)
        new_obstacle = Obstacle(
            assets_manager.images[f'obstacle{obstacle_num}'],
            pygame.Vector2(
                SCREEN_WIDTH + OBSTACLE_WIDTH,
                random.randint(
                    BUILDING_HEIGHT + OBSTACLE_HEIGHT / 2, SCREEN_HEIGHT - OBSTACLE_WIDTH / 2
                ),
            )
        )
        self.obstacles.add(new_obstacle)
        self.player_collision_group.add(new_obstacle)

    def update(self, t: float) -> None:
        self.obstacles.update(t)
        if self.reached_checkpoint:
            return
        if self.cooldown <= 0:
            self.add()
            self.cooldown = OBSTACLE_COOLDOWN
        else:
            self.cooldown -= t

    def draw(self, window: pygame.Surface) -> None:
        for obstacle in self.obstacles:
            window.blit(obstacle.image, obstacle.rect)

    def kill(self) -> None:
        self.obstacles.empty()
