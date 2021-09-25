import pygame

from game.constants import *
from game.sprites.explode import Explode
from game.sprites.player import Player


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

    def update(self, t: float) -> None:
        if not self.explode:
            self.pos += pygame.Vector2(self.velocity_x, self.velocity_y) * t
            self.rect.center = self.pos
            if not self.in_bounds():
                self.kill()
        elif not self.explode.update(t):
            self.kill()

    def in_bounds(self) -> bool:
        return self.rect.right > 0 and self.rect.left < SCREEN_WIDTH and self.rect.bottom > 0 and self.rect.top < SCREEN_HEIGHT

    def player_hit(self, player: Player) -> None:  # should be called when collided by player
        if not self.explode:
            if player.hit():
                self.image = None
                self.explode = Explode(self.rect.center)

    def draw(self, window: pygame.Surface) -> None:
        if self.image:
            window.blit(self.image, self.rect)
        elif self.explode and self.explode.image:
            window.blit(self.explode.image, self.explode.rect)
