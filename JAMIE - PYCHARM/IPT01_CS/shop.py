import pygame
import sys
import math

parts = [
    {"name": "LCD", "price": 100},
    {"name": "iPhone Case", "price": 200},
    {"name": "Battery", "price": 300},
    {"name": "Camera", "price": 400},
    {"name": "Speaker", "price": 500},
    {"name": "Buttons", "price": 600},
    {"name": "Charging Port", "price": 700},
    {"name": "Back Glass", "price": 800},
    {"name": "Front Glass", "price": 900},
    {"name": "Face ID", "price": 1000},
    {"name": "Motherboard", "price": 1100},
    {"name": "Final Assembly", "price": 1200}
]


# ==================================================
# UI HELPERS (visual only)
# ==================================================
def make_background(width, height):
    bg = pygame.Surface((width, height))
    top = (90, 160, 230)
    mid = (150, 200, 245)
    bottom = (200, 230, 200)
    for y in range(height):
        t = y / height
        if t < 0.5:
            k = t / 0.5
            a, b = top, mid
        else:
            k = (t - 0.5) / 0.5
            a, b = mid, bottom
        color = (
            int(a[0] + (b[0] - a[0]) * k),
            int(a[1] + (b[1] - a[1]) * k),
            int(a[2] + (b[2] - a[2]) * k),
        )
        pygame.draw.line(bg, color, (0, y), (width, y))

    # Scattered soft stars / sparkles
    stars = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(70):
        sx = (i * 223 + 57) % width
        sy = (i * 131 + 23) % height
        size = 1 + (i % 3)
        pygame.draw.circle(stars, (255, 255, 255, 60 + (i % 4) * 25), (sx, sy), size)
    bg.blit(stars, (0, 0))
    return bg


def draw_shadow(screen, rect, radius=16, offset=6, alpha=90):
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(
        shadow, (0, 0, 0, alpha), shadow.get_rect(), border_radius=radius
    )
    screen.blit(shadow, (rect.x + offset, rect.y + offset))


def draw_panel(screen, rect, fill, border, border_width=2, radius=16):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, fill, panel.get_rect(), border_radius=radius)
    screen.blit(panel, rect.topleft)
    pygame.draw.rect(
        screen, border, rect, border_width, border_radius=radius
    )


def draw_text_shadow(screen, font, text, color, pos, shadow=(0, 0, 0), offset=2):
    screen.blit(font.render(text, True, shadow), (pos[0] + offset, pos[1] + offset))
    screen.blit(font.render(text, True, color), pos)


def draw_coin(screen, center, radius):
    pygame.draw.circle(screen, (190, 140, 0), center, radius)
    pygame.draw.circle(screen, (255, 215, 40), center, radius - 2)
    pygame.draw.circle(screen, (255, 240, 130), center, radius - 6, 2)


def draw_lock(screen, center):
    cx, cy = center
    # shackle
    pygame.draw.arc(
        screen, (220, 220, 230),
        (cx - 14, cy - 34, 28, 36), 0, math.pi, 5
    )
    pygame.draw.line(screen, (220, 220, 230), (cx - 14, cy - 16), (cx - 14, cy - 6), 5)
    pygame.draw.line(screen, (220, 220, 230), (cx + 13, cy - 16), (cx + 13, cy - 6), 5)
    # body
    body = pygame.Rect(cx - 22, cy - 8, 44, 34)
    pygame.draw.rect(screen, (150, 150, 170), body, border_radius=6)
    pygame.draw.rect(screen, (230, 230, 240), body, 2, border_radius=6)
    pygame.draw.circle(screen, (50, 50, 70), (cx, cy + 6), 5)
    pygame.draw.rect(screen, (50, 50, 70), (cx - 2, cy + 8, 4, 10))


def draw_check(screen, center):
    cx, cy = center
    pygame.draw.circle(screen, (30, 150, 70), (cx, cy), 30)
    pygame.draw.circle(screen, (120, 240, 160), (cx, cy), 30, 3)
    pygame.draw.lines(
        screen, (255, 255, 255), False,
        [(cx - 14, cy), (cx - 4, cy + 11), (cx + 15, cy - 11)], 6
    )


# ==================================================
# SHOP
# ==================================================
def shop(screen, game_data):
    WIDTH = 1510
    HEIGHT = 890
    clock = pygame.time.Clock()

    # ------------------------------------------------
    # LOAD 12 PART IMAGES
    # -----------------------------------------------
    part_images = []
    for i in range(1, 13):
        image = pygame.image.load(
            f"pictures/shop_part{i}.png"
        ).convert_alpha()
        part_images.append(image)
    # ------------------------------------------------
    # RESIZE ALL IMAGES TO SAME SIZE
    # ------------------------------------------------
    image_width = 250
    image_height = 150
    resized_images = []
    for image in part_images:
        image = pygame.transform.smoothscale(
            image,
            (image_width, image_height)
        )
        resized_images.append(image)

    # Greyed-out copies for locked parts
    locked_images = []
    for image in resized_images:
        grey = image.copy()
        dark = pygame.Surface(grey.get_size(), pygame.SRCALPHA)
        dark.fill((20, 15, 40, 170))
        grey.blit(dark, (0, 0))
        locked_images.append(grey)

    # ------------------------------------------------
    # BACKGROUND (uses your own art if the file exists)
    # ------------------------------------------------
    try:
        background = pygame.image.load("pictures/").convert()
        background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))
        tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        tint.fill((15, 10, 40, 120))  # darken so cards stay readable
        background.blit(tint, (0, 0))
    except (pygame.error, FileNotFoundError):
        background = make_background(WIDTH, HEIGHT)

    # ------------------------------------------------
    # FONTS
    # ------------------------------------------------
    title_font = pygame.font.Font(None, 70)
    info_font = pygame.font.Font(None, 30)
    part_font = pygame.font.Font(None, 25)
    badge_font = pygame.font.Font(None, 22)
    number_font = pygame.font.Font(None, 28)

    # ------------------------------------------------
    # CARD LAYOUT
    # ------------------------------------------------
    card_w = 330
    card_h = 225
    gap_x = 30
    gap_y = 12
    start_x = (WIDTH - (4 * card_w + 3 * gap_x)) // 2
    start_y = 82

    status_colors = {
        "BOUGHT": (60, 190, 100),
        "AVAILABLE": (255, 205, 60),
        "LOCKED": (130, 130, 150),
    }

    # ------------------------------------------------
    # TEXT INPUT
    # ------------------------------------------------
    input_text = ""
    message = ""
    running = True
    while running:
        ticks = pygame.time.get_ticks()
        pulse = (math.sin(ticks / 250) + 1) / 2  # 0..1

        screen.blit(background, (0, 0))

        # ==================================================
        # HEADER BAR
        # ==================================================
        header = pygame.Rect(40, 12, WIDTH - 80, 60)
        draw_shadow(screen, header, radius=14, offset=4, alpha=80)
        draw_panel(screen, header, (20, 14, 48, 215), (160, 130, 255), 2, 14)

        # ESC instruction (left)
        esc_badge = pygame.Rect(58, 26, 120, 32)
        pygame.draw.rect(screen, (60, 50, 100), esc_badge, border_radius=8)
        pygame.draw.rect(screen, (170, 150, 240), esc_badge, 2, border_radius=8)
        esc_text = info_font.render("ESC = Back", True, (225, 220, 250))
        screen.blit(
            esc_text,
            (esc_badge.centerx - esc_text.get_width() // 2,
             esc_badge.centery - esc_text.get_height() // 2)
        )

        # Title (center)
        title_text = "SHOP"
        title_w = title_font.size(title_text)[0]
        draw_text_shadow(
            screen, title_font, title_text, (255, 235, 150),
            (WIDTH // 2 - title_w // 2, 22), shadow=(80, 40, 20), offset=3
        )

        # Coins (right)
        coins_label = f"{game_data['coins']}"
        coins_surface = info_font.render(coins_label, True, (255, 220, 0))
        pill_w = coins_surface.get_width() + 80
        pill = pygame.Rect(WIDTH - 58 - pill_w, 24, pill_w, 36)
        pygame.draw.rect(screen, (50, 38, 10), pill, border_radius=18)
        pygame.draw.rect(screen, (255, 215, 40), pill, 2, border_radius=18)
        draw_coin(screen, (pill.x + 20, pill.centery), 12)
        screen.blit(
            coins_surface,
            (pill.x + 42, pill.centery - coins_surface.get_height() // 2)
        )

        # ==================================================
        # DISPLAY 12 PARTS
        # ==================================================
        for i in range(12):

            # 4 columns
            column = i % 4
            # 3 rows
            row = i // 4
            # Position of each box
            x = start_x + column * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)

            # ------------------------------------------------
            # STATUS (same rule as before)
            # ------------------------------------------------
            if i < game_data["parts_bought"]:
                status = "BOUGHT"
            elif i == game_data["parts_bought"]:
                status = "AVAILABLE"
            else:
                status = "LOCKED"
            accent = status_colors[status]

            # ------------------------------------------------
            # CARD
            # ------------------------------------------------
            card = pygame.Rect(x, y, card_w, card_h)
            draw_shadow(screen, card)
            if status == "LOCKED":
                fill = (25, 20, 45, 200)
                border = (80, 75, 110)
                border_w = 2
            elif status == "BOUGHT":
                fill = (20, 50, 40, 215)
                border = (60, 190, 100)
                border_w = 2
            else:
                fill = (45, 35, 85, 235)
                glow = int(170 + 85 * pulse)
                border = (glow, int(glow * 0.8), 60)
                border_w = 3
            draw_panel(screen, card, fill, border, border_w, 16)

            # Image frame
            image_x = x + (card_w - image_width) // 2
            image_y = y + 10
            frame = pygame.Rect(image_x - 4, image_y - 4, image_width + 8, image_height + 8)
            pygame.draw.rect(screen, (12, 8, 30), frame, border_radius=10)

            # Draw image
            if status == "LOCKED":
                screen.blit(locked_images[i], (image_x, image_y))
                draw_lock(screen, (image_x + image_width // 2, image_y + image_height // 2))
            else:
                screen.blit(resized_images[i], (image_x, image_y))
                if status == "BOUGHT":
                    shade = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
                    shade.fill((0, 40, 20, 110))
                    screen.blit(shade, (image_x, image_y))
                    draw_check(screen, (image_x + image_width // 2, image_y + image_height // 2))
            pygame.draw.rect(screen, accent, frame, 2, border_radius=10)

            # Number badge (the number the player types)
            num_rect = pygame.Rect(image_x - 10, image_y - 10, 36, 30)
            pygame.draw.rect(screen, (20, 14, 48), num_rect, border_radius=8)
            pygame.draw.rect(screen, accent, num_rect, 2, border_radius=8)
            num_text = number_font.render(str(i + 1), True, (255, 255, 255))
            screen.blit(
                num_text,
                (num_rect.centerx - num_text.get_width() // 2,
                 num_rect.centery - num_text.get_height() // 2)
            )

            # ------------------------------------------------
            # PART NAME
            # ------------------------------------------------
            name_color = (150, 150, 170) if status == "LOCKED" else (255, 255, 255)
            name_text = part_font.render(
                f"{i + 1}. {parts[i]['name']}",
                True,
                name_color
            )
            screen.blit(
                name_text,
                (
                    x + 16,
                    y + image_height + 22
                )
            )
            # ------------------------------------------------
            # PRICE
            # ------------------------------------------------
            draw_coin(screen, (x + 24, y + image_height + 58), 9)
            price_color = (150, 130, 60) if status == "LOCKED" else (255, 220, 0)
            price_text = part_font.render(
                f"Price: {parts[i]['price']} coins",
                True,
                price_color
            )
            screen.blit(
                price_text,
                (
                    x + 40,
                    y + image_height + 49
                )
            )
            # ------------------------------------------------
            # STATUS BADGE
            # ------------------------------------------------
            status_text = badge_font.render(status, True, (20, 14, 40))
            badge_w = status_text.get_width() + 20
            badge = pygame.Rect(
                x + card_w - badge_w - 14,
                y + image_height + 22,
                badge_w, 24
            )
            pygame.draw.rect(screen, accent, badge, border_radius=12)
            screen.blit(
                status_text,
                (badge.centerx - status_text.get_width() // 2,
                 badge.centery - status_text.get_height() // 2)
            )

        # ==================================================
        # INPUT AREA
        # ==================================================
        bar = pygame.Rect(40, 800, WIDTH - 80, 72)
        draw_shadow(screen, bar, radius=14, offset=4, alpha=80)
        draw_panel(screen, bar, (20, 14, 48, 225), (160, 130, 255), 2, 14)

        input_label = info_font.render(
            "Enter the number you want to buy:",
            True,
            (255, 255, 255)
        )
        screen.blit(
            input_label,
            (70, 825)
        )
        # Input box
        input_rect = pygame.Rect(415, 816, 100, 40)
        pygame.draw.rect(screen, (12, 8, 30), input_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 235, 150), input_rect, 2, border_radius=8)
        input_display = info_font.render(
            input_text,
            True,
            (255, 255, 255)
        )
        screen.blit(
            input_display,
            (input_rect.x + 16, input_rect.centery - input_display.get_height() // 2)
        )
        # Blinking cursor
        if (ticks // 500) % 2 == 0:
            cursor_x = input_rect.x + 16 + input_display.get_width() + 3
            pygame.draw.line(
                screen, (255, 235, 150),
                (cursor_x, input_rect.y + 9), (cursor_x, input_rect.bottom - 9), 2
            )

        # Message (green for success, red-ish for problems)
        if message == "":
            message_color = (255, 255, 255)
        elif "purchased" in message:
            message_color = (120, 240, 150)
        else:
            message_color = (255, 130, 130)
        message_text = info_font.render(
            message,
            True,
            message_color
        )
        screen.blit(
            message_text,
            (550, 825)
        )

        pygame.display.update()
        clock.tick(60)
        # ==================================================
        # EVENTS
        # ==================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # -----------------------------------------
                # ESC
                # ------------------------------------------
                if event.key == pygame.K_ESCAPE:
                    running = False
                # ------------------------------------------
                # BACKSPACE
                # ------------------------------------------
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                # -----------------------------------------
                # ENTER
                # ------------------------------------------
                elif event.key == pygame.K_RETURN:
                    if input_text != "":
                        try:
                            selected_number = int(input_text)
                            result = buy_part(
                                selected_number,
                                game_data
                            )
                            input_text = ""
                            message = result
                        except ValueError:
                            input_text = ""
                            message = "Please enter a valid number."
                # ------------------------------------------
                # NUMBER INPUT
                # ------------------------------------------
                elif event.unicode.isdigit():
                    if len(input_text) < 2:
                        input_text += event.unicode


# ==================================================
# BUY PART
# ==================================================
def buy_part(number, game_data):
    # ----------------------------------------------
    # INVALID NUMBER
    # ----------------------------------------------

    if number < 1 or number > 12:
        return "Enter a number from 1 to 12."
    index = number - 1
    # ----------------------------------------------
    # ALREADY BOUGHT
    # ----------------------------------------------
    if index < game_data["parts_bought"]:
        return "You already bought this part."
    # ----------------------------------------------
    # LOCKED
    # ----------------------------------------------
    if index > game_data["parts_bought"]:
        next_part = game_data["parts_bought"] + 1
        return f"Part {number} is locked. Buy Part {next_part} first."
    # ----------------------------------------------
    # CHECK COINS
    # ----------------------------------------------
    price = parts[index]["price"]
    if game_data["coins"] < price:
        return "Not enough coins."
    # ----------------------------------------------
    # PURCHASE
    # ----------------------------------------------
    game_data["coins"] -= price
    game_data["parts_bought"] += 1
    return f"{parts[index]['name']} purchased!"
# ==================================================
# PURCHASE MESSAGE
# ==================================================
def get_message(number, game_data):
    index = number - 1
    # Invalid number
    if number < 1 or number > 12:
        return "Enter a number from 1 to 12."
    # Already bought
    if index < game_data["parts_bought"]:
        return "You already bought this part."
    # Locked
    if index > game_data["parts_bought"]:
        next_part = game_data["parts_bought"] + 1
        return f"Part {number} is locked. Buy Part {next_part} first."
    # This was the correct part.
    # Check whether the purchase actually happened.
    if game_data["coins"] >= parts[index]["price"]:
        return "Not enough coins."
    return f"{parts[index]['name']} purchased!"