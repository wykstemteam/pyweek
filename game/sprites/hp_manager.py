import pygame

from game.assets_manager import assets_manager


class HPManager(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, game: 'Game') -> None:
        super().__init__()

        self.image = assets_manager.images['HP4']
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.game = game

    def update(self, t: float):
        self.image = assets_manager.images[f'HP{self.game.player.hp}']

    def draw(self, window: pygame.Surface):
        window.blit(self.image, self.rect)
