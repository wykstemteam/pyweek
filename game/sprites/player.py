from re import match
import numpy as np
import pygame

from game.constants import *
from game.sprites.missile import Missile
from game.sprites import Obstacle


class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vx = -BACKGROUND_VELOCITY
        self.vy = 0.0
        self.dir = 0.0
        self.real_x = float(x)
        self.real_y = float(y)

        self.hp = 4
        self.missiles = pygame.sprite.Group()

        self.items = {1: 0, 2: 0}
        self.holding = 1

    def acc(self, dx, dy):
        self.vx = min(self.vx + dx, PLAYER_MAX_HORI_SPEED)
        self.vy += dy

    def update(self, t):
        self.real_x += (self.vx + BACKGROUND_VELOCITY) * t
        self.real_y += self.vy * t
        self.rect.left = self.real_x
        self.rect.top = self.real_y

        x = pygame.mouse.get_pos()[0] - (self.real_x + PLAYER_WIDTH / 2)
        y = (self.real_y + PLAYER_HEIGHT / 2) - pygame.mouse.get_pos()[1]
        self.dir = np.arctan2(y, x)

        keys = pygame.key.get_pressed()
        if self.real_x < 0:  # touches left border
            self.real_x = 0
            self.vx = -BACKGROUND_VELOCITY
        if self.real_x < SCREEN_WIDTH - PLAYER_WIDTH // 2:
            if keys[pygame.K_w]:
                self.acc(0, -PLAYER_ACC)
            if keys[pygame.K_s]:
                self.acc(0, PLAYER_ACC)
            if keys[pygame.K_d]:
                self.acc(PLAYER_ACC, 0)
            if keys[pygame.K_a]:
                self.acc(-PLAYER_ACC, 0)
        else:  # touches right border
            self.rect.left = SCREEN_WIDTH - PLAYER_WIDTH // 2
            self.vx = -BACKGROUND_VELOCITY

        if self.real_y < BUILDING_HEIGHT:
            self.real_y = BUILDING_HEIGHT
            self.vy = 0
        if self.real_y + PLAYER_HEIGHT > SCREEN_HEIGHT:
            self.real_y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.vy = 0

        if keys[pygame.K_1]:
            self.holding = 1
        elif keys[pygame.K_2]:
            self.holding = 2
        left_button_pressed = pygame.mouse.get_pressed()[0]
        if left_button_pressed:
            if self.items[self.holding] == 1:
                # FIXME: play some sound effect maybe
                self.hp += 1
            elif self.items[self.holding] == 2:  # invincible
                pass
            elif self.items[self.holding] == 3:
                self.vx -= np.cos(self.dir) * 100
                self.vy += np.sin(self.dir) * 100
                self.shoot_missile()
            elif self.items[self.holding] == 4:  # earthquake
                pass
            elif self.items[self.holding] == 5:  # shield
                pass
            elif self.items[self.holding] == 6:  # bullet time
                pass
            self.items[self.holding] = 0

        self.missiles.update(t)

        if self.vx > 0:
            self.vx = max(0, self.vx - FRICTION_HORI)
        else:
            self.vx = min(0, self.vx + FRICTION_HORI)

        if self.vy > 0:
            self.vy = max(0, self.vy - FRICTION_VERT)
        else:
            self.vy = min(0, self.vy + FRICTION_VERT)

    def draw(self, window):
        for missile in self.missiles:
            missile.draw(window)
        window.blit(self.image, self.rect)

    def in_bounds(self):
        return BUILDING_HEIGHT < self.real_y < SCREEN_HEIGHT - PLAYER_HEIGHT

    def shoot_missile(self):
        new_missile = Missile(self.rect.center, self.dir)
        self.missiles.add(new_missile)

    def resolve_collision(self, obstacle: Obstacle):
        obstacle_left = obstacle.pos.x - OBSTACLE_WIDTH // 2
        obstacle_right = obstacle.pos.x + OBSTACLE_WIDTH // 2
        obstacle_top = obstacle.pos.y - OBSTACLE_HEIGHT // 2
        obstacle_bottom = obstacle.pos.y + OBSTACLE_HEIGHT // 2
        self_left = self.real_x
        self_right = self.real_x + PLAYER_WIDTH
        self_top = self.real_y
        self_bottom = self.real_y + PLAYER_HEIGHT
        distances = [(self_right - obstacle_left, 0), (obstacle_right - self_left, 1),
                     (self_bottom - obstacle_top, 2), (obstacle_bottom - self_top, 3)]
        distances = sorted(filter(lambda x: x[0] >= 0, distances))

        if distances[0][1] == 0:  # right
            self.real_x = obstacle_left - PLAYER_WIDTH
            self.vx = 0
        elif distances[0][1] == 1:  # left
            self.real_x = obstacle_right
            self.vx = 0
        elif distances[0][1] == 2:  # top
            self.real_y = obstacle_top - PLAYER_HEIGHT
            self.vy = 0
        else:  # bottom
            self.real_y = obstacle_bottom
            self.vy = 0
        self.rect.left = self.real_x
        self.rect.top = self.real_y
