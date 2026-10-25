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
menu_bg = pygame.image.load("pictures/game_menu.png")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

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
        back_text = font.render(
            "Press ESC to return",
            True,
            (255, 255, 255)
        )
        screen.blit(
            back_text,
            (100, 30)
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

def phone_complete_screen():
    view_phonee.play(-1)
    picture = pygame.image.load("pictures/phone_complete.png").convert_alpha()
    picture = pygame.transform.smoothscale(picture, (WIDTH, HEIGHT))

    big_font = pygame.font.Font(None, 60)
    font = pygame.font.Font(None, 40)
    stage = "picture"   # first the picture, then the options

    while True:
        screen.blit(picture, (0, 0))

        if stage == "picture":
            hint = font.render("Press ENTER to continue", True, (255, 255, 255))
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 30)))
        else:
            # dim the picture a little so the options are easy to read
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            title = big_font.render("Phone Complete!", True, (255, 210, 31))
            opt1 = font.render("1. Keep Playing", True, (255, 255, 255))
            opt2 = font.render("2. Exit Game", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90)))
            screen.blit(opt1, opt1.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            screen.blit(opt2, opt2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 55)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if stage == "picture":
                    if event.key == pygame.K_RETURN:
                        click.play()
                        stage = "options"
                else:
                    if event.key == pygame.K_1:
                        click.play()
                        view_phonee.stop()
                        return                      # back to the game menu, nothing reset
                    elif event.key == pygame.K_2:
                        save_game(game_data)
                        pygame.quit()
                        sys.exit()

def adventure_menu():
    game_menu.play(-1)

    GOLD = (255, 210, 31)
    coin_font = pygame.font.Font(None, 46)

    while True:
        screen.blit(menu_bg, (0, 0))

        # ---------- COINS (top-left) ----------
        coin_text = coin_font.render(str(game_data["coins"]), True, (255, 255, 255))
        pill_w = 95 + coin_text.get_width() + 25
        pill = pygame.Surface((pill_w, 60), pygame.SRCALPHA)
        pygame.draw.rect(pill, (15, 20, 35, 190), pill.get_rect(), border_radius=30)
        screen.blit(pill, (30, 25))
        pygame.draw.rect(screen, GOLD, (30, 25, pill_w, 60), 2, border_radius=30)
        pygame.draw.circle(screen, GOLD, (70, 55), 20)
        pygame.draw.circle(screen, (180, 130, 20), (70, 55), 20, 3)
        pygame.draw.circle(screen, (180, 130, 20), (70, 55), 10, 2)
        screen.blit(coin_text, coin_text.get_rect(midleft=(103, 55)))

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
                    parts_before = game_data["parts_bought"]
                    shop(screen, game_data)
                    save_game(game_data)
                    if parts_before < 12 and game_data["parts_bought"] == 12:
                        phone_complete_screen()
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