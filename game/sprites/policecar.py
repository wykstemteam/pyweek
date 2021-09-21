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
        self.quickfire_skill_cooldown = QUICKFIRE_SKILL_COOLDOWN

        self.objectives = []
        self.velocity = POLICECAR_VELOCITY
        self.state = 0

    def shoot(self, bullet_speed):
        self.bullets.add(
            Bullet(self.bullet_image, self.rect.center, bullet_speed))

    def objectivepos(self, t):
        if self.rect.centery != self.objectives[0]:
            if self.rect.centery > self.objectives[0]:
                if abs(self.rect.centery - self.objectives[0]) < self.velocity * t:
                    self.rect.centery = self.objectives[0]
                else:
                    self.rect.centery -= self.velocity * t
            else:
                if abs(self.rect.centery - self.objectives[0]) < self.velocity * t:
                    self.rect.centery = self.objectives[0]
                else:
                    self.rect.centery += self.velocity * t
        else:
            self.objectives.pop(0)

    def update(self, t):
        if self.state == 0:  
            if len(self.objectives) == 0:
                self.objectives.append(
                    random.randint(120, 600 - POLICECAR_HEIGHT))
            self.objectivepos(t)
            if self.shoot_cooldown <= 0:
                self.shoot(-BACKGROUND_VELOCITY)
                self.shoot_cooldown = SHOOT_COOLDOWN
            else:
                self.shoot_cooldown -= t
            if len(self.objectives) == 0 and self.quickfire_skill_cooldown <= 0:
                self.state = 1
                self.objectives.append(SCREEN_HEIGHT - BULLET_HEIGHT)
                self.objectives.append(300)
                self.shoot_cooldown = QUICKFIRE_COOLDOWN
            else:
                self.quickfire_skill_cooldown -= t
        elif self.state == 1: # bottom to top quickfire
            self.objectivepos(t)
            if len(self.objectives) == 0:
                self.state = 0
                self.quickfire_skill_cooldown = QUICKFIRE_SKILL_COOLDOWN
            if self.shoot_cooldown <= 0:
                self.shoot(-BACKGROUND_VELOCITY)
                self.shoot_cooldown = QUICKFIRE_COOLDOWN
            else:
                self.shoot_cooldown -= t

        self.bullets.update(t)

    def draw(self, window):
        window.blit(self.image, self.rect)
        for bullet in self.bullets:
            window.blit(bullet.image, bullet.rect)
