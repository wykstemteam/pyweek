import math
import random
from enum import Enum

import numpy as np
import pygame
import pygame_gui

from game.assets_manager import assets_manager
from game.constants import *
from game.pause import pause
from game.screen_shake_manager import ScreenShakeManager
from game.shop import Shop
from game.sprites import *
from game.sprites.round_counter import RoundCounter

font = pygame.font.Font(FONT_PATH, 40)


class Scenes(Enum):
    CITY = 1
    SPACE = 2


class Game:
    def __init__(self, highscore: int) -> None:
        self.clock = pygame.time.Clock()

        self.cur_scene = Scenes.CITY

        # objects in all scenes
        # ================================================================================================
        self.player = Player(
            assets_manager.images['motorbike'], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self
        )
        self.player_collision_group = pygame.sprite.Group()
        self.missile_collision_group = pygame.sprite.Group()
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

        self.round_counter = RoundCounter()
        self.distance_manager = DistanceManager(self)
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
        self.difficulty = INITIAL_DIFFICULTY

        # game_screen
        self.game_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 100 - 10, 10), (100, 50)),
            text='Pause',
            manager=self.game_screen
        )

        # lose_screen
        self.lose_screen = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "menu_theme.json")
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (SCREEN_WIDTH // 2 - 172, SCREEN_HEIGHT // 2 + 75), (130, 50)
            ),
            text='Restart',
            manager=self.lose_screen
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 28, SCREEN_HEIGHT // 2 + 75), (200, 50)),
            text='Exit to Menu',
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
        self.missile_collision_group.add(self.policecar)
        self.missile_collision_group.add(self.bomber)
        self.buildings = BuildingManager()
        self.obstacle_manager = ObstacleManager(self.player_collision_group)
        self.beach_image = assets_manager.images['beach_full']
        self.beach_rect = pygame.Rect(0, 0, 0, 0)

        # objects in scene.SPACE
        # ================================================================================================
        self.spaceship = Spaceship(self.player_collision_group, self)
        self.ufo = UFO(self.player_collision_group, self)
        self.comets = CometManager(self.player_collision_group)
        self.missile_collision_group.add(self.ufo)
        self.missile_collision_group.add(self.spaceship)
        self.space_temp_deactivated_enemies = False
        self.space_temp_deactivated_enemies_t = SPACE_ENEMIES_DEACTIVATE_DURATION

        self.set_scene_music()
        self.play_quote()
        self.score: int = 0
        self.highscore: int = highscore

    def play_quote(self) -> None:
        if not assets_manager.play_quotes:
            return
        if self.cur_scene == Scenes.CITY:
            assets_manager.play_sound("long_road")
        elif self.cur_scene == Scenes.SPACE:
            assets_manager.play_sound("crazy_universe")

    def set_scene_music(self) -> None:
        if self.cur_scene == Scenes.CITY:
            assets_manager.play_music("8bitaggressive")
        elif self.cur_scene == Scenes.SPACE:
            assets_manager.play_music("galaxy")

    def reset(self):
        self.difficulty *= 2
        self.distance_manager.dist_to_next_country = INITIAL_DISTANCE_TO_NEXT_COUNTRY * (1 + (np.log2(self.difficulty) / 5))
        self.stage1_countdown = DEACTIVATE_DURATION
        self.stage2 = False
        self.dimming = False
        self.darken_alpha = 0
        self.coin_manager.__init__(self.player_collision_group)
        self.player.item_invincible = False
        self.player.shield.activate = False
        self.player.inputtable = True
        self.player.vx = -BACKGROUND_VELOCITY
        self.player.vy = 0.0
        self.player.real_x = SCREEN_WIDTH / 2
        self.player.real_y = SCREEN_HEIGHT / 2
        self.spaceship.activated = False
        self.ufo.activated = False
        self.comets.kill()
        self.kill_bullets()
        if self.cur_scene == Scenes.CITY:
            self.policecar.activated = True
            for road in self.roads:
                road.stop_moving = False
            self.laser_manager.reached_checkpoint = False
            self.buildings.__init__()
            self.obstacle_manager.reached_checkpoint = False
            self.bomber.__init__(self.player_collision_group)
            self.beach_rect.topleft = (0, 0)

        self.set_scene_music()
        self.play_quote()
        self.round_counter.increment()
        self.fade_in_manager.start_fade_in()

    def event_process(self, window: pygame.Surface):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if self.lose:
                    if event.ui_element == self.restart_button:
                        self.__init__()  # Reinitialize
                    elif event.ui_element == self.exit_button:
                        return True  # Stop gaming
                elif event.ui_element == self.pause_button:
                    return pause(window, self)

            self.game_screen.process_events(event)
            self.lose_screen.process_events(event)

    def update(self, t: float, window: pygame.Surface) -> None:
        # objects in all scenes:
        if not self.lose:
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
                self.add_scene_score()
                self.shop_scene.appear(window)
                # leaving shop
                self.clock.tick(60)
                # resetting things
                self.cur_scene = random.choice(list(Scenes))
                # self.cur_scene = Scenes.CITY
                self.reset()

                # ==========================================
            elif self.stage1_countdown <= 0:
                self.player.inputtable = False
                for road in self.roads:
                    road.stop_moving = True
                self.player.vx = -BACKGROUND_VELOCITY * 3
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
            self.player.update(t if not self.bullet_time else t / self.rate, self.cur_scene)
            self.player_collision()
            self.missile_collision()
            if self.cur_scene == Scenes.CITY and self.player.real_y < BUILDING_HEIGHT:
                self.player.real_y = BUILDING_HEIGHT
                self.player.vy = 0
            if self.cur_scene == Scenes.SPACE and self.player.real_y < 0:
                self.player.real_y = 0
                self.player.vy = 0
            if self.player.real_y + PLAYER_HEIGHT > SCREEN_HEIGHT:
                self.player.real_y = SCREEN_HEIGHT - PLAYER_HEIGHT
                self.player.vy = 0

            self.coin_manager.update(t)
            self.arrow.update()
            self.distance_manager.update(t)
            self.coin_gui.update(t)
            self.hp_manager.update(t)

            if self.player.hp <= 0:
                self.trigger_lose()

            if self.earthquake:
                self.earthquake_time -= t
                if self.earthquake_time <= 0:
                    self.earthquake = False
                    self.screen_shake_manager.shaking = False
                    self.spaceship.earthquake = False
                else:
                    self.spaceship.earthquake = True
                    self.laser_manager.kill()
                    for obj in self.player_collision_group:
                        if type(obj) not in (PoliceCar, Bomber, Spaceship, UFO, Coin):
                            obj.kill()

        # objects in scene.CITY:
        if self.cur_scene == Scenes.CITY and not self.lose:
            self.laser_manager.update(t)
            self.roads.update(t)
            self.buildings.update(t)
            self.policecar.update(t)
            if (
                self.distance_manager.dist_to_next_country > 0
                and self.distance_manager.dist_to_next_country > 50
            ):
                self.bomber.random_activate(self.difficulty)
            self.bomber.aim(self.player.rect.centerx, self.player.rect.centery)
            self.bomber.update(t, self.difficulty)
            self.obstacle_manager.update(t)

        # objects in scene.SPACE:
        if self.cur_scene == Scenes.SPACE and not self.lose:
            if self.distance_manager.dist_to_next_country > 30:
                if not self.spaceship.activated and not self.space_temp_deactivated_enemies:
                    self.ufo.random_activate(self.difficulty)
                if not self.ufo.activated and not self.space_temp_deactivated_enemies:
                    self.spaceship.random_activate(self.difficulty)

                if (
                    self.distance_manager.dist_to_next_country > 30 and self.spaceship.activated
                    and self.spaceship.x == 1000 and not self.spaceship.is_charge
                    and not self.spaceship.is_shoot and self.spaceship.activated_dur >= 10.0
                    and random.randint(0, 1000) <= self.difficulty
                ):
                    self.spaceship.is_charge = True

                self.comets.add(self.difficulty)

            self.spaceship.update(t, self.difficulty)
            self.ufo.update(t, self.difficulty)
            self.comets.update(t, self.difficulty)
            if self.space_temp_deactivated_enemies:
                self.space_temp_deactivated_enemies_t -= t
                if self.space_temp_deactivated_enemies_t <= 0:
                    self.space_temp_deactivated_enemies = False

        # gui
        self.game_screen.update(t)
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
        if self.lose:
            window.blit(assets_manager.images['darken'], pygame.Rect(0, 0, 0, 0))
            window.blit(assets_manager.images['GameOver'], pygame.Rect(0, 0, 0, 0))
            self.lose_screen.draw_ui(window)
            score_image = font.render(f'Score: {self.score} (Highest: {self.highscore})', True, (255, 255, 255))
            score_rect = score_image.get_rect()
            score_rect.center = (SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 - 10)
            window.blit(score_image, score_rect)
            round_image = font.render(
                f'Rounds survived: {self.round_counter.rounds_survived}', True, (255, 255, 255)
            )
            round_rect = score_rect.move(0, 50)
            window.blit(round_image, round_rect)

        else:
            self.game_screen.draw_ui(window)
        self.distance_manager.draw(window)
        self.round_counter.draw(window)
        self.coin_gui.draw(window)
        self.hp_manager.draw(window)
        self.inventory.draw(window)

        if self.dimming:
            darken_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken_image.fill((0, 0, 0))
            darken_image.set_alpha(self.darken_alpha)
            window.blit(darken_image, pygame.Rect(0, 0, 0, 0))
            self.darken_alpha = min(self.darken_alpha + 4, 255)
            if self.darken_alpha == 255:
                self.stage2 = True

        self.screen_shake_manager.shake(window)

    def trigger_lose(self) -> None:
        if not self.lose and not PLAYER_INVIN:
            assets_manager.play_music("ensolarado")
            if assets_manager.play_quotes:
                assets_manager.play_sound("die")
            self.lose = True

    def player_collision(self) -> None:
        for obj in self.player_collision_group:
            if (
                self.distance_manager.dist_to_next_country == 0
                and type(obj) not in (Coin, Obstacle)
            ):
                continue
            if self.cur_scene == Scenes.SPACE and type(obj) in (Spaceship, Comet):
                obj.collision_player(self.player)
            if self.player.rect.colliderect(obj.rect):
                if type(obj) in (Bullet, MissileAircraft):
                    obj.player_hit(self.player)
                elif type(obj) == Coin:
                    obj.player_hit(self.player)
                elif self.cur_scene == Scenes.CITY:
                    if type(obj) == PoliceCar:
                        self.trigger_lose()
                    elif type(obj) == Obstacle:
                        self.player.resolve_collision(obj)

    def missile_collision(self) -> None:
        for obj in self.missile_collision_group:
            for missile in self.player.missiles:
                if missile.rect.colliderect(obj.rect):
                    obj.missile_hit(missile)

    def kill_bullets(self):
        for obj in self.player_collision_group:
            if type(obj) in (Bullet, MissileAircraft, Comet):
                obj.kill()

    def start_earthquake(self) -> None:
        self.screen_shake_manager.shaking = True
        self.earthquake = True
        self.earthquake_time = ITEM_EARTHQUAKE_DURATION

    def add_coin_score(self):
        self.coins += 1
        self.score += int(np.log2(2 * self.difficulty)) * COIN_SCORE_MULT
        self.highscore = max(self.highscore, self.score)

    def add_dist_score(self, dist):
        self.score += int(np.log2(2 * self.difficulty)) * DIST_SCORE_MULT * dist
        self.highscore = max(self.highscore, self.score)

    def add_scene_score(self):
        self.score += int(np.log2(2 * self.difficulty)) * SCENE_SCORE_MULT
        self.highscore = max(self.highscore, self.score)

    def run(self, window) -> int:
        previous_pause = False
        while True:
            ret = self.event_process(window)
            t = self.clock.get_time()
            if previous_pause:
                self.update(0.001, window)
                previous_pause = False
            else:
                self.update(t / 1000, window)
            if ret:  # pressed return
                return self.highscore
            if ret is not None:  # pressed resume
                previous_pause = True
            self.draw(window)
            pygame.display.flip()
            self.clock.tick(60)

            if SHOW_FPS:
                print(f'fps = {0 if t == 0 else 1000 / t}')
