import numpy as np
import pygame

from game.constants import *
from game.sprites.missle import Missle

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
        self.missles = pygame.sprite.Group()

    def acc(self, dx, dy):
        self.vx = min(self.vx + dx, PLAYER_MAX_HORI_SPEED)
        self.vy += dy

    def update(self, t):
        self.real_x += (self.vx + BACKGROUND_VELOCITY) * t
        self.real_y += self.vy * t
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

        left_button_pressed = pygame.mouse.get_pressed()[0]
        if left_button_pressed:
            self.shoot_missle()
        
        self.missles.update(t)

        if self.vx > 0:
            self.vx = max(0, self.vx - FRICTION_HORI)
        elif self.vx < 0:
            self.vx = min(0, self.vx + FRICTION_HORI)

        if self.vy > 0:
            self.vy = max(0, self.vy - FRICTION_VERT)
        elif self.vy < 0:
            self.vy = min(0, self.vy + FRICTION_VERT)

        self.rect.left = self.real_x
        self.rect.top = self.real_y

    def draw(self, window):
        for missle in self.missles:
            missle.draw(window)
        window.blit(self.image, self.rect)

    def in_bounds(self):
        return BUILDING_HEIGHT < self.real_y < SCREEN_HEIGHT - PLAYER_HEIGHT

    def shoot_missle(self):
        new_missle = Missle((self.real_x, self.real_y), self.dir)
        self.missles.add(new_missle)
