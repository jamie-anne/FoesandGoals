import pygame
import sys


from adventure import adventure
from shop import shop
from pokemon_book import pokemon_book, load_game, save_game

pygame.init()
pygame.mixer.init()


WIDTH = 1510
HEIGHT = 890

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Foes & Goals")

game_data = {
    "coins": 500,
    "parts_bought": 0,

    "world1_unlocked": 1,
    "world2_unlocked": 1,
    "world3_unlocked": 1
}
load_game(game_data)

#MUSIC
click = pygame.mixer.Sound("music/click.mp3")
lp_music = pygame.mixer.Sound("music/LP_music.mp3")


opening_image = pygame.image.load("pictures/foes.png")
second_image = pygame.image.load("pictures/foes.png")

opening_image = pygame.transform.scale(opening_image, (WIDTH, HEIGHT))
second_image = pygame.transform.scale(second_image, (WIDTH, HEIGHT))


def opening_screen():
    screen.blit(opening_image, (0, 0))
    pygame.display.update()

    lp_music.play(-1)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lp_music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    lp_music.stop()
                    waiting = False

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

def view_phone(screen, game_data):
    WIDTH = 1510
    HEIGHT = 890
    phone_images = []
    for i in range(13):
        image = pygame.image.load(
            f"pictures/phone_stage_{i}.png"
        ).convert_alpha()
        image = pygame.transform.smoothscale(
            image,
            (WIDTH, HEIGHT)
        )
        phone_images.append(image)
    click.play()
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
                    click.play()
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
            "4. Pokemon Book",
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
                    click.play()
                    adventure(screen, game_data)
                elif event.key == pygame.K_2:
                    click.play()
                    shop(screen, game_data)
                elif event.key == pygame.K_3:
                    view_phone(screen, game_data)
                elif event.key == pygame.K_4:
                    click.play()
                    pokemon_book(screen, game_data)
                elif event.key == pygame.K_5:
                    click.play()
                    save_game(game_data)
                    pygame.quit()
                    sys.exit()
opening_screen()
second_screen()
adventure_menu()