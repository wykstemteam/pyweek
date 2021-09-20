import pygame

from assets_manager import AssetsManager
from constants import *

assets_manager = AssetsManager()


class Background(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, dx, dy):
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


def main():
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    assets_manager.images['road'] = pygame.transform.scale(assets_manager.images['road'], (SCREEN_WIDTH, SCREEN_HEIGHT))
    backgrounds = pygame.sprite.Group(
        Background(assets_manager.images['road'], 0, 0),
        Background(assets_manager.images['road'], SCREEN_WIDTH, 0),
    )

    clock = pygame.time.Clock()

    running = True
    while running:
        backgrounds.update(3, 0)
        backgrounds.draw(window)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)


if __name__ == '__main__':
    main()
