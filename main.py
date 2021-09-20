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

    def update(self, dx, dy):
        self.rect.left += dx
        self.rect.top += dy


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
        roads.update(BACKGROUND_SPEED, 0)
        player.update(-1, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.update(0, -PLAYER_SPEED)
        if keys[pygame.K_s]:
            player.update(0, PLAYER_SPEED)
        if keys[pygame.K_d]:
            player.update(PLAYER_SPEED, 0)
        if keys[pygame.K_a]:
            player.update(-PLAYER_SPEED, 0)

        roads.draw(window)
        window.blit(player.image, player.rect)
        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main()
