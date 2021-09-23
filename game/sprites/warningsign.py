import pygame


class Warn(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, t):
        self.kill()

    def draw(self, window):
        window.blit(self.image, self.rect)
