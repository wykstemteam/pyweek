import pygame

from game.assets_manager import assets_manager
from game.constants import *
from game.sprites import *


def run(window: pygame.Surface):
    assets_manager.play_music("boys_summer_vacation")
    running = True
    cock = pygame.time.Clock()
    buildings = BuildingManager()
    roads = pygame.sprite.Group(
        Road(assets_manager.images['road'], 0),
        Road(assets_manager.images['road'], SCREEN_WIDTH),
    )
    title_font = pygame.font.SysFont('Castellar', 30, True)
    title = title_font.render('ESCAPE FROM COPS 2021 HD DELUXE PRO MAX ULTRA REMASTERED', False, (255, 255, 0))
    instruction_font = pygame.font.SysFont('Comic Sans MS', 30)
    instruction = lambda text: instruction_font.render(text, False, (255, 255, 255))
    instructions = [
        instruction('WASD to move'),
        instruction('1 and 2 to select item in inventory'),
        instruction('Left click mouse to use item'),
        instruction('Press any key to start the escape'),
    ]
    police_car = assets_manager.images['policecar']
    bomber = assets_manager.animations['bomber'][0]
    motorbike = assets_manager.images['motorbike']

    while running:
        dt = cock.get_time() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                return

        buildings.update(dt)
        roads.update(dt)

        window.fill((0, 0, 0))
        buildings.draw(window)
        roads.draw(window)
        window.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 0))
        window.blit(police_car,
                    (50, BUILDING_HEIGHT + (SCREEN_HEIGHT - BUILDING_HEIGHT) // 2 - police_car.get_height() // 2))
        window.blit(bomber,
                    (300, BUILDING_HEIGHT + (SCREEN_HEIGHT - BUILDING_HEIGHT) // 2 - bomber.get_height() // 2))
        window.blit(motorbike,
                    (1000, BUILDING_HEIGHT + (SCREEN_HEIGHT - BUILDING_HEIGHT) // 2 - motorbike.get_height() // 2))
        for i in range(len(instructions)):
            window.blit(instructions[i],
                        (20, SCREEN_HEIGHT - 50 - instructions[i].get_height() * (len(instructions) - i - 1)))

        pygame.display.flip()
        cock.tick(60)
