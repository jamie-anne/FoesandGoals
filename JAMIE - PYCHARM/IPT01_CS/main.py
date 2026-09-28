import pygame
import sys

from adventure import adventure
from shop import shop


pygame.init()

WIDTH = 1510
HEIGHT = 890

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Foes & Goals")

# --------------------------------------------------
# GAME DATA
# --------------------------------------------------

game_data = {
    "coins": 500,
    "parts_bought": 0
}

# --------------------------------------------------
# IMAGES
# --------------------------------------------------


opening_image = pygame.image.load("pictures/foes.png")
second_image = pygame.image.load("pictures/foes.png")

opening_image = pygame.transform.scale(opening_image, (WIDTH, HEIGHT))
second_image = pygame.transform.scale(second_image, (WIDTH, HEIGHT))


# --------------------------------------------------
# OPENING SCREEN
# --------------------------------------------------

def opening_screen():

    screen.blit(opening_image, (0, 0))
    pygame.display.update()

    waiting = True

    while waiting:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    waiting = False


# --------------------------------------------------
# SECOND SCREEN
# --------------------------------------------------

def second_screen():

    screen.blit(second_image, (0, 0))
    pygame.display.update()

    waiting = True

    while waiting:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    waiting = False


# --------------------------------------------------
# VIEW PHONE
# --------------------------------------------------

def view_phone(screen, game_data):
    WIDTH = 1510
    HEIGHT = 890

    phone_images = []
    for i in range(13):
        image = pygame.image.load(
            f"phone_stage_{i}.png"
        ).convert_alpha()
        image = pygame.transform.smoothscale(
            image,
            (WIDTH, HEIGHT)
        )
        phone_images.append(image)

    font = pygame.font.Font(None, 35)
    running = True
    while running:
        current_stage = game_data["parts_bought"]
        screen.blit(
            phone_images[current_stage],
            (0, 0)
        )

        parts_text = font.render(
            f"Parts Completed: {game_data['parts_bought']}/12",
            True,
            (255, 255, 255)
        )
        screen.blit(
            parts_text,
            (30, 70)
        )

        back_text = font.render(
            "Press ESC to return",
            True,
            (255, 255, 255)
        )
        screen.blit(
            back_text,
            (1100, 30)
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def developers():
    font = pygame.font.Font(None, 60)
    running = True
    while running:
        screen.fill((0, 0, 0))
        text = font.render("DEVELOPERS", True, (255, 255, 255))
        screen.blit(text, (480, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def adventure_menu():

    font = pygame.font.Font(None, 50)

    while True:

        screen.fill((0, 0, 0))

        title = font.render("FOES & GOALS", True, (255, 255, 255))
        screen.blit(title, (500, 80))

        coins = font.render(
            f"Coins: {game_data['coins']}",
            True,
            (255, 255, 0)
        )

        screen.blit(coins, (30, 30))

        options = [
            "1. Adventure",
            "2. Shop",
            "3. View Phone",
            "4. Developers",
            "5. Exit Game"
        ]

        y = 200

        for option in options:

            text = font.render(option, True, (255, 255, 255))
            screen.blit(text, (450, y))

            y += 70

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    adventure(screen, game_data)
                elif event.key == pygame.K_2:
                    shop(screen, game_data)
                elif event.key == pygame.K_3:
                    view_phone(screen, game_data)
                elif event.key == pygame.K_4:
                    developers()
                elif event.key == pygame.K_5:
                    pygame.quit()
                    sys.exit()


# --------------------------------------------------
# START GAME
# --------------------------------------------------

opening_screen()
second_screen()
adventure_menu()