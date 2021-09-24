import math

import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.screen_shake_manager import ScreenShakeManager
from game.sprites import *

# TODO: Replace self.pause and self.lose with self.state which is GAMING, PAUSE or LOSE


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
        self.bomber = Bomber(self.player_collision_group)
        self.spaceship = Spaceship(self.player_collision_group)
        self.ufo = UFO(self.player_collision_group)
        self.player = Player(
            assets_manager.images['motorbike'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self
        )
        self.laser_manager = LaserManager(self.player_collision_group)
        self.buildings = BuildingManager()
        self.obstacle_manager = ObstacleManager(self.player_collision_group)
        self.distance_manager = DistanceManager()
        self.arrow = Arrow(assets_manager.images['arrow'], self.player)
        self.screen_shake_manager = ScreenShakeManager()
        # self.screen_shake_manager.shaking = True

        self.fade_in_manager = FadeInManager(assets_manager.images['gradient_line'])
        self.fade_in_manager.start_fade_in()

        # Health_bar
        self.health_bar_image = assets_manager.images['HP4']

        # shop
        self.beach_image = assets_manager.images['beach_full']
        self.shop = False
        self.show_sea_time = SHOW_SEA_TIME
        self.show_shop_animation = False
        self.dimming = False
        self.darken_alpha = 0
        self.beach_rect = pygame.Rect(0, 0, 0, 0)

        #coins
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

        assets_manager.play_music("8bitaggressive1")

        # items
        self.bullet_time = False
        self.bullet_time_t = ITEM_BULLET_TIME_DURATION
        self.earthquake_time = ITEM_EARTHQUAKE_DURATION
        self.earthquake = False

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
        self.player.hp = max(self.player.hp, 0)
        self.health_bar_image = assets_manager.images[f"HP{self.player.hp}"]

        if self.show_shop_animation:
            if self.player.go_right(t) and not self.dimming:
                self.dimming = True
            return

        if self.bullet_time:
            self.bullet_time_t -= t
            if self.bullet_time_t <= 0:
                self.bullet_time_t = ITEM_BULLET_TIME_DURATION
                self.bullet_time = False
            else:
                rate = 0
                if ITEM_BULLET_TIME_DURATION - self.bullet_time_t <= 1:
                    rate = -math.sqrt(
                        (ITEM_BULLET_TIME_DURATION - self.bullet_time_t) * (1 - BULLET_TIME_RATE)**2
                    ) + 1
                else:
                    rate = (1 - BULLET_TIME_RATE) * (
                        (1 - self.bullet_time_t / (ITEM_BULLET_TIME_DURATION - 1))**2
                    ) + BULLET_TIME_RATE
                t *= rate
                print(rate, sep=' ')

        if not self.lose and not self.pause:
            self.fade_in_manager.update(t)
            self.roads.update(t)
            self.buildings.update(t, self.shop)
            self.player.update(t if not self.bullet_time else t / rate)
            self.policecar.update(t, self.shop)

            # bomber
            # if self.distance_manager.dist >= BOMBER_APPEAR_DIST-1 and self.distance_manager.dist <= BOMBER_APPEAR_DIST+1:
            #    self.bomber.activated = True
            # self.bomber.aim(self.player.rect.centerx, self.player.rect.centery)
            # self.bomber.update(t)

            # spaceship
            # TODO: Hitbox for laser
            # if self.distance_manager.dist >= 50 and self.distance_manager.dist <= 51:
            #    self.spaceship.activated = True
            # if self.distance_manager.dist >= 70 and self.distance_manager.dist <= 71:
            #    self.spaceship.is_charge = True
            # self.spaceship.update(t)

            # UFO
            if 50 <= self.distance_manager.dist <= 51:
                self.ufo.activated = True
            self.ufo.update(t)

            self.obstacle_manager.update(t, self.shop)
            self.coin_manager.update(t)
            self.arrow.update(self.player)
            self.laser_manager.update(t, self.shop)
            if self.shop:
                self.beach_rect.move_ip(BACKGROUND_VELOCITY // 100, 0)
            if not self.shop:
                self.distance_manager.update(t)
                self.player_collision()
            else:
                self.show_sea_time -= t
                if self.show_sea_time <= 0:
                    self.show_shop_animation = True

        if self.player.hp <= 0 and not self.shop and not self.lose:
            print(self.player.hp)
            if not PLAYER_INVIN:
                self.trigger_lose()

        if self.distance_manager.dist_to_next_country <= 0 and not self.shop:
            self.trigger_shop()

        self.game_screen.update(t)
        self.pause_screen.update(t)
        self.lose_screen.update(t)

        if self.earthquake:
            self.earthquake_time -= t
            if self.earthquake_time <= 0:
                self.earthquake = False
                self.screen_shake_manager.shaking = False
            else:
                for obj in self.player_collision_group:
                    if type(obj) not in (PoliceCar, Spaceship):
                        obj.kill()

    def draw(self, window: pygame.Surface) -> None:
        window.fill((0, 0, 0))
        self.roads.draw(window)
        if self.shop:
            window.blit(self.beach_image, self.beach_rect)
        self.buildings.draw(window)
        self.policecar.draw(window)
        self.laser_manager.draw(window)
        self.obstacle_manager.draw(window)
        self.coin_manager.draw(window)
        self.player.draw(window)
        self.arrow.draw(window)

        # objects that fly
        self.bomber.draw(window)
        self.spaceship.draw(window)
        self.ufo.draw(window)
        self.fade_in_manager.draw(window)

        self.distance_manager.draw(window)

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
            self.darken_alpha = min(self.darken_alpha + 1, 255)
            return

        self.screen_shake_manager.shake(window)

    def trigger_lose(self) -> None:
        if not self.lose and not self.pause:
            assets_manager.play_music("ensolarado")
            self.lose = True

    def trigger_shop(self) -> None:
        if not self.shop and not self.pause:
            assets_manager.play_music("mid_afternoon_mood")
            self.shop = True
            self.bomber.activated = False
            self.spaceship.activated = False
            self.ufo.activated = False

    def player_collision(self) -> None:
        for obj in self.player_collision_group:
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