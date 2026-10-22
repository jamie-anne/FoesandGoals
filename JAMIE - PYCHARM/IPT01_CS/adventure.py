import pygame
import sys

from world1 import world1
from world2 import world2
from world3 import world3
pygame.mixer.init()
click = pygame.mixer.Sound("music/click.mp3")

def adventure(screen, game_data):
    world_image = pygame.image.load("pictures/world_selection.jpg")
    world_image = pygame.transform.scale(world_image, (1510, 890))
    running = True
    while running:

        screen.blit(world_image, (0, 0))

        pygame.display.update()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    click.play()
                    world1(screen, game_data)
                elif event.key == pygame.K_2:
                    click.play()
                    world2(screen, game_data)
                elif event.key == pygame.K_3:
                    click.play()
                    world3(screen, game_data)
                elif event.key == pygame.K_ESCAPE:
                    click.play()
                    running = False