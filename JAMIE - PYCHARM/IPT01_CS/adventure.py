import pygame
import sys

from world1 import world1
from world2 import world2
from world3 import world3
from save_system import save_game

pygame.mixer.init()
click = pygame.mixer.Sound("music/click.mp3")
world_bg = pygame.mixer.Sound("music/world_level.mp3")

WIDTH = 1510
HEIGHT = 890

# =========================================================
# SETTINGS (easy things to change)
# =========================================================
# Center (x, y) of the "[ LOCKED ]" text for each world.
# Put it just below that world's name/location label on world_selection.jpg.
LOCKED_LABEL_POSITIONS = {
    1: (251, 520),
    2: (755, 520),
    3: (1259, 520),
}
LOCKED_COLOR = (0,0,0)
LOCKED_SIZE = 40
SHOW_ALL_LABELS = False   # True = show [ LOCKED ] under every world so you can line them up

WORLD_FUNCTIONS = {1: world1, 2: world2, 3: world3}
WORLD_KEYS = {
    pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
    pygame.K_KP1: 1, pygame.K_KP2: 2, pygame.K_KP3: 3,
}


def is_world_unlocked(game_data, world):
    """World 1 is always open. World N opens when all 5 levels of world N-1 are cleared."""
    if world == 1:
        return True
    cleared = game_data.get(f"world{world - 1}_cleared", [])
    return all(level in cleared for level in range(1, 6))


def adventure(screen, game_data):

    world_image = pygame.image.load("pictures/world_selection.jpg")
    world_image = pygame.transform.scale(world_image, (WIDTH, HEIGHT))

    label_font = pygame.font.Font(None, LOCKED_SIZE)
    label_font.set_bold(True)
    clock = pygame.time.Clock()

    running = True
    while running:

        screen.blit(world_image, (0, 0))

        # "[ LOCKED ]" under each locked world
        for world, (x, y) in LOCKED_LABEL_POSITIONS.items():
            if SHOW_ALL_LABELS or not is_world_unlocked(game_data, world):
                label = label_font.render("[ LOCKED ]", True, LOCKED_COLOR)
                screen.blit(label, label.get_rect(center=(x, y)))

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in WORLD_KEYS:
                    world = WORLD_KEYS[event.key]
                    if is_world_unlocked(game_data, world):
                        click.play()
                        WORLD_FUNCTIONS[world](screen, game_data)
                        save_game(game_data)
                elif event.key == pygame.K_ESCAPE:
                    click.play()
                    running = False