import pygame, sys
import pygame_gui
from shop import shop_main_menu

pygame.init()

SCREEN_WIDTH, SCREEN_HIGHT = 1500, 600
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
pygame.display.set_caption("GGGG")

RED = (0, 0, 0)

FPS = 60



def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        window.fill(RED)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("Shop opened")
                    shop_main_menu(window)

        pygame.display.update()


if __name__ == "__main__":
    main()

