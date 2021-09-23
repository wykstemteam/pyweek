import numpy as np
import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import *


class Game:
    def __init__(self) -> None:
        self.roads = pygame.sprite.Group(
            Road(assets_manager.images['road'], 0),
            Road(assets_manager.images['road'], SCREEN_WIDTH),
        )
        self.player_collision_group = pygame.sprite.Group()
        self.policecar = PoliceCar(
            assets_manager.images['policecar'], pygame.Vector2(20, 280),
            assets_manager.images['bullet'], self.player_collision_group
        )
        self.bomber = Bomber()

        self.warn = Warn(assets_manager.images['warning sign'], pygame.Vector2(30, 300))
        self.player = Player(
            assets_manager.images['motorbike'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        )
        self.laser_manager = LaserManager()
        self.buildings = BuildingManager()
        self.obstacle_manager = ObstacleManager(self.player_collision_group)
        self.distance_manager = DistanceManager()
        self.arrow = Arrow(assets_manager.images['arrow'], self.player)

        # Health_bar
        self.health_bar_image = assets_manager.images['HP4']

        # game_screen
        self.game_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 100 - 10, 10), (100, 50)),
            text='Pause',
            manager=self.game_screen
        )

        # pause_screen
        self.pause_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 100 - 10, 10), (100, 50)),
            text='Return',
            manager=self.pause_screen
        )
        self.pause = False

        # lose_screen
        self.lose_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100), (100, 50)
            ),
            text='Restart',
            manager=self.lose_screen
        )
        self.return_title_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2), (100, 50)),
            text='Return',
            manager=self.lose_screen
        )
        self.lose = False

        assets_manager.play_music("8bitaggressive1")

    def event_process(self, window: pygame.Surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if not self.pause and not self.lose and event.ui_element == self.pause_button:
                    self.pause = True
                    break  # Otherwise will click both pause and return buttons

                if self.pause and event.ui_element == self.return_button:
                    self.pause = False

                if self.lose and event.ui_element == self.restart_button:
                    self.__init__()  # Reinitialize

                if self.lose and event.ui_element == self.return_title_button:
                    return True  # Stop gaming

            self.game_screen.process_events(event)
            self.pause_screen.process_events(event)
            self.lose_screen.process_events(event)

    def update(self, t):
        self.health_bar_image = assets_manager.images[f"HP{self.player.hp}"]

        if not self.lose and not self.pause:
            self.roads.update(t)
            self.buildings.update(t)
            self.player.update(t)
            self.policecar.update(t)

            # bomber
            if self.distance_manager.dist_to_next_country <= 950:
                self.bomber.goin()
            self.bomber.update(t)
            
            self.obstacle_manager.update(t)
            self.laser_manager.update(t)
            self.distance_manager.update(t)
            self.arrow_image = pygame.transform.rotate(
                assets_manager.images['arrow'], self.player.dir * 360 // (2 * np.pi)
            )
            self.arrow_rect = self.arrow_image.get_rect(
                center=assets_manager.images['arrow'].get_rect(
                    center=(
                        self.player.rect.left + (PLAYER_WIDTH / 2),
                        self.player.rect.top + (PLAYER_HEIGHT / 2)
                    )
                ).center
            )
            self.arrow_rect.left += np.cos(self.player.dir) * 150
            self.arrow_rect.top -= np.sin(self.player.dir) * 150
            self.arrow.update(self.player)

            self.player_collision()

        if self.player.hp <= 0:
            self.trigger_lose()

        self.game_screen.update(t)
        self.pause_screen.update(t)
        self.lose_screen.update(t)

    def draw(self, window: pygame.Surface):
        window.fill((0, 0, 0))
        self.roads.draw(window)
        self.buildings.draw(window)
        self.policecar.draw(window)
        self.bomber.draw(window)
        self.warn.draw(window)
        self.laser_manager.draw(window)
        self.obstacle_manager.draw(window)
        self.player.draw(window)
        self.distance_manager.draw(window)
        self.arrow.draw(window)
        window.blit(self.health_bar_image, pygame.Rect((10, 10), (400, 100)))
        if self.pause:
            window.blit(assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
            self.pause_screen.draw_ui(window)
        elif self.lose:
            window.blit(assets_manager.images['Darken'], pygame.Rect(0, 0, 0, 0))
            window.blit(assets_manager.images['GameOver'], pygame.Rect(0, 0, 0, 0))
            self.lose_screen.draw_ui(window)
        else:
            self.game_screen.draw_ui(window)

    def trigger_lose(self):
        if not self.lose and not self.pause:
            assets_manager.play_music("greensleeves")
            self.lose = True

    def player_collision(self):
        for obj in self.player_collision_group:
            if self.player.rect.colliderect(obj.rect):
                if type(obj) == PoliceCar:
                    self.trigger_lose()
                elif type(obj) == Bullet:
                    obj.player_hit(self.player)
                elif type(obj) == Obstacle:
                    self.player.resolve_collision(obj)
