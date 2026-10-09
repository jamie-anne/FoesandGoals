import pygame
import sys

WIDTH = 1510
HEIGHT = 890

# =========================================================
# ADJUST THESE
# =========================================================

PICTURE_FOLDER = "pictures"
PICTURE_NAME = "{world}_lvl{level}.png"   # -> pictures/1_lvl1.png, 2_lvl3.png, ...

IMAGE_SIZE = (300, 200)    # (width, height) of each level picture
H_SPACING = 250            # horizontal distance between neighboring level centers
ROW_GAP = 317              # vertical distance between the top row and bottom row
TOP_ROW_Y = 275            # center Y of the top row (lvl2, lvl4)

LABEL_GAP = 28             # distance between a picture and its [ LOCKED ] text
LABEL_SIZE = 34            # font size of [ LOCKED ] / [ UNLOCKED ]

DIM_LOCKED = True          # darken the pictures of locked levels

LOCKED_COLOR = (220, 60, 60)
UNLOCKED_COLOR = (60, 220, 90)


# =========================================================
# HELPERS
# =========================================================

def load_image(filename, size=None):
    try:
        image = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(image, size) if size else image
    except (pygame.error, FileNotFoundError):
        print(f"Could not load image: {filename}")
        return None


def draw_text(screen, text, size, x, y, color=(255, 255, 255), center=False):
    surface = pygame.font.Font(None, size).render(str(text), True, color)
    screen.blit(surface, surface.get_rect(center=(x, y)) if center else (x, y))


def get_level_center(level):
    """Zigzag layout: lvl1, lvl3, lvl5 on the bottom row; lvl2, lvl4 on top."""
    center_x = WIDTH // 2 + (level - 3) * H_SPACING

    if level % 2 == 0:
        center_y = TOP_ROW_Y
    else:
        center_y = TOP_ROW_Y + ROW_GAP

    return center_x, center_y


def make_placeholder(level):
    """Shown only if the picture file is missing."""
    surface = pygame.Surface(IMAGE_SIZE, pygame.SRCALPHA)
    pygame.draw.rect(surface, (225, 170, 240),
                     surface.get_rect(), border_radius=20)
    draw_text(surface, f"lvl{level}", 60,
              IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2, (0, 0, 0), True)
    return surface


def load_level_images(world_number):
    normal = {}
    dimmed = {}

    for level in range(1, 6):
        path = f"{PICTURE_FOLDER}/" + PICTURE_NAME.format(
            world=world_number, level=level
        )

        image = load_image(path, IMAGE_SIZE)

        if image is None:
            image = make_placeholder(level)

        dark = image.copy()
        dark.fill((110, 110, 110, 255), special_flags=pygame.BLEND_RGBA_MULT)

        normal[level] = image
        dimmed[level] = dark

    return normal, dimmed


# =========================================================
# LEVEL SELECTION (shared by World 1, 2 and 3)
# =========================================================

def level_selection(screen, game_data, progress_key, code_prefix, world_number):
    background = load_image("pictures/level_selection.png", (WIDTH, HEIGHT))
    normal_images, dimmed_images = load_level_images(world_number)
    cheat_input = ""

    while True:
        max_unlocked = game_data.get(progress_key, 1)

        # ---------- DRAW ----------
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 30))
            draw_text(screen, "LEVEL SELECTION", 60, WIDTH // 2, 100, center=True)

        for level in range(1, 6):
            unlocked = level <= max_unlocked
            center_x, center_y = get_level_center(level)

            if unlocked or not DIM_LOCKED:
                image = normal_images[level]
            else:
                image = dimmed_images[level]

            rect = image.get_rect(center=(center_x, center_y))
            screen.blit(image, rect)

            label = "[ UNLOCKED ]" if unlocked else "[ LOCKED ]"
            color = UNLOCKED_COLOR if unlocked else LOCKED_COLOR

            draw_text(screen, label, LABEL_SIZE,
                      center_x, rect.bottom + LABEL_GAP, color, True)

        draw_text(screen, f"Unlocked Levels: 1 - {max_unlocked}", 32,
                  WIDTH // 2, HEIGHT - 45, (255, 215, 0), True)

        pygame.display.update()

        # ---------- EVENTS ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                return None

            if event.key == pygame.K_BACKSPACE:
                cheat_input = cheat_input[:-1]
                continue

            if event.key == pygame.K_RETURN:
                code = cheat_input.lower().strip()
                if code_prefix and code.startswith(code_prefix):
                    suffix = code[len(code_prefix):]
                    if suffix in ("1", "2", "3", "4", "5"):
                        requested_level = min(int(suffix) + 1, 5)
                        game_data[progress_key] = max(
                            game_data.get(progress_key, 1), requested_level
                        )
                cheat_input = ""
                continue

            character = event.unicode.lower()
            if character.isalnum() and len(character) == 1:
                if cheat_input or character.isalpha():
                    cheat_input += character
                    continue

            for key, level in [
                (pygame.K_1, 1), (pygame.K_2, 2), (pygame.K_3, 3),
                (pygame.K_4, 4), (pygame.K_5, 5),
            ]:
                if event.key == key and level <= max_unlocked:
                    return level