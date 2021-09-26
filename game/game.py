import math
import random
from enum import Enum

import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.screen_shake_manager import ScreenShakeManager
from game.settings import get_audio_controls
from game.sprites import *
from game.sprites.coin_gui import CoinGUI
from game.sprites.hp_manager import HPManager
from game.sprites.inventory import Inventory
from game.sprites.comet_manager import CometManager


class Scenes(Enum):
    CITY = 1
    SPACE = 2


class Game:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()

        self.cur_scene = Scenes.CITY

        # objects in all scenes
        # ================================================================================================
        self.player = Player(
            assets_manager.images['motorbike'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self
        )
        self.player_collision_group = pygame.sprite.Group()
        self.laser_manager = LaserManager(self.player_collision_group)
        self.arrow = Arrow(assets_manager.images['arrow'], self.player)
        self.inventory = Inventory(
            [
                assets_manager.images[f'{item_name}_inventory'] for item_name in (
                    'item_blank', 'item_healpotion', 'item_shield', 'item_star', 'item_clock',
                    'item_missile', 'item_earthquake'
                )
            ], self
        )

        self.distance_manager = DistanceManager()
        self.screen_shake_manager = ScreenShakeManager()

        # self.screen_shake_manager.shaking = True
        self.fade_in_manager = FadeInManager(assets_manager.images['gradient_line'])
        self.fade_in_manager.start_fade_in()

        # Health_bar
        self.hp_manager = HPManager((10, 10), self)

        # coins
        self.coin_manager = CoinManager(self.player_collision_group)
        self.coins = 0
        self.coin_gui = CoinGUI((1200, 36), self)

        # difficulty
        self.difficulty = 1

        # game_screen
        self.game_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 100 - 10, 10), (100, 50)),
            text='Pause',
            manager=self.game_screen
        )

        # pause_screen
        self.pause_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 100 - 10, 10), (100, 50)),
            text='Return',
            manager=self.pause_screen
        )
        self.pause = False
        self.music_label, self.music_slider, self.sound_label, self.sound_slider = get_audio_controls(
            manager=self.pause_screen
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 75), (200, 50)
            ),
            text='Exit to Menu',
            manager=self.pause_screen
        )

        # lose_screen
        self.lose_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100), (100, 50)
            ),
            text='Restart',
            manager=self.lose_screen
        )
        # TODO: Maybe edit it to become like exit_button
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
        # deactivate everything for .. seconds
        self.stage1_countdown = DEACTIVATE_DURATION
        self.stage2 = False  # player at right?
        self.dimming = False
        self.darken_alpha = 0

        self.shop_scene = Shop(self)

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
        self.comets = CometManager(self.player_collision_group)

        self.set_scene_music()

    def set_scene_music(self) -> None:
        if self.cur_scene == Scenes.CITY:
            assets_manager.play_music("8bitaggressive")
        elif self.cur_scene == Scenes.SPACE:
            assets_manager.play_music("galaxy")

    def reset(self):
        self.difficulty *= 2
        self.distance_manager.dist_to_next_country = INITIAL_DISTANCE_TO_NEXT_COUNTRY
        self.stage1_countdown = DEACTIVATE_DURATION
        self.stage2 = False
        self.dimming = False
        self.darken_alpha = 0
        self.coin_manager.reached_checkpoint = False
        self.player.inputtable = True
        self.player.vx = -BACKGROUND_VELOCITY
        self.player.vy = 0.0
        self.player.real_x = SCREEN_WIDTH / 2
        self.player.real_y = SCREEN_HEIGHT / 2
        self.spaceship.activated = False
        self.ufo.activated = False
        if self.cur_scene == Scenes.CITY:
            self.policecar.activated = True
            for road in self.roads:
                road.stop_moving = False
            self.laser_manager.reached_checkpoint = False
            self.buildings.__init__()
            self.obstacle_manager.reached_checkpoint = False
            self.bomber.__init__(self.player_collision_group)
            self.beach_rect.topleft = (0, 0)
        self.comets.kill()

    def event_process(self, window: pygame.Surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if (
                event.type == pygame.USEREVENT and self.pause
                and event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED
            ):
                if event.ui_element == self.music_slider:
                    assets_manager.set_music_volume(event.value)
                elif event.ui_element == self.sound_slider:
                    assets_manager.set_sound_volume(event.value)

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if not self.pause and not self.lose and event.ui_element == self.pause_button:
                    self.pause = True
                    break  # Otherwise will click both pause and return buttons
                elif self.pause and event.ui_element == self.return_button:
                    self.pause = False
                elif self.pause and event.ui_element == self.exit_button:
                    return True
                elif self.lose:
                    if event.ui_element == self.restart_button:
                        self.__init__()  # Reinitialize
                    elif event.ui_element == self.return_title_button:
                        return True  # Stop gaming

            self.game_screen.process_events(event)
            self.pause_screen.process_events(event)
            self.lose_screen.process_events(event)

    def update(self, t: float, window: pygame.Surface) -> None:

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

            # shop
            if self.stage2:
                assets_manager.play_music("mid_afternoon_mood")
                self.shop_scene.appear(window)
                # leaving shop
                self.clock.tick(60)
                # resetting things
                self.cur_scene = random.choice(list(Scenes))
                # self.cur_scene = Scenes.CITY
                self.reset()
                self.set_scene_music()

                # ==========================================
            elif self.stage1_countdown <= 0:
                self.player.inputtable = False
                for road in self.roads:
                    road.stop_moving = True
                self.player.vx = -BACKGROUND_VELOCITY * 2.5
                if self.player.rect.left >= SCREEN_WIDTH:
                    self.dimming = True
                    pygame.mixer.music.fadeout(3000)
            elif self.distance_manager.dist_to_next_country <= 0:
                self.coin_manager.reached_checkpoint = True
                self.laser_manager.reached_checkpoint = True
                self.buildings.reached_checkpoint = True
                self.obstacle_manager.reached_checkpoint = True
                self.policecar.activated = False
                self.bomber.activated = False
                self.ufo.activated = False
                self.spaceship.activated = False
                self.beach_rect.move_ip(BACKGROUND_VELOCITY / 2 * t, 0)
                self.stage1_countdown -= t

            self.player.hp = max(self.player.hp, 0)

            self.fade_in_manager.update(t)
            self.player.update(t if not self.bullet_time else t / self.rate)
            self.player_collision()
            self.coin_manager.update(t)
            self.arrow.update(self.player)
            self.distance_manager.update(t)
            self.coin_gui.update(t)
            self.hp_manager.update(t)

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

        # objects in scene.CITY:
        if self.cur_scene == Scenes.CITY:
            if not self.lose and not self.pause:
                self.laser_manager.update(t)
                self.roads.update(t)
                self.buildings.update(t)
                self.policecar.update(t)
                if self.distance_manager.dist_to_next_country > 0:
                    if self.distance_manager.dist_to_next_country > 150:
                        self.bomber.random_activate(self.difficulty)
                self.bomber.aim(self.player.rect.centerx, self.player.rect.centery)
                self.bomber.update(t, self.difficulty)
                self.obstacle_manager.update(t)

        # objects in scene.SPACE:
        if self.cur_scene == Scenes.SPACE:
            if not self.lose and not self.pause:
                if self.distance_manager.dist_to_next_country > 30:
                    if not self.spaceship.activated:
                        self.ufo.random_activate(self.difficulty)
                    if not self.ufo.activated:
                        self.spaceship.random_activate(self.difficulty)

                    if (
                        self.distance_manager.dist_to_next_country > 30 and self.spaceship.activated
                        and self.spaceship.x == 1000 and not self.spaceship.is_charge
                        and not self.spaceship.is_shoot and self.spaceship.activated_dur >= 10.0
                        and random.randint(0, 1000) <= self.difficulty
                    ):
                        self.spaceship.is_charge = True

                    self.comets.add(self.difficulty)

                self.spaceship.update(t)
                self.ufo.update(t, self.difficulty)
                self.comets.update(t, self.difficulty)

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
            if self.distance_manager.dist_to_next_country <= 0:
                window.blit(self.beach_image, self.beach_rect)
            self.buildings.draw(window)
            self.policecar.draw(window)
            self.obstacle_manager.draw(window)

        # objects that fly in the sky:
        self.arrow.draw(window)
        self.fade_in_manager.draw(window)

        if self.cur_scene == Scenes.CITY:
            self.bomber.draw(window)
        elif self.cur_scene == Scenes.SPACE:
            self.spaceship.draw(window)
            self.ufo.draw(window)
            self.comets.draw(window)

        # gui
        if self.pause:
            window.blit(assets_manager.images['darken'], pygame.Rect(0, 0, 0, 0))
            self.pause_screen.draw_ui(window)
        elif self.lose:
            window.blit(assets_manager.images['darken'], pygame.Rect(0, 0, 0, 0))
            window.blit(assets_manager.images['GameOver'], pygame.Rect(0, 0, 0, 0))
            self.lose_screen.draw_ui(window)
        else:
            self.game_screen.draw_ui(window)
        self.distance_manager.draw(window)
        self.coin_gui.draw(window)
        self.hp_manager.draw(window)
        self.inventory.draw(window)

        if self.dimming:
            darken_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken_image.fill((0, 0, 0))
            darken_image.set_alpha(self.darken_alpha)
            window.blit(darken_image, pygame.Rect(0, 0, 0, 0))
            self.darken_alpha = min(self.darken_alpha + 3, 255)
            if self.darken_alpha == 255:
                self.stage2 = True

        self.screen_shake_manager.shake(window)

    def trigger_lose(self) -> None:
        if not self.lose and not self.pause:
            assets_manager.play_music("ensolarado")
            self.lose = True

    def player_collision(self) -> None:
        for obj in self.player_collision_group:
            if (
                self.distance_manager.dist_to_next_country == 0
                and type(obj) not in (Coin, Obstacle)
            ):
                continue
            if type(obj) in (Spaceship, Comet):
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

    def start_earthquake(self) -> None:
        self.screen_shake_manager.shaking = True
        self.earthquake = True
        self.earthquake_time = ITEM_EARTHQUAKE_DURATION

    def run(self, window) -> None:
        while True:
            t = self.clock.get_time()

            if self.event_process(window):  # Returns True if stop gaming
                return

            self.update(t / 1000, window)
            self.draw(window)
            pygame.display.flip()
            self.clock.tick(60)

            if SHOW_FPS:
                print(f'fps = {0 if t == 0 else 1000 / t}')
