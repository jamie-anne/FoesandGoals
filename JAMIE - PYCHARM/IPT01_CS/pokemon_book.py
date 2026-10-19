import pygame
import sys
import json
import os
pygame.mixer.init()

WIDTH = 1510
HEIGHT = 890

SAVE_FILE = "savegame.json"
PER_PAGE = 10

click = pygame.mixer.Sound("music/click.mp3")
def save_game(game_data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(game_data, f)
    except OSError as error:
        print("Could not save:", error)

def load_game(game_data):
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE) as f:
                game_data.update(json.load(f))
        except (OSError, ValueError) as error:
            print("Could not load save:", error)

# RECORD A DEFEAT
def record_defeat(game_data, name, world, level):
    book = game_data.setdefault("pokemon_book", {})

    if name not in book:
        book[name] = {"defeated": 0, "world": world, "level": level}

    book[name]["defeated"] += 1
    save_game(game_data)

# POKEMON BOOK SCREEN
def pokemon_book(screen, game_data):
    book = game_data.get("pokemon_book", {})
    names = list(book.keys())          # order = first time defeated
    page = 0
    total_pages = max(1, (len(names) + PER_PAGE - 1) // PER_PAGE)

    title_font = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 38)
    small = pygame.font.Font(None, 30)

    while True:
        screen.fill((25, 25, 40))

        title = title_font.render("POKEMON BOOK", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))
        count = small.render(f"Defeated: {len(names)} different Pokemon",
                             True, (255, 215, 0))
        screen.blit(count, count.get_rect(center=(WIDTH // 2, 135)))

        if not names:
            empty = font.render("No Pokemon defeated yet.", True, (200, 200, 200))
            screen.blit(empty, empty.get_rect(center=(WIDTH // 2, 400)))

        start = page * PER_PAGE
        for i, name in enumerate(names[start:start + PER_PAGE]):
            info = book[name]
            col, row = i % 2, i // 2
            x = 200 + col * 650
            y = 200 + row * 110

            pygame.draw.rect(screen, (50, 50, 75), (x, y, 600, 90), border_radius=12)
            screen.blit(font.render(f"{start + i + 1}. {name}", True,
                                    (255, 255, 255)), (x + 20, y + 12))
            screen.blit(small.render(
                f"World {info['world']} - Level {info['level']}   "
                f"Defeated: {info['defeated']}x", True, (180, 180, 220)),
                (x + 20, y + 52))

        footer = small.render(
            f"Page {page + 1}/{total_pages}    LEFT/RIGHT = Change page    ESC = Back",
            True, (200, 200, 200))
        screen.blit(footer, footer.get_rect(center=(WIDTH // 2, HEIGHT - 45)))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    click.play()
                    return
                elif event.key == pygame.K_RIGHT and page < total_pages - 1:
                    page += 1
                elif event.key == pygame.K_LEFT and page > 0:
                    page -= 1