import random

import pygame

from game.constants import *
from game.sprites import Bullet


class PoliceCar(pygame.sprite.Sprite):
    def __init__(
        self, image: pygame.Surface, pos: pygame.Vector2, bullet_image: pygame.Surface
    ) -> None:
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
        self.bullets.add(Bullet(self.bullet_image, self.rect.center, bullet_speed))

    def objectivepos(self, speed: int, t):
        if self.rect.centery != self.objectives[0]:
            if self.rect.centery > self.objectives[0]:
                if abs(self.rect.centery - self.objectives[0]) < speed * t:
                    self.rect.centery = self.objectives[0]
                else:
                    self.rect.centery -= speed * t
            else:
                if abs(self.rect.centery - self.objectives[0]) < speed * t:
                    self.rect.centery = self.objectives[0]
                else:
                    self.rect.centery += speed * t
        else:
            self.objectives.pop(0)

    def update(self, t):
        if self.state == 0:
            if len(self.objectives) == 0:
                self.objectives.append(random.randint(120, 600 - POLICECAR_HEIGHT))
            self.objectivepos(self.velocity, t)
            if self.shoot_cooldown <= 0:
                self.shoot(-BACKGROUND_VELOCITY)
                self.shoot_cooldown = SHOOT_COOLDOWN
            else:
                self.shoot_cooldown -= t
            if len(self.objectives) == 0 and self.quickfire_skill_cooldown <= 0:
                self.state = random.randint(1, 2)
                if(self.state == 1):
                    self.objectives.append(SCREEN_HEIGHT - BULLET_HEIGHT)
                else:
                    self.objectives.append(BUILDING_HEIGHT)
            else:
                self.quickfire_skill_cooldown -= t
        elif self.state == 1:  # go to bottom first
            self.objectivepos(self.velocity, t)
            if self.shoot_cooldown <= 0:
                self.shoot(-BACKGROUND_VELOCITY)
                self.shoot_cooldown = SHOOT_COOLDOWN
            else:
                self.shoot_cooldown -= t
            if len(self.objectives) == 0:
                self.state =101
                self.objectives.append(230)
                self.shoot_cooldown = 0
        elif self.state == 101:  # bottom to top quickfire
            self.objectivepos(self.velocity * 2, t)
            if len(self.objectives) == 0:
                self.state = 0
                self.quickfire_skill_cooldown = QUICKFIRE_SKILL_COOLDOWN
                self.shoot_cooldown = 3
            if self.shoot_cooldown <= 0:
                self.shoot(-BACKGROUND_VELOCITY)
                self.shoot_cooldown = QUICKFIRE_COOLDOWN
            else:
                self.shoot_cooldown -= t
        elif self.state == 2:  # go to top first
            self.objectivepos(self.velocity, t)
            if self.shoot_cooldown <= 0:
                self.shoot(-BACKGROUND_VELOCITY)
                self.shoot_cooldown = SHOOT_COOLDOWN
            else:
                self.shoot_cooldown -= t
            if len(self.objectives) == 0:
                self.state = 102
                self.objectives.append(470)
                self.shoot_cooldown = 0
        elif self.state == 102:  # top to bottom quickfire
            self.objectivepos(self.velocity * 2, t)
            if len(self.objectives) == 0:
                self.state = 0
                self.quickfire_skill_cooldown = QUICKFIRE_SKILL_COOLDOWN
                self.shoot_cooldown = 3
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

    def kill(self):
        self.bullets.empty()

    def player_hit(self, player):  # should be called when collided by someone
        # animation
        pass
