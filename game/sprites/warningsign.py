import pygame


class Warn(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        print(self.width)

    def update(self, t):
        self.kill()

    def draw(self, window):
        window.blit(self.image, self.rect)
