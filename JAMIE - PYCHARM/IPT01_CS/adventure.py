import pygame
import sys

from world1 import world1
from world2 import world2
from world3 import world3


def adventure(screen, game_data):

    world_image = pygame.image.load("pictures/world_selection.png")
    world_image = pygame.transform.scale(world_image, (1510, 890))

    running = True

    while running:

        screen.blit(world_image, (0, 0))

        font = pygame.font.Font(None, 35)

        text = font.render(
            "Press 1, 2, or 3 to choose a world",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (400, 650))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    world1(screen, game_data)

                elif event.key == pygame.K_2:
                    world2(screen, game_data)

                elif event.key == pygame.K_3:
                    world3(screen, game_data)

                elif event.key == pygame.K_ESCAPE:
                    running = False