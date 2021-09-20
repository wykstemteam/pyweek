import time
import pygame

from assets_manager import AssetsManager
from constants import *

assets_manager = AssetsManager()


class Road(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, dx: int, dy: int):
        self.rect.left += dx
        if self.rect.left > self.width:
            self.rect.left -= self.width * 2
        elif self.rect.right < 0:
            self.rect.left += self.width * 2
        self.rect.top += dy
        if self.rect.top > self.height:
            self.rect.top -= self.height * 2
        elif self.rect.bottom < 0:
            self.rect.top += self.height * 2


class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.imageL = pygame.transform.flip(image, True, False)
        self.imageR = pygame.transform.flip(image, False, False)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vx = 0.0
        self.vy = 0.0

    def acc(self, dx, dy):
        self.vx += dx
        self.vy += dy

    def friction(self):
        if self.vx > 0:
            self.vx -= FRICTION
        elif self.vx < 0:
            self.vx += FRICTION
        
        if self.vy > 0:
            self.vy -= FRICTION
        elif self.vy < 0:
            self.vy += FRICTION

    def update_pos(self, t):
        self.rect.left += self.vx * t
        self.rect.top += self.vy * t


def main():
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    assets_manager.images['road'] = pygame.transform.scale(
        assets_manager.images['road'], (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    roads = pygame.sprite.Group(
        Road(assets_manager.images['road'], 0, 0),
        Road(assets_manager.images['road'], SCREEN_WIDTH, 0),
    )
    assets_manager.images['player'] = pygame.transform.scale(assets_manager.images['player'], (PLAYER_WIDTH, PLAYER_HEIGHT))
    player = Player(assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    clock = pygame.time.Clock()

    running = True
    while running:
        t = clock.get_time()
        t = t // 10
        print(t)

        roads.update(BACKGROUND_SPEED, 0)
        player.acc(BACKGROUND_ACC, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.acc(0, -PLAYER_ACC)
        if keys[pygame.K_s]:
            player.acc(0, PLAYER_ACC)
        if keys[pygame.K_d]:
            player.acc(PLAYER_ACC, 0)
        if keys[pygame.K_a]:
            player.acc(-PLAYER_ACC, 0)

        player.friction()
        player.update_pos(t)

        roads.draw(window)
        window.blit(player.image, player.rect)
        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main()
