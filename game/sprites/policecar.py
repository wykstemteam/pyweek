import pygame
import random

from game.constants import *
from game.sprites import Bullet


class PoliceCar(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, bullet_image: pygame.Surface) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.bullets = pygame.sprite.Group()
        self.bullet_image = bullet_image
        self.shoot_cooldown = SHOOT_COOLDOWN

        self.objective = self.rect.centery
        self.velocity = POLICECAR_VELOCITY
        self.state = 0

    def shoot(self, bullet_speed):
        self.bullets.add(Bullet(self.bullet_image, self.rect.center, bullet_speed))

    def objectivepos(self, x : int , speed : int):
        if self.rect.centery != x:
            if self.rect.centery > x:
                if abs(self.rect.centery - x) < speed * t:
                    self.rect.centery = x
                else:
                    self.rect.centery -= speed * t
            else:
                if abs(self.rect.centery - x) < speed * t:
                    self.rect.centery = x
                else:
                    self.rect.centery += speed * t
    def update(self, t):
        if self.state == 0:  # bottom to top quickfire
            self.objectivepos(50, self.velocity)
            self.objectivepos(400, 50)
            self.state = 1
        else:
            if self.rect.centery != self.objective:
                if self.rect.centery > self.objective:
                    if abs(self.rect.centery - self.objective) < self.velocity * t:
                        self.rect.centery = self.objective
                    else:
                        self.rect.centery -= self.velocity * t
                else:
                    if abs(self.rect.centery - self.objective) < self.velocity * t:
                        self.rect.centery = self.objective
                    else:
                        self.rect.centery += self.velocity * t
            else:
                self.objective = random.randint(120, 600 - POLICECAR_HEIGHT)

        self.bullets.update(t)
        if self.shoot_cooldown <= 0:
            self.shoot(-BACKGROUND_VELOCITY)
            self.shoot_cooldown = SHOOT_COOLDOWN
        else:
            self.shoot_cooldown -= t

    def draw(self, window):
        window.blit(self.image, self.rect)
        for bullet in self.bullets:
            window.blit(bullet.image, bullet.rect)
