import pygame
import random

from game.constants import *
from game.sprites.bullet import Bullet

class PoliceCar(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, bullet_image: pygame.Surface) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.bullets = pygame.sprite.Group()
        self.bullet_image = bullet_image
        self.shoot_cooldown = SHOOT_COOLDOWN

    def shoot(self, bullet_speed):
        self.bullets.add(Bullet(self.bullet_image, self.rect.center, bullet_speed))
    
    def update(self, t):
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
    
    def normal(self):
        movement = True
        while movement:
            y = random.randint(120, 600-POLICECAR_HEIGHT)
            while y != self.rect.top:
                movement = False
                if abs(y - self.rect.top) <= 50:
                    self.rect.top = y
                elif y < self.rect.top:
                    self.rect.top += 50
                else
                    self.rect.top -= 50
