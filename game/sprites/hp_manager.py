import pygame

from game.assets_manager import assets_manager


class HPManager(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, game) -> None:
        super().__init__()

        self.image = assets_manager.images['HP4']
        self.outline_image = self.image.copy()
        self.outline_image.fill(0x000000, special_flags=pygame.BLEND_RGB_MULT)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.game = game
        self.at_shop = False

    def update(self, t: float):
        if self.at_shop:
            self.image = assets_manager.images[f'HP{self.game.player.hp}_shop']
        else:
            self.image = assets_manager.images[f'HP{self.game.player.hp}']
        self.outline_image = self.image.copy()
        self.outline_image.fill(0x000000, special_flags=pygame.BLEND_RGB_MULT)

    def draw(self, window: pygame.Surface):
        window.blit(self.outline_image, self.rect.move(-3, 3))
        window.blit(self.outline_image, self.rect.move(-3, -3))
        window.blit(self.outline_image, self.rect.move(3, 3))
        window.blit(self.outline_image, self.rect.move(3, -3))
        window.blit(self.image, self.rect)
