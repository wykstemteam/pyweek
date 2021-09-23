import pygame

from game.constants import *
from game.sprites.explode import Explode


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, vx: float, vy: float) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity_x = vx
        self.velocity_y = vy

        self.explode = None

    def update(self, t) -> None:
        if not self.explode:
            self.pos += pygame.Vector2(self.velocity_x, self.velocity_y)*t
            self.rect.center = self.pos
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.kill()
        elif not self.explode.update(t):
            self.kill()

    def player_hit(self, player) -> None:  # should be called when collided by player
        if not self.explode:
            self.image = None
            self.explode = Explode(self.rect.center)
            player.hit()

    def draw(self, window):
        if self.image:
            window.blit(self.image, self.rect)
        elif self.explode and self.explode.image:
            window.blit(self.explode.image, self.explode.rect)
