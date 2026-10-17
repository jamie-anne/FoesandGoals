import pygame
import sys

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

# SETTINGS (easy things to change)
BACKGROUND_FILE = "pictures/shop_bg.jpg"   # your photo (optional)
BACKGROUND_COLOR = (25, 30, 45)                    # used if no photo is found
CARD_COLOR = (40, 45, 65)
TEXT_COLOR = (255, 255, 255)
GOLD = (255, 220, 0)
STATUS_COLORS = {
    "BOUGHT": (80, 200, 120),
    "AVAILABLE": (255, 220, 0),
    "LOCKED": (130, 130, 140),
}


# SHOP
def shop(screen, game_data):
    WIDTH = 1510
    HEIGHT = 890

    # LOAD + RESIZE PART IMAGES
    image_width = 250
    image_height = 150
    images = []
    for i in range(1, 13):
        image = pygame.image.load(f"pictures/shop_part{i}.png").convert_alpha()
        images.append(pygame.transform.smoothscale(image, (image_width, image_height)))

    # BACKGROUND (photo if it exists, otherwise a plain color)
    try:
        background = pygame.image.load(BACKGROUND_FILE).convert()
        background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))
    except (pygame.error, OSError):
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(BACKGROUND_COLOR)

    # FONTS
    title_font = pygame.font.Font(None, 55)
    info_font = pygame.font.Font(None, 30)
    part_font = pygame.font.Font(None, 25)

    # LAYOUT
    card_w = 330
    card_h = 225
    gap = 30
    start_x = (WIDTH - (4 * card_w + 3 * gap)) // 2
    start_y = 85

    input_text = ""
    message = ""
    running = True
    while running:

        screen.blit(background, (0, 0))

        # TOP BAR: ESC, TITLE, COINS
        screen.blit(info_font.render("ESC = Back", True, (200, 200, 200)), (70, 28))

        title = title_font.render("SHOP", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 18))

        coins_text = info_font.render(f"Coins: {game_data['coins']}", True, GOLD)
        screen.blit(coins_text, (WIDTH - 70 - coins_text.get_width(), 28))

        # 12 PARTS (4 columns x 3 rows)
        for i in range(12):
            x = start_x + (i % 4) * (card_w + gap)
            y = start_y + (i // 4) * (card_h + 12)

            # Status
            if i < game_data["parts_bought"]:
                status = "BOUGHT"
            elif i == game_data["parts_bought"]:
                status = "AVAILABLE"
            else:
                status = "LOCKED"
            color = STATUS_COLORS[status]

            # Card
            card = pygame.Rect(x, y, card_w, card_h)
            pygame.draw.rect(screen, CARD_COLOR, card, border_radius=12)
            pygame.draw.rect(screen, color, card, 2, border_radius=12)

            # Image
            screen.blit(images[i], (x + (card_w - image_width) // 2, y + 10))

            # Name, price, status
            name_text = part_font.render(f"{i + 1}. {parts[i]['name']}", True, TEXT_COLOR)
            screen.blit(name_text, (x + 15, y + image_height + 20))

            price_text = part_font.render(f"Price: {parts[i]['price']} coins", True, GOLD)
            screen.blit(price_text, (x + 15, y + image_height + 45))

            status_text = part_font.render(status, True, color)
            screen.blit(status_text, (x + card_w - status_text.get_width() - 15, y + image_height + 20))


        # INPUT AREA
        screen.blit(
            info_font.render("Enter the number you want to buy:", True, TEXT_COLOR),
            (70, 820)
        )
        pygame.draw.rect(screen, TEXT_COLOR, (415, 810, 100, 40), 2)
        screen.blit(info_font.render(input_text, True, TEXT_COLOR), (450, 820))
        screen.blit(info_font.render(message, True, TEXT_COLOR), (550, 820))

        pygame.display.update()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                elif event.key == pygame.K_RETURN:
                    if input_text != "":
                        try:
                            selected_number = int(input_text)
                            result = buy_part(selected_number, game_data)
                            input_text = ""
                            message = result
                        except ValueError:
                            input_text = ""
                            message = "Please enter a valid number."

                elif event.unicode.isdigit():
                    if len(input_text) < 2:
                        input_text += event.unicode


# ==================================================
# BUY PART
# ==================================================
def buy_part(number, game_data):
    # INVALID NUMBER
    if number < 1 or number > 12:
        return "Enter a number from 1 to 12."
    index = number - 1
    # ALREADY BOUGHT
    if index < game_data["parts_bought"]:
        return "You already bought this part."
    # LOCKED
    if index > game_data["parts_bought"]:
        next_part = game_data["parts_bought"] + 1
        return f"Part {number} is locked. Buy Part {next_part} first."
    # CHECK COINS
    price = parts[index]["price"]
    if game_data["coins"] < price:
        return "Not enough coins."
    # PURCHASE
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