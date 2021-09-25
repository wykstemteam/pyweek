import math
from enum import Enum

import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.screen_shake_manager import ScreenShakeManager
from game.sprites import *


class Scenes(Enum):
    CITY = 1
    SHOP = 2
    SPACE = 3


class Game:
    def __init__(self) -> None:
        self.cur_scene = Scenes.CITY

        # objects in all scenes
        # ================================================================================================
        self.player = Player(
            assets_manager.images['motorbike'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self
        )
        self.player_collision_group = pygame.sprite.Group()
        self.laser_manager = LaserManager(self.player_collision_group)
        self.arrow = Arrow(assets_manager.images['arrow'], self.player)
        self.distance_manager = DistanceManager()
        self.screen_shake_manager = ScreenShakeManager()
        # self.screen_shake_manager.shaking = True
        self.fade_in_manager = FadeInManager(assets_manager.images['gradient_line'])
        self.fade_in_manager.start_fade_in()
        # Health_bar
        self.health_bar_image = assets_manager.images['HP4']
        # coins
        self.coin_manager = CoinManager(self.player_collision_group)

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

        # items
        self.bullet_time = False
        self.bullet_time_t = ITEM_BULLET_TIME_DURATION
        self.rate = 1.0
        self.earthquake_time = ITEM_EARTHQUAKE_DURATION
        self.earthquake = False

        # entering shop
        self.reached_checkpoint = False
        self.show_shop_animation = False
        self.dimming = False
        self.darken_alpha = 0
        self.show_sea_time = SHOW_SEA_TIME

        self.shop_scene = Shop(
            assets_manager.images['confirm_button'], assets_manager.images['main_menu'],
            assets_manager.images['darken']
        )

        # objects in scene.CITY
        # ================================================================================================
        self.roads = pygame.sprite.Group(
            Road(assets_manager.images['road'], 0),
            Road(assets_manager.images['road'], SCREEN_WIDTH),
        )
        self.policecar = PoliceCar(
            assets_manager.images['policecar'], pygame.Vector2(20, 280),
            assets_manager.images['bullet'], self.player_collision_group
        )
        self.bomber = Bomber(self.player_collision_group)
        self.buildings = BuildingManager()
        self.obstacle_manager = ObstacleManager(self.player_collision_group)
        self.beach_image = assets_manager.images['beach_full']
        self.beach_rect = pygame.Rect(0, 0, 0, 0)

        # objects in scene.SHOP
        # ================================================================================================

        # objects in scene.SPACE
        # ================================================================================================
        self.spaceship = Spaceship(self.player_collision_group)
        self.ufo = UFO(self.player_collision_group)
        self.spaceship.activated = True

        assets_manager.play_music("8bitaggressive1")

    def event_process(self, window: pygame.Surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if not self.pause and not self.lose and event.ui_element == self.pause_button:
                    self.pause = True
                    break  # Otherwise will click both pause and return buttons
                elif self.pause and event.ui_element == self.return_button:
                    self.pause = False
                elif self.lose:
                    if event.ui_element == self.restart_button:
                        self.__init__()  # Reinitialize
                    elif event.ui_element == self.return_title_button:
                        return True  # Stop gaming

            self.game_screen.process_events(event)
            self.pause_screen.process_events(event)
            self.lose_screen.process_events(event)

    def update(self, t: float) -> None:
        # objects in all scenes:
        if not self.lose and not self.pause:
            if self.bullet_time:
                self.bullet_time_t -= t
                if self.bullet_time_t <= 0:
                    self.bullet_time_t = ITEM_BULLET_TIME_DURATION
                    self.bullet_time = False
                else:
                    self.rate = 0
                    if ITEM_BULLET_TIME_DURATION - self.bullet_time_t <= 1:
                        self.rate = -math.sqrt(
                            (ITEM_BULLET_TIME_DURATION - self.bullet_time_t) *
                            (1 - BULLET_TIME_RATE)**2
                        ) + 1
                    else:
                        self.rate = (1 - BULLET_TIME_RATE) * (
                            (1 - self.bullet_time_t / (ITEM_BULLET_TIME_DURATION - 1))**2
                        ) + BULLET_TIME_RATE
                    t *= self.rate

            self.player.hp = max(self.player.hp, 0)
            self.health_bar_image = assets_manager.images[f"HP{self.player.hp}"]
            if self.show_shop_animation:
                self.arrow.rect.left += -BACKGROUND_VELOCITY * t
                if self.player.go_right(t) and not self.dimming:
                    self.dimming = True
                return

            self.fade_in_manager.update(t)
            self.player.update(t if not self.bullet_time else t / self.rate)
            self.player_collision()
            self.coin_manager.update(t)
            self.arrow.update(self.player)
            if self.reached_checkpoint:
                self.beach_rect.move_ip(BACKGROUND_VELOCITY // 200, 0)
                self.show_sea_time -= t
                if self.show_sea_time <= 0:
                    self.show_shop_animation = True
            else:
                if self.distance_manager.dist_to_next_country <= 0:
                    self.trigger_shop()
                self.distance_manager.update(t)

            if self.player.hp <= 0:
                if not PLAYER_INVIN:
                    self.trigger_lose()

            if self.earthquake:
                self.earthquake_time -= t
                if self.earthquake_time <= 0:
                    self.earthquake = False
                    self.screen_shake_manager.shaking = False
                else:
                    for obj in self.player_collision_group:
                        if type(obj) not in (PoliceCar, Bomber, Spaceship, UFO, Coin):
                            obj.kill()

        # objects in scene.SHOP:

        # objects in scene.CITY:
        if self.cur_scene == Scenes.CITY:
            if not self.lose and not self.pause:
                self.laser_manager.update(t)
                self.roads.update(t)
                self.buildings.update(t)
                self.policecar.update(t)
                self.bomber.aim(self.player.rect.centerx, self.player.rect.centery)
                self.bomber.update(t)
                self.obstacle_manager.update(t)

        # objects in scene.SPACE:
        if self.cur_scene == Scenes.SPACE:
            if not self.lose and not self.pause:
                if 50 <= self.distance_manager.dist <= 51:
                    self.spaceship.is_charge = True
                self.spaceship.update(t)
                self.ufo.update(t)

        # gui
        self.game_screen.update(t)
        self.pause_screen.update(t)
        self.lose_screen.update(t)

    def draw(self, window: pygame.Surface) -> None:
        window.fill((0, 0, 0))

        # objects in the ground:
        if self.cur_scene == Scenes.CITY:
            self.roads.draw(window)
        if self.cur_scene == Scenes.SPACE:
            window.blit(assets_manager.images['space_background1'], pygame.Rect(0, -200, 0, 0))

        # objects on the ground:
        self.coin_manager.draw(window)
        self.player.draw(window)

        if self.cur_scene == Scenes.CITY:
            self.laser_manager.draw(window)
            if self.reached_checkpoint:
                window.blit(self.beach_image, self.beach_rect)
            self.buildings.draw(window)
            self.policecar.draw(window)
            self.obstacle_manager.draw(window)

        # objects that fly in the sky:
        self.arrow.draw(window)
        self.fade_in_manager.draw(window)
        self.distance_manager.draw(window)

        if self.cur_scene == Scenes.CITY:
            self.bomber.draw(window)

        if self.cur_scene == Scenes.SPACE:
            self.spaceship.draw(window)
            self.ufo.draw(window)

        if self.cur_scene == Scenes.SHOP:
            self.shop_scene.appear(window)

        window.blit(self.health_bar_image, pygame.Rect((10, 10), (400, 100)))
        if self.pause:
            window.blit(assets_manager.images['darken'], pygame.Rect(0, 0, 0, 0))
            self.pause_screen.draw_ui(window)
        elif self.lose:
            window.blit(assets_manager.images['darken'], pygame.Rect(0, 0, 0, 0))
            window.blit(assets_manager.images['GameOver'], pygame.Rect(0, 0, 0, 0))
            self.lose_screen.draw_ui(window)
        else:
            self.game_screen.draw_ui(window)

        if self.dimming:
            darken_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken_image.fill((0, 0, 0))
            darken_image.set_alpha(self.darken_alpha)
            window.blit(darken_image, pygame.Rect(0, 0, 0, 0))
            self.darken_alpha = min(self.darken_alpha + 2, 255)
            if self.darken_alpha == 255:
                self.shop_scene.appear(window)

        self.screen_shake_manager.shake(window)

    def trigger_lose(self) -> None:
        if not self.lose and not self.pause:
            assets_manager.play_music("ensolarado")
            self.lose = True

    def trigger_shop(self) -> None:
        if not self.reached_checkpoint and not self.pause:
            assets_manager.play_music("mid_afternoon_mood")
            self.reached_checkpoint = True
            self.bomber.activated = False
            self.spaceship.activated = False
            self.ufo.activated = False
            self.laser_manager.reached_checkpoint = True
            self.obstacle_manager.reached_checkpoint = True
            self.policecar.reached_checkpoint = True
            self.buildings.reached_checkpoint = True
            self.coin_manager.reached_checkpoint = True

    def player_collision(self) -> None:
        for obj in self.player_collision_group:
            if self.reached_checkpoint and type(obj) not in (Coin, Obstacle):
                continue
            if type(obj) == Spaceship:
                obj.collision_player(self.player)
            if self.player.rect.colliderect(obj.rect):
                if type(obj) == PoliceCar and not PLAYER_INVIN:
                    self.trigger_lose()
                elif type(obj) in (Bullet, MissileAircraft):
                    obj.player_hit(self.player)
                elif type(obj) == Obstacle:
                    self.player.resolve_collision(obj)
                elif type(obj) == Coin:
                    obj.player_hit(self.player)

    def start_earthquake(self):
        self.screen_shake_manager.shaking = True
        self.earthquake = True
        self.earthquake_time = ITEM_EARTHQUAKE_DURATION
