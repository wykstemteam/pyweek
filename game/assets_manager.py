import os

import pygame

from game.constants import *


class AssetsManager:
    def __init__(self) -> None:
        pygame.mixer.init()
        self.sound_volume = INIT_SOUND_VOLUME
        self.music_volume = INIT_MUSIC_VOLUME
        self.play_quotes = False

        self.images = {}
        self.animations = {}
        self.sounds = {}

        self.init_images()
        self.scale_images()
        self.init_animations()
        self.scale_animations()
        self.init_sounds()

    def init_images(self) -> None:
        for fn in os.listdir(os.path.join('assets', 'images')):
            if not os.path.isfile(os.path.join('assets', 'images', fn)):
                continue

            base_fn = os.path.splitext(fn)[0]
            self.images[base_fn] = pygame.image.load(os.path.join('assets', 'images', fn))

    def scale_images(self) -> None:
        # background
        self.images['road'] = pygame.transform.scale(
            self.images['road'], (SCREEN_WIDTH, SCREEN_HEIGHT - BUILDING_HEIGHT)
        )
        self.images['3buildings'] = pygame.transform.scale(
            self.images['3buildings'], (BUILDING_WIDTH, BUILDING_HEIGHT)
        )
        self.images['beach_full'] = pygame.transform.scale(
            self.images['beach_full'], (SCREEN_WIDTH * 2, BUILDING_HEIGHT)
        )
        self.images['gradient_line'] = pygame.transform.scale(
            self.images['gradient_line'], (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # gui
        self.images['GameOver'] = pygame.transform.scale(
            self.images['GameOver'], (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.images['arrow'] = pygame.transform.scale(self.images['arrow'], (80, 100))
        for i in range(5):
            self.images[f'HP{i}'] = pygame.transform.scale(self.images[f'HP{i}'], (400, 100))
        for i in range(5):
            self.images[f'HP{i}_shop'] = pygame.transform.scale(self.images[f'HP{i}'], (240, 60))

        # enemy
        self.images['bullet'] = pygame.transform.scale(
            self.images['bullet'], (BULLET_WIDTH, BULLET_HEIGHT)
        )
        self.images['bomber_bullet'] = pygame.transform.scale(
            self.images['bomber_bullet'], (BOMBER_BULLET_WIDTH, BOMBER_BULLET_HEIGHT)
        )
        self.images['policecar'] = pygame.transform.scale(
            self.images['policecar'], (POLICECAR_WIDTH, POLICECAR_HEIGHT)
        )
        self.images['missile'] = pygame.transform.scale(
            self.images['missile'], (MISSILE_WIDTH, MISSILE_HEIGHT)
        )
        self.images['missile_for_aircraft'] = pygame.transform.scale(
            self.images['missile_for_aircraft'], (MISSILE_AIRCRAFT_WIDTH, LASER_HEIGHT)
        )
        self.images['space_ship'] = pygame.transform.scale(
            self.images['space_ship'], (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        )
        self.images['lc_charge_none'] = pygame.transform.scale(
            self.images['lc_charge_none'], (200, 200)
        )
        self.images['ls_shoot_none'] = pygame.transform.scale(
            self.images['ls_shoot_none'], (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.images['spaceship_bullet'] = pygame.transform.scale(
            self.images['spaceship_bullet'], (SPACESHIP_BULLET_WIDTH, SPACESHIP_BULLET_HEIGHT)
        )
        self.images['UFO'] = pygame.transform.scale(self.images['UFO'], (450, 450))
        self.images['UFO_bullet'] = pygame.transform.scale(
            self.images['UFO_bullet'], (UFO_BULLET_WIDTH, UFO_BULLET_HEIGHT)
        )
        self.images['comet'] = pygame.transform.scale(self.images['comet'], (200, 60))

        for i in range(1, 4):
            self.images[f'obstacle{i}'] = pygame.transform.scale(
                self.images[f'obstacle{i}'], (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            )
        self.images['motorbike'] = pygame.transform.scale(
            self.images['motorbike'], (PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        for i in range(1, 4):
            self.images[f'shield{i}'] = pygame.transform.scale(
                self.images[f'shield{i}'],
                (PLAYER_WIDTH + SHIELD_WIDTH_OFFSET, PLAYER_HEIGHT + SHIELD_HEIGHT_OFFSET)
            )
        for item_name in (
            'item_blank', 'item_healpotion', 'item_shield', 'item_star', 'item_clock',
            'item_missile', 'item_earthquake'
        ):
            self.images[f'{item_name}_inventory'] = pygame.transform.scale(
                self.images[item_name], (ITEM_WIDTH, ITEM_HEIGHT)
            )
        for item_name in (
            'item_blank', 'item_healpotion', 'item_shield', 'item_star', 'item_clock',
            'item_missile', 'item_earthquake'
        ):
            self.images[f'{item_name}_shop'] = pygame.transform.scale(
                self.images[item_name], (ITEM_WIDTH_SHOP, ITEM_HEIGHT_SHOP)
            )

    def init_animations(self) -> None:
        for dirname in os.listdir(os.path.join('assets', 'animations')):
            self.animations[dirname] = []
            files = os.listdir(os.path.join('assets', 'animations', dirname))
            files.sort(key=lambda fn: int(os.path.splitext(fn)[0]))
            for fn in files:
                self.animations[dirname].append(
                    pygame.image.load(os.path.join('assets', 'animations', dirname, fn))
                )

    def scale_animations(self) -> None:
        for i in range(len(self.animations['explode'])):
            self.animations['explode'][i] = pygame.transform.scale(
                self.animations['explode'][i], (EXPLODE_WIDTH, EXPLODE_HEIGHT)
            )
        for i in range(len(self.animations['bomber'])):
            self.animations['bomber'][i] = pygame.transform.scale(
                self.animations['bomber'][i], (BOMBER_WIDTH, BOMBER_HEIGHT)
            )
        for i in range(len(self.animations['laser_charge'])):
            self.animations['laser_charge'][i] = pygame.transform.scale(
                self.animations['laser_charge'][i], (200, 200)
            )
        for i in range(len(self.animations['laser_shoot'])):
            self.animations['laser_shoot'][i] = pygame.transform.scale(
                self.animations['laser_shoot'][i], (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        for i in range(len(self.animations['coin'])):
            self.animations['coin'][i] = pygame.transform.scale(
                self.animations['coin'][i], (COIN_WIDTH, COIN_HEIGHT)
            )

    def init_sounds(self) -> None:
        for fn in os.listdir(os.path.join('assets', 'sounds')):
            base_fn = os.path.splitext(fn)[0]
            self.sounds[base_fn] = pygame.mixer.Sound(os.path.join('assets', 'sounds', fn))

    def play_sound(self, name: str) -> None:
        sound = self.sounds[name].play()
        sound.set_volume(self.sound_volume)

    def play_music(self, name: str) -> None:
        for fn in os.listdir(os.path.join('assets', 'music')):
            base_fn = os.path.splitext(fn)[0]
            if base_fn == name:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(os.path.join('assets', 'music', fn))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.music_volume)
                break
        else:
            raise ValueError(f"No music '{name}' found")

    def set_sound_volume(self, val: float) -> None:
        self.sound_volume = val

    def set_music_volume(self, val: float) -> None:
        self.music_volume = val
        pygame.mixer.music.set_volume(self.music_volume)


assets_manager = AssetsManager()
