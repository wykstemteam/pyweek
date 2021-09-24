import pygame

from game.assets_manager import assets_manager


class Explode(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()

        self.animation = assets_manager.animations['explode']
        self.image = self.animation[0]
        self.rect = self.animation[0].get_rect()
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos
        self.frame = 0

    def update(self, t: float) -> bool:
        if self.frame < len(self.animation):
            self.image = self.animation[self.frame]
            self.rect = self.animation[self.frame].get_rect()
            self.rect.center = self.pos
            self.frame += 1
            return True
        return False

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)
