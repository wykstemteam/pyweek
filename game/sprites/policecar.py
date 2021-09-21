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

    def update(self, t):
        if self.state == 0:  # bottom to top quickfire
            while self.rect.centery != 50:
                if self.rect.centery > 50:
                    if abs(self.rect.centery - 50) < self.velocity * t:
                        self.rect.centery = 50
                    else:
                        self.rect.centery -= self.velocity * t
                else:
                    if abs(self.rect.centery - 50) < self.velocity * t:
                        self.rect.centery = 50
                    else:
                        self.rect.centery += self.velocity * t
            while centery <= 400:
                self.rect.centery += 100
                self.bullets.update(t)
                if self.shoot_cooldown <= 0:
                    self.shoot(500)
                    self.shoot_cooldown = QUICKFIRE_COOLDOWN
                else:
                    self.shoot_cooldown -= t
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
                self.shoot(500)
                self.shoot_cooldown = SHOOT_COOLDOWN
            else:
                self.shoot_cooldown -= t

    def draw(self, window):
        window.blit(self.image, self.rect)
        for bullet in self.bullets:
            window.blit(bullet.image, bullet.rect)
