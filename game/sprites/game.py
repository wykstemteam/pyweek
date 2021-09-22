import pygame
import pygame_gui
import numpy as np

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import Player, PoliceCar, Road, ObstacleManager, BuildingManager, Warn


class Game:
    def __init__(self) -> None:
        self.roads = pygame.sprite.Group(
            Road(assets_manager.images['road'], 0, BUILDING_HEIGHT),
            Road(assets_manager.images['road'], SCREEN_WIDTH, BUILDING_HEIGHT),
        )
        self.policecar = PoliceCar(
            assets_manager.images['policecar'], (20, 280), assets_manager.images['bullet'])
        self.warn = Warn(
            assets_manager.images['warning sign'], 30, 300
        )
        self.player = Player(
            assets_manager.images['player'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.buildings = BuildingManager()  # copied code to building.py
        self.obstacle_manager = ObstacleManager()
        self.arrow_image = pygame.transform.rotate(assets_manager.images['arrow'], self.player.dir * 360 // (2 * np.pi) )
        self.arrow_rect = self.arrow_image.get_rect(center = assets_manager.images['arrow'].get_rect(center = (self.player.rect.left + (PLAYER_WIDTH / 2) , self.player.rect.top + (PLAYER_HEIGHT / 2))).center)
        self.arrow_rect.left += np.cos(self.player.dir) * 150
        self.arrow_rect.top -= np.sin(self.player.dir) * 150

        assets_manager.stop_music()
        assets_manager.play_music("8bitaggressive1")

        self.lose_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100),
                (100, 50)
            ),
            text='Restart',
            manager=self.lose_screen
        )
        self.lose = False

    def event_process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if self.lose:
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.restart_button:
                            self.__init__()
                            self.lose = False
            self.lose_screen.process_events(event)

    def update(self, t):
        if not self.lose:
            self.roads.update(t)
            self.player.update(t)
            self.policecar.update(t)
            self.buildings.update(t)
            self.obstacle_manager.update(t)
            self.arrow_image = pygame.transform.rotate(assets_manager.images['arrow'], self.player.dir * 360 // (2 * np.pi) )
            self.arrow_rect = self.arrow_image.get_rect(center = assets_manager.images['arrow'].get_rect(center = (self.player.rect.left + (PLAYER_WIDTH / 2) , self.player.rect.top + (PLAYER_HEIGHT / 2))).center)
            self.arrow_rect.left += np.cos(self.player.dir) * 150
            self.arrow_rect.top -= np.sin(self.player.dir) * 150
        
        if not self.player.in_bounds():
            if not self.lose:
                assets_manager.stop_music()
                assets_manager.play_music("greensleeves")
            self.lose = True
        self.lose_screen.update(t)

    def draw(self, window):
        self.roads.draw(window)
        self.buildings.draw(window)
        self.policecar.draw(window)
        self.warn.draw(window)
        self.obstacle_manager.draw(window)
        window.blit(self.player.image, self.player.rect)
        window.blit(self.arrow_image, self.arrow_rect)
        if self.lose:
            window.blit(
                assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
            window.blit(
                assets_manager.images['GameOver'], pygame.Rect(0, 0, 0, 0))
            self.lose_screen.draw_ui(window)


    
