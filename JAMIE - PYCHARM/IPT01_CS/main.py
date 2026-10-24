import pygame
import sys
import atexit

from adventure import adventure
from shop import shop
from save_system import load_game, save_game
import character

pygame.init()
pygame.mixer.init()


WIDTH = 1510
HEIGHT = 870

# True  = pick girl/boy every time the game starts
# False = pick only the first time (the choice is saved)
ASK_EVERY_LAUNCH = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Foes & Goals")

game_data = {
    "coins": 500,
    "parts_bought": 0,
    "character": None,

    "world1_unlocked": 1,
    "world2_unlocked": 1,
    "world3_unlocked": 1
}
load_game(game_data)
character.init(game_data, save_game)

# Save automatically whenever the game closes (X button, Exit Game, etc.)
atexit.register(lambda: save_game(game_data))

#MUSIC
click = pygame.mixer.Sound("music/click.mp3")
lp_music = pygame.mixer.Sound("music/LP_music.mp3")
game_menu = pygame.mixer.Sound("music/game_menu.mp3")
view_phonee = pygame.mixer.Sound("music/view_phone.mp3")

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
    view_phonee.play(-1)
    WIDTH = 15102
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
                    view_phonee.stop()
                    click.play()
                    running = False


def adventure_menu():
    game_menu.play(-1)
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
            "4. Character",
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
                    game_menu.stop()
                    adventure(screen, game_data)
                    save_game(game_data)
                    game_menu.play(-1)  # music back after Adventure
                elif event.key == pygame.K_2:
                    click.play()
                    game_menu.stop()
                    shop(screen, game_data)
                    save_game(game_data)
                    game_menu.play(-1)  # music back after Shop
                elif event.key == pygame.K_3:
                    game_menu.stop()
                    view_phone(screen, game_data)
                    game_menu.play(-1)  # music back after View Phone
                elif event.key == pygame.K_4:
                    click.play()
                    game_menu.stop()
                    character.character_menu(screen, game_data)
                    game_menu.play(-1)  # music back after Character
                elif event.key == pygame.K_5:
                    click.play()
                    game_menu.stop()
                    save_game(game_data)
                    pygame.quit()
                    sys.exit()


opening_screen()
second_screen()
if ASK_EVERY_LAUNCH or game_data.get("character") is None:
    character.choose_first_character(screen, game_data)
adventure_menu()