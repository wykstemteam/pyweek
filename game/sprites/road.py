import pygame


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
