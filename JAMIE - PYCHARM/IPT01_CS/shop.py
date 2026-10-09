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
# ==================================================
# SHOP
# ==================================================
def shop(screen, game_data):
    WIDTH = 1510
    HEIGHT = 890
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
    # ------------------------------------------------
    # FONTS
    # ------------------------------------------------
    title_font = pygame.font.Font(None, 55)
    info_font = pygame.font.Font(None, 30)
    part_font = pygame.font.Font(None, 25)
    # ------------------------------------------------
    # TEXT INPUT
    # ------------------------------------------------
    input_text = ""
    message = ""
    running = True
    while running:

        screen.fill((20, 20, 20))
        # ==================================================
        # TITLE
        # ==================================================

        title = title_font.render(
            "SHOP",
            True,
            (255, 255, 255)
        )
        screen.blit(
            title,
            (640 - title.get_width() // 2, 15)
        )
        # =================================================
        # COINS
        # ==================================================
        coins_text = info_font.render(
            f"Coins: {game_data['coins']}",
            True,
            (255, 220, 0)
        )
        screen.blit(
            coins_text,
            (1100, 25)
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
            x = 70 + column * 370
            y = 80 + row * 235
            # Draw image
            screen.blit(
                resized_images[i],
                (x, y)
            )
            # ------------------------------------------------
            # PART NAME
            # ------------------------------------------------
            name_text = part_font.render(
                f"{i + 1}. {parts[i]['name']}",
                True,
                (255, 255, 255)
            )
            screen.blit(
                name_text,
                (
                    x,
                    y + image_height + 5
                )
            )
            # ------------------------------------------------
            # PRICE
            # ------------------------------------------------
            price_text = part_font.render(
                f"Price: {parts[i]['price']} coins",
                True,
                (255, 220, 0)
            )
            screen.blit(
                price_text,
                (
                    x,
                    y + image_height + 32
                )
            )
            # -----------------------------------------------
            # STATUS
            # ------------------------------------------------
            if i < game_data["parts_bought"]:
                status = "BOUGHT"
            elif i == game_data["parts_bought"]:
                status = "AVAILABLE"
            else:
                status = "LOCKED"
            status_text = part_font.render(
                f"Status: {status}",
                True,
                (255, 255, 255)
            )
            screen.blit(
                status_text,
                (
                    x,
                    y + image_height + 59
                )
            )
        # ==================================================
        # INPUT AREA
        # ==================================================
        input_label = info_font.render(
            "Enter the number you want to buy:",
            True,
            (255, 255, 255)
        )
        screen.blit(
            input_label,
            (70, 820)
        )
        # Input box
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (415, 810, 100, 40),
            2
        )
        input_display = info_font.render(
            input_text,
            True,
            (255, 255, 255)
        )
        screen.blit(
            input_display,
            (450, 820)
        )
        # Message
        message_text = info_font.render(
            message,
            True,
            (255, 255, 255)
        )
        screen.blit(
            message_text,
            (550, 820)
        )
        # ESC instruction
        esc_text = info_font.render(
            "ESC = Back",
            True,
            (180, 180, 180)
        )
        screen.blit(
            esc_text,
            (70, 25)
        )
        pygame.display.update()
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