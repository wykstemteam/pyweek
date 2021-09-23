import random
from enum import Enum

import pygame

from game.constants import *
from game.sprites.bullet import Bullet


class PoliceCar(pygame.sprite.Sprite):
    class State(Enum):
        RANDOM = 0
        BOTTOM_TO_UP = 1
        UP_TO_BOTTOM = 2

    def __init__(
        self, image: pygame.Surface, pos: pygame.Vector2, bullet_image: pygame.Surface,
        player_collision_group: pygame.sprite.Group
    ) -> None:
        super().__init__()

        self.image = image
        self.shadow = self.image.copy()
        alpha = 128
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.shadow_rect = self.rect.copy()
        self.shadow_rect.topleft = self.shadow_rect.topleft + pygame.Vector2(-5, 5)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.bullets = pygame.sprite.Group()
        self.bullet_image = bullet_image
        self.shoot_cooldown = SHOOT_COOLDOWN
        self.quickfire_skill_cooldown = QUICKFIRE_SKILL_COOLDOWN

        self.objectives = []
        self.velocity = POLICECAR_VELOCITY
        self.state = PoliceCar.State.RANDOM
        self.going_to_target = False

        self.player_collision_group = player_collision_group
        self.player_collision_group.add(self)

    def shoot(self, bullet_speed):
        new_bullet = Bullet(self.bullet_image, self.rect.center, bullet_speed)
        self.bullets.add(new_bullet)
        self.player_collision_group.add(new_bullet)

    def objectivepos(self, speed: int, t):
        if self.rect.centery == self.objectives[0]:
            del self.objectives[0]
        elif abs(self.rect.centery - self.objectives[0]) < speed * t:
            self.rect.centery = self.objectives[0]
        elif self.rect.centery > self.objectives[0]:
            self.rect.centery -= speed * t
        else:
            self.rect.centery += speed * t

    def update(self, t, shop: bool = False):
        if shop:
            self.rect.right = max(0, self.rect.right - 20*t)
            self.shadow_rect = self.rect.copy()
            self.shadow_rect.topleft = self.shadow_rect.topleft + pygame.Vector2(-5, 5)
            return
        # FIXME: @Jutsin/Eason please use an enum instead of raw integers for state
        if self.state == PoliceCar.State.RANDOM:
            if len(self.objectives) == 0:
                self.objectives.append(random.randint(120, 600 - POLICECAR_HEIGHT))
            self.objectivepos(self.velocity, t)
            if self.shoot_cooldown <= 0:
                self.shoot(-BACKGROUND_VELOCITY)
                self.shoot_cooldown = SHOOT_COOLDOWN
            else:
                self.shoot_cooldown -= t
            if len(self.objectives) == 0 and self.quickfire_skill_cooldown <= 0:
                self.state = random.choice(
                    [PoliceCar.State.BOTTOM_TO_UP, PoliceCar.State.UP_TO_BOTTOM]
                )
                if self.state == PoliceCar.State.BOTTOM_TO_UP:
                    self.objectives.append(SCREEN_HEIGHT)
                else:
                    self.objectives.append(BUILDING_HEIGHT)
                self.going_to_target = True
            else:
                self.quickfire_skill_cooldown -= t

        elif not self.going_to_target:
            self.objectivepos(self.velocity * 2, t)
            if len(self.objectives) == 0:
                self.state = PoliceCar.State.RANDOM
                self.quickfire_skill_cooldown = QUICKFIRE_SKILL_COOLDOWN
                self.shoot_cooldown = 3
            if self.shoot_cooldown <= 0:
                self.shoot(-BACKGROUND_VELOCITY)
                self.shoot_cooldown = QUICKFIRE_COOLDOWN
            else:
                self.shoot_cooldown -= t

        elif self.state == PoliceCar.State.BOTTOM_TO_UP:  # go to bottom first
            self.objectivepos(self.velocity, t)
            if len(self.objectives) == 0:
                self.going_to_target = False
                self.objectives.append(230)
                self.shoot_cooldown = 0

        else:  # PoliceCar.State.UP_TO_BOTTOM
            self.objectivepos(self.velocity, t)
            if len(self.objectives) == 0:
                self.going_to_target = False
                self.objectives.append(470)
                self.shoot_cooldown = 0

        self.shadow_rect = self.rect.copy()
        self.shadow_rect.topleft = self.shadow_rect.topleft + pygame.Vector2(-5, 5)
        self.bullets.update(t)

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.shadow, self.shadow_rect)
        window.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(window)

    def kill(self) -> None:
        self.bullets.empty()

    def player_hit(self, player):  # should be called when collided by someone
        # animation
        pass
