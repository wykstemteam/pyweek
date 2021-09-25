import pygame

from game.constants import *
from game.assets_manager import assets_manager
from game.sprites.player import Player


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__()

        self.animation = assets_manager.animations['coin']
        self.rect = self.animation[0].get_rect()
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos

        self.frame = 0

    def update(self, t: float) -> None:
        self.image = self.animation[int(self.frame)]
        self.rect.move_ip(BACKGROUND_VELOCITY * t, 0)
        self.frame += 0.5
        if self.frame > len(self.animation) - 1:
            self.frame -= len(self.animation)
        if self.rect.right <= 0:
            self.kill()

    def player_hit(self, player: Player) -> None:  # should be called when collided by player
        player.coins += 1
        self.kill()
        assets_manager.play_sound("coin")

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
