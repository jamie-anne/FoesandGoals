import pygame
import sys

pygame.mixer.init()

WIDTH = 1510
HEIGHT = 890

# =========================================================
# SETTINGS (easy things to change)
# =========================================================
# Order matters: 1 = Girl, 2 = Boy, 3 = Girl (outfit 2), 4 = Boy (outfit 2)
CHARACTER_FILES = [
    "pictures/character_1.png", #girl
    "pictures/character_2.png",
    "pictures/character_3.png", #girl2
    "pictures/character_4.png",
]
CHARACTER_NAMES = ["Jamie", "Railey", "Shermie", "Justin"]

# Where / how big the player is drawn during a match
MATCH_POSITION = (100, 270)     # top-left of the area (just above "PLAYER")
MATCH_SIZE = (330, 330)         # the character is scaled to fit inside this

BACKGROUND_FILE = "pictures/shop_bg.jpg"   # optional, falls back to a color
BACKGROUND_COLOR = (25, 30, 45)
CARD_COLOR = (32, 40, 59)
TEXT_COLOR = (255, 255, 255)
GOLD = (220, 168, 50)
BORDER_COLOR = (104, 115, 134)
SELECTED_COLOR = (255, 210, 31)

click = pygame.mixer.Sound("music/click.mp3")

# =========================================================
# SHARED STATE
# game_data["character"] is None (not chosen yet) or 0-3
# =========================================================
_game_data = None
_save = None
_cache = {}


def init(game_data, save_function=None):
    """Call once in main.py, right after load_game(game_data).
    save_function (optional) is your save_game; it is called whenever the
    player picks a character."""
    global _game_data, _save
    _game_data = game_data
    _save = save_function
    game_data.setdefault("character", None)


def get_character():
    if _game_data is None:
        return None
    return _game_data.get("character")


def set_character(game_data, index):
    game_data["character"] = index
    if _save is not None:
        _save(game_data)


# =========================================================
# IMAGES
# =========================================================
def _placeholder(index):
    """Shown only if the picture file is missing."""
    surface = pygame.Surface((400, 500), pygame.SRCALPHA)
    pygame.draw.rect(surface, (225, 170, 240),
                     surface.get_rect(), border_radius=30)
    label = pygame.font.Font(None, 60).render(
        CHARACTER_NAMES[index], True, (0, 0, 0))
    surface.blit(label, label.get_rect(center=surface.get_rect().center))
    return surface


def _load_original(index):
    key = ("original", index)
    if key not in _cache:
        try:
            _cache[key] = pygame.image.load(
                CHARACTER_FILES[index]).convert_alpha()
        except (pygame.error, OSError):
            print(f"Could not load image: {CHARACTER_FILES[index]}")
            _cache[key] = _placeholder(index)
    return _cache[key]


def get_image(index, box):
    """Character image scaled to fit inside box = (w, h), keeping its shape."""
    key = (index, box)
    if key not in _cache:
        original = _load_original(index)
        w, h = original.get_size()
        scale = min(box[0] / w, box[1] / h)
        size = (max(1, int(w * scale)), max(1, int(h * scale)))
        _cache[key] = pygame.transform.smoothscale(original, size)
    return _cache[key]


def _load_background():
    try:
        image = pygame.image.load(BACKGROUND_FILE).convert()
        return pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
    except (pygame.error, OSError):
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill(BACKGROUND_COLOR)
        return surface


# =========================================================
# USE THIS INSIDE world1 / world2 / world3 MATCH SCREENS
# =========================================================
def draw_player_character(screen, position=MATCH_POSITION, size=MATCH_SIZE):
    index = get_character()
    if index is None:
        return
    image = get_image(index, size)
    rect = image.get_rect(
        midbottom=(position[0] + size[0] // 2, position[1] + size[1])
    )
    screen.blit(image, rect)


# =========================================================
# DRAWING HELPERS
# =========================================================
def _draw_card(screen, rect, index, font, border_color, border_width, tag=""):
    pygame.draw.rect(screen, CARD_COLOR, rect, border_radius=12)

    # top 40px is kept free for the "SELECTED" tag, bottom 60px for the name
    image_area_h = rect.h - 100
    image = get_image(index, (rect.w - 40, image_area_h))
    screen.blit(image, image.get_rect(
        center=(rect.centerx, rect.y + 40 + image_area_h // 2)))

    label = font.render(f"{CHARACTER_NAMES[index]}",
                        True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=(rect.centerx, rect.bottom - 30)))

    if tag:
        tag_surface = font.render(tag, True, border_color)
        screen.blit(tag_surface, (rect.right - tag_surface.get_width() - 15,
                                  rect.y + 12))

    pygame.draw.rect(screen, border_color, rect, border_width,
                     border_radius=12)


def _draw_input(screen, font, prompt, input_text, message, y=820):
    label = font.render(prompt, True, TEXT_COLOR)
    screen.blit(label, (70, y))
    box = pygame.Rect(70 + label.get_width() + 20, y - 10, 60, 40)
    pygame.draw.rect(screen, TEXT_COLOR, box, 2)
    screen.blit(font.render(input_text, True, TEXT_COLOR), (box.x + 22, y))
    screen.blit(font.render(message, True, TEXT_COLOR), (box.right + 25, y))


# =========================================================
# FIRST PICK  (after the landing page + animation)
# Only 2 options: 1 = Girl, 2 = Boy
# =========================================================
def choose_first_character(screen, game_data):
    background = _load_background()
    title_font = pygame.font.Font(None, 70)
    info_font = pygame.font.Font(None, 30)
    card_font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    card_w, card_h, gap = 400, 520, 80
    start_x = (WIDTH - (2 * card_w + gap)) // 2
    rects = [pygame.Rect(start_x + i * (card_w + gap), 170, card_w, card_h)
             for i in range(2)]

    input_text = ""
    message = ""

    while True:
        screen.blit(background, (0, 0))

        title = title_font.render("CHOOSE YOUR CHARACTER", True, TEXT_COLOR)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 90)))

        for i, rect in enumerate(rects):
            typed = input_text == str(i + 1)
            _draw_card(screen, rect, i, card_font,
                       TEXT_COLOR if typed else BORDER_COLOR,
                       4 if typed else 2)

        _draw_input(screen, info_font,
                    "Type 1 or 2, then press ENTER:", input_text, message)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_BACKSPACE:
                input_text = ""

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if input_text in ("1", "2"):
                    click.play()
                    set_character(game_data, int(input_text) - 1)
                    return
                message = "Please type 1 or 2."
                input_text = ""

            elif len(event.unicode) == 1 and event.unicode in "0123456789":
                input_text = event.unicode
                message = ""


# =========================================================
# CHARACTER MENU  (all 4 characters)
# Left: 2 x 2 grid.  Right: the chosen character.
# Type a number + ENTER to switch.  ESC = back.
# =========================================================
def character_menu(screen, game_data):
    background = _load_background()
    title_font = pygame.font.Font(None, 55)
    info_font = pygame.font.Font(None, 30)
    card_font = pygame.font.Font(None, 32)
    panel_font = pygame.font.Font(None, 45)
    clock = pygame.time.Clock()

    card_w, card_h, gap = 330, 300, 30
    grid_x, grid_y = 70, 110
    rects = [
        pygame.Rect(grid_x + (i % 2) * (card_w + gap),
                    grid_y + (i // 2) * (card_h + gap),
                    card_w, card_h)
        for i in range(4)
    ]
    panel = pygame.Rect(820, 110, 620, 630)

    input_text = ""
    message = ""

    while True:
        chosen = game_data.get("character")
        screen.blit(background, (0, 0))

        # TOP BAR
        screen.blit(info_font.render("ESC = Back", True, (200, 200, 200)),
                    (70, 28))
        title = title_font.render("CHARACTERS", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 18))

        # LEFT: 2 x 2 GRID
        for i, rect in enumerate(rects):
            if i == chosen:
                _draw_card(screen, rect, i, card_font, SELECTED_COLOR, 4,
                           "SELECTED")
            elif input_text == str(i + 1):
                _draw_card(screen, rect, i, card_font, TEXT_COLOR, 4)
            else:
                _draw_card(screen, rect, i, card_font, BORDER_COLOR, 2)

        # RIGHT: CHOSEN CHARACTER
        pygame.draw.rect(screen, CARD_COLOR, panel, border_radius=12)
        pygame.draw.rect(screen, GOLD, panel, 3, border_radius=12)
        header = panel_font.render("YOUR CHARACTER", True, GOLD)
        screen.blit(header, header.get_rect(center=(panel.centerx,
                                                    panel.y + 35)))
        if chosen is not None:
            image_area_h = panel.h - 150
            image = get_image(chosen, (panel.w - 80, image_area_h))
            screen.blit(image, image.get_rect(
                center=(panel.centerx, panel.y + 65 + image_area_h // 2)))
            name = panel_font.render(CHARACTER_NAMES[chosen], True,
                                     TEXT_COLOR)
            screen.blit(name, name.get_rect(center=(panel.centerx,
                                                    panel.bottom - 40)))

        # INPUT AREA
        _draw_input(screen, info_font,
                    "Enter the number of the character (1-4):",
                    input_text, message)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                click.play()
                return

            elif event.key == pygame.K_BACKSPACE:
                input_text = ""

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if input_text in ("1", "2", "3", "4"):
                    click.play()
                    index = int(input_text) - 1
                    set_character(game_data, index)
                    message = f"{CHARACTER_NAMES[index]} selected!"
                else:
                    message = "Enter a number from 1 to 4."
                input_text = ""

            elif len(event.unicode) == 1 and event.unicode in "0123456789":
                input_text = event.unicode
                message = ""