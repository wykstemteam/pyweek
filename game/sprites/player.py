import numpy as np
import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites.missile import Missile
from game.sprites.obstacle import Obstacle
from game.sprites.shield import Shield


class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int, game) -> None:
        super().__init__()

        self.game = game

        self.ori_image = image.copy()
        self.image = image.copy()
        self.shadow = self.image.copy()
        alpha = 128
        self.shadow.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.shadow_rect = self.image.get_rect()
        self.shadow_rect.topleft = (x - 5, y + 5)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vx = -BACKGROUND_VELOCITY
        self.vy = 0.0
        self.dir = 0.0
        self.real_x = float(x)
        self.real_y = float(y)

        self.hp = 4
        self.missiles = pygame.sprite.Group()

        self.coins = 0

        self.items = {1: 0, 2: 0}
        self.holding = 1

        self.invincibility_after_damage = 0
        self.blink_state = 1
        self.blink_cooldown = PLAYER_BLINK_COOLDOWN

        self.shield = Shield((self.real_x, self.real_y))

        self.item_invincible = False
        self.invincible_color = 0x000000
        self.item_invincible_time = ITEM_INVINCIBILITY_TIME

        self.inputtable = True

    def acc(self, dx: int, dy: int) -> None:
        self.vx = max(min(self.vx + dx, PLAYER_MAX_SPEED), -PLAYER_MAX_SPEED)
        self.vy = max(min(self.vy + dy, PLAYER_MAX_SPEED), -PLAYER_MAX_SPEED)

    def apply_friction(self) -> None:
        if self.vx > 0:
            self.vx = max(0, self.vx - FRICTION_HORI)
        else:
            self.vx = min(0, self.vx + FRICTION_HORI)

        if self.vy > 0:
            self.vy = max(0, self.vy - FRICTION_VERT)
        else:
            self.vy = min(0, self.vy + FRICTION_VERT)

    def update(self, t: float, scene) -> None:
        self.real_x += (self.vx + BACKGROUND_VELOCITY) * t
        self.real_y += self.vy * t

        self.invincibility_after_damage -= t
        if self.invincibility_after_damage <= 0:
            self.blink_state = 1
        else:
            self.blink_cooldown -= t
            if self.blink_cooldown <= 0:
                self.blink_state = 1 - self.blink_state
                self.blink_cooldown = PLAYER_BLINK_COOLDOWN
        self.image.set_alpha(self.blink_state * 255)

        x = pygame.mouse.get_pos()[0] - (self.real_x + PLAYER_WIDTH / 2)
        y = (self.real_y + PLAYER_HEIGHT / 2) - pygame.mouse.get_pos()[1]
        self.dir = np.arctan2(y, x)

        keys = pygame.key.get_pressed()
        if self.real_x < 0:  # touches left border
            self.real_x = 0
            self.vx = -BACKGROUND_VELOCITY
        if self.real_x < SCREEN_WIDTH - PLAYER_WIDTH:
            if self.inputtable:
                if keys[pygame.K_w]:
                    self.acc(0, -PLAYER_ACC)
                if keys[pygame.K_s]:
                    self.acc(0, PLAYER_ACC)
                if keys[pygame.K_d]:
                    self.acc(PLAYER_ACC, 0)
                if keys[pygame.K_a]:
                    self.acc(-PLAYER_ACC, 0)
        elif self.inputtable:  # touches right border
            self.real_x = SCREEN_WIDTH - PLAYER_WIDTH
            self.vx = -BACKGROUND_VELOCITY

        if FREE_ITEMS:
            for i in range(6):
                if keys[pygame.K_KP_1 + i]:
                    self.items[self.holding] = i + 1
            if keys[pygame.K_c]:
                self.add_coin()
                assets_manager.play_sound("coin")

        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        if keys[pygame.K_1]:
            self.holding = 1
        elif keys[pygame.K_2]:
            self.holding = 2
        left_button_pressed = pygame.mouse.get_pressed(num_buttons=3)[0]
        # Make sure mouse is not on the pause button
        if left_button_pressed and self.inputtable and not (1390 <= mx <= 1490 and 10 <= my <= 60):
            if self.items[self.holding] == 1:
                if self.hp < 4:
                    assets_manager.play_sound("heal")
                    self.hp += 1
                    self.items[self.holding] = 0
            elif self.items[self.holding] == 2:  # shield
                assets_manager.play_sound("shield_equip")
                self.shield.turn_on()
                self.items[self.holding] = 0
            elif self.items[self.holding] == 3:  # invincible
                assets_manager.play_sound("star")
                self.become_item_invincible()
                self.items[self.holding] = 0
            elif self.items[self.holding] == 4:  # bullet time
                assets_manager.play_sound("slow_motion")
                self.game.bullet_time = True
                self.game.bullet_time_t = ITEM_BULLET_TIME_DURATION
                self.items[self.holding] = 0
            elif self.items[self.holding] == 5:
                assets_manager.play_sound("launch_missile")
                self.vx -= np.cos(self.dir) * 100
                self.vy += np.sin(self.dir) * 100
                self.shoot_missile()
                self.items[self.holding] = 0
            elif self.items[self.holding] == 6:  # earthquake
                self.game.start_earthquake()
                self.items[self.holding] = 0

        self.missiles.update(t)

        self.apply_friction()

        if self.item_invincible:
            self.item_invincible_time -= t
            if self.item_invincible_time <= 0:
                self.item_invincible = False
                self.image = self.ori_image
            else:
                self.image = self.ori_image.copy()
                self.image.fill(self.invincible_color, special_flags=pygame.BLEND_RGB_MULT)
                self.invincible_color += 0xFFFFFF // (60 * ITEM_INVINCIBILITY_TIME)

        self.shadow_rect.left = self.real_x - 5
        self.shadow_rect.top = self.real_y + 5
        self.rect.left = self.real_x
        self.rect.top = self.real_y
        if self.shield.activate:
            self.shield.update(t, self.rect.center)

    def draw(self, window: pygame.Surface) -> None:
        for missile in self.missiles:
            missile.draw(window)
        window.blit(self.shadow, self.shadow_rect)
        window.blit(self.image, self.rect)
        if self.shield.activate:
            self.shield.draw(window)

    def in_bounds(self) -> bool:
        return BUILDING_HEIGHT < self.real_y < SCREEN_HEIGHT - PLAYER_HEIGHT

    def shoot_missile(self) -> None:
        new_missile = Missile(self.rect.center, self.dir)
        self.missiles.add(new_missile)

    def resolve_collision(self, obstacle: Obstacle) -> None:
        obstacle_left = obstacle.pos.x - OBSTACLE_WIDTH // 2
        obstacle_right = obstacle.pos.x + OBSTACLE_WIDTH // 2
        obstacle_top = obstacle.pos.y - OBSTACLE_HEIGHT // 2
        obstacle_bottom = obstacle.pos.y + OBSTACLE_HEIGHT // 2
        self_left = self.real_x
        self_right = self.real_x + PLAYER_WIDTH
        self_top = self.real_y
        self_bottom = self.real_y + PLAYER_HEIGHT

        distances = [
            (self_right - obstacle_left, 0), (obstacle_right - self_left, 1),
            (self_bottom - obstacle_top, 2), (obstacle_bottom - self_top, 3)
        ]
        distances = [x for x in distances if x[0] >= 0]
        distances.sort()

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
        self.shadow_rect.left = self.real_x - 5
        self.shadow_rect.top = self.real_y + 5

    def hit(self) -> bool:
        if self.is_invincible():
            return False

        if self.shield.activate:
            self.shield.hit()
            return True

        assets_manager.play_sound("explosion")
        self.invincibility_after_damage = INVINCIBILITY_AFTER_DAMAGE
        self.hp = max(self.hp - 1, 0)
        self.blink_cooldown = PLAYER_BLINK_COOLDOWN
        return True

    def is_invincible(self) -> bool:
        return self.item_invincible or self.invincibility_after_damage > 0

    def become_item_invincible(self):
        self.item_invincible = True
        self.item_invincible_time = ITEM_INVINCIBILITY_TIME
        self.invincible_color = 0x000000

    def add_coin(self):
        self.game.coins += 1
        self.game.score_manager.score += 100
