import pygame

from game.constants import *
from assets_manager import assets_manager

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__()

        self.animation = assets_manager.animations['coin']
        self.rect = self.animation[0].get_rect()
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.explode = None

    def update(self, t: float) -> None:
        if not self.explode:
            self.pos += pygame.Vector2(self.velocity_x, self.velocity_y) * t
            self.rect.center = self.pos
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.kill()
        elif not self.explode.update(t):
            self.kill()

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
