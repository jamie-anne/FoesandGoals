import pygame
import sys
import random
import requests
from io import BytesIO


# =========================================================
# WORLD 1 SETTINGS
# =========================================================

WIDTH = 1510
HEIGHT = 890

# Level settings
LEVEL_DATA = {
    1: {
        "hp": 100,
        "bow": (15, 20),
        "sword": (20, 30),
        "bomb": (30, 35),
        "enemy_attack": (15, 35),
        "coins": (90, 100),
        "hospital": 30
    },

    2: {
        "hp": 120,
        "bow": (15, 20),
        "sword": (20, 30),
        "bomb": (30, 35),
        "enemy_attack": (15, 35),
        "coins": (100, 110),
        "hospital": 40
    },

    3: {
        "hp": 150,
        "bow": (20, 30),
        "sword": (30, 40),
        "bomb": (40, 50),
        "enemy_attack": (30, 50),
        "coins": (110, 120),
        "hospital": 40
    },

    4: {
        "hp": 170,
        "bow": (30, 40),
        "sword": (40, 50),
        "bomb": (50, 60),
        "enemy_attack": (40, 60),
        "coins": (120, 130),
        "hospital": 50
    },

    5: {
        "hp": 200,
        "bow": (40, 50),
        "sword": (50, 60),
        "bomb": (60, 70),
        "enemy_attack": (50, 70),
        "coins": (130, 150),
        "hospital": 60
    }
}


# =========================================================
# POKEMON LIST FOR WORLD 1
# =========================================================

POKEMON_LIST = [
    "bulbasaur",
    "oddish",
    "bellsprout",
    "paras",
    "caterpie",
    "weedle",
    "pidgey",
    "rattata"
]


# =========================================================
# IMAGE LOADING
# =========================================================

def load_image(filename, size=None):
    try:
        image = pygame.image.load(filename).convert_alpha()

        if size:
            image = pygame.transform.scale(image, size)

        return image

    except pygame.error:
        print(f"Could not load image: {filename}")
        return None


# =========================================================
# GET POKEMON FROM POKEAPI
# =========================================================

def get_pokemon():

    pokemon_name = random.choice(POKEMON_LIST)

    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None, pokemon_name.capitalize()

        data = response.json()

        artwork_url = data["sprites"]["other"]["official-artwork"]["front_default"]

        image_response = requests.get(
            artwork_url,
            timeout=5
        )

        if image_response.status_code != 200:
            return None, pokemon_name.capitalize()

        pokemon_image = pygame.image.load(
            BytesIO(image_response.content)
        ).convert_alpha()

        pokemon_image = pygame.transform.scale(
            pokemon_image,
            (330, 330)
        )

        return pokemon_image, data["name"].capitalize()

    except Exception as error:
        print("PokéAPI error:", error)

        return None, pokemon_name.capitalize()


# =========================================================
# TEXT HELPER
# =========================================================

def draw_text(
    screen,
    text,
    size,
    x,
    y,
    color=(255, 255, 255)
):

    font = pygame.font.Font(None, size)

    surface = font.render(
        text,
        True,
        color
    )

    screen.blit(
        surface,
        (x, y)
    )


# =========================================================
# LEVEL SELECTION
# =========================================================

def level_selection(screen, max_unlocked):
    image = load_image(
        "pictures/level_selection.png",
        (WIDTH, HEIGHT)
    )

    while True:

        if image:
            screen.blit(
                image,
                (0, 0)
            )

        else:
            screen.fill(
                (30, 30, 30)
            )

            draw_text(
                screen,
                "LEVEL SELECTION",
                60,
                560,
                150
            )

            draw_text(
                screen,
                "1  2  3  4  5",
                50,
                600,
                300
            )

        # ---------------------------------------------
        # SHOW LOCKED LEVELS
        # ---------------------------------------------

        for level in range(1, 6):

            if level > max_unlocked:
                draw_text(
                    screen,
                    "LOCKED",
                    25,
                    550 + ((level - 1) * 110),
                    470,
                    (255, 80, 80)
                )

        # ---------------------------------------------
        # INFORMATION
        # ---------------------------------------------

        draw_text(
            screen,
            f"Unlocked Levels: 1 - {max_unlocked}",
            30,
            550,
            750,
            (255, 215, 0)
        )

        pygame.display.update()

        # ---------------------------------------------
        # EVENTS
        # ---------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # LEVEL 1
                if event.key == pygame.K_1:

                    if max_unlocked >= 1:
                        return 1

                # LEVEL 2
                elif event.key == pygame.K_2:

                    if max_unlocked >= 2:
                        return 2

                # LEVEL 3
                elif event.key == pygame.K_3:

                    if max_unlocked >= 3:
                        return 3

                # LEVEL 4
                elif event.key == pygame.K_4:

                    if max_unlocked >= 4:
                        return 4

                # LEVEL 5
                elif event.key == pygame.K_5:

                    if max_unlocked >= 5:
                        return 5

                elif event.key == pygame.K_ESCAPE:

                    return None


# =========================================================
# INSTRUCTION SCREEN
# =========================================================

def instruction_screen(screen):

    image = load_image(
        "pictures/instruction_world1.png",
        (WIDTH, HEIGHT)
    )

    while True:

        if image:
            screen.blit(
                image,
                (0, 0)
            )

        else:
            screen.fill(
                (20, 20, 20)
            )

            draw_text(
                screen,
                "WORLD 1",
                70,
                650,
                250
            )

            draw_text(
                screen,
                "Press ENTER to continue",
                45,
                560,
                400
            )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return True

                elif event.key == pygame.K_ESCAPE:
                    return False


# =========================================================
# HEALTH BAR
# =========================================================

def draw_health_bar(
    screen,
    x,
    y,
    width,
    height,
    current_hp,
    max_hp
):

    # Background
    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (x, y, width, height)
    )

    # HP percentage
    percentage = current_hp / max_hp

    if percentage < 0:
        percentage = 0

    hp_width = int(
        width * percentage
    )

    # HP
    pygame.draw.rect(
        screen,
        (40, 200, 70),
        (x, y, hp_width, height)
    )

    # Border
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (x, y, width, height),
        3
    )


# =========================================================
# MATCH INTERFACE
# =========================================================

def battle_interface(
    screen,
    level,
    player_hp,
    enemy_hp,
    max_enemy_hp,
    pokemon_image,
    pokemon_name
):

    background = load_image(
        "pictures/places_1.png",
        (WIDTH, HEIGHT)
    )

    if background:
        screen.blit(
            background,
            (0, 0)
        )

    else:
        screen.fill(
            (40, 70, 40)
        )

    # -----------------------------------------------------
    # DARK SLANTED UI AREA
    # -----------------------------------------------------

    pygame.draw.polygon(
        screen,
        (20, 20, 25),
        [
            (0, 620),
            (1510, 570),
            (1510, 890),
            (0, 890)
        ]
    )

    # -----------------------------------------------------
    # ENEMY
    # -----------------------------------------------------

    if pokemon_image:

        screen.blit(
            pokemon_image,
            (1050, 100)
        )

    draw_text(
        screen,
        pokemon_name,
        40,
        1080,
        40
    )

    # Enemy HP
    draw_health_bar(
        screen,
        1040,
        85,
        350,
        30,
        enemy_hp,
        max_enemy_hp
    )

    draw_text(
        screen,
        f"{enemy_hp}/{max_enemy_hp}",
        25,
        1400,
        88
    )

    # -----------------------------------------------------
    # PLAYER HP
    # -----------------------------------------------------

    draw_text(
        screen,
        "PLAYER",
        40,
        80,
        650
    )

    draw_health_bar(
        screen,
        80,
        700,
        350,
        35,
        player_hp,
        LEVEL_DATA[level]["hp"]
    )

    draw_text(
        screen,
        f"{player_hp}/{LEVEL_DATA[level]['hp']}",
        28,
        440,
        703
    )

    # -----------------------------------------------------
    # LEVEL
    # -----------------------------------------------------

    draw_text(
        screen,
        f"LEVEL {level}",
        35,
        80,
        60
    )

    pygame.display.update()


# =========================================================
# PLACE SCREEN
# Automatically continues after 2 seconds
# =========================================================

def place_screen(screen):

    place_image = load_image(
        "pictures/places_1.png",
        (WIDTH, HEIGHT)
    )

    start_time = pygame.time.get_ticks()

    while True:

        if place_image:
            screen.blit(
                place_image,
                (0, 0)
            )

        else:
            screen.fill(
                (30, 30, 30)
            )

            draw_text(
                screen,
                "PLACE 1",
                70,
                650,
                300
            )

        pygame.display.update()

        # Allow window closing
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return False

        # 2 seconds
        if pygame.time.get_ticks() - start_time >= 2000:
            return True


# =========================================================
# ENEMY INTRO SCREEN
# White background + enemy in middle
# 2 seconds
# =========================================================

def enemy_intro_screen(
    screen,
    pokemon_image,
    pokemon_name
):

    start_time = pygame.time.get_ticks()

    while True:

        screen.fill(
            (255, 255, 255)
        )

        # Enemy in the middle
        if pokemon_image:

            image_rect = pokemon_image.get_rect(
                center=(WIDTH // 2, 390)
            )

            screen.blit(
                pokemon_image,
                image_rect
            )

        # Enemy name
        font = pygame.font.Font(
            None,
            50
        )

        name_surface = font.render(
            pokemon_name,
            True,
            (20, 20, 20)
        )

        name_rect = name_surface.get_rect(
            center=(WIDTH // 2, 700)
        )

        screen.blit(
            name_surface,
            name_rect
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return False

        # 2 seconds
        if pygame.time.get_ticks() - start_time >= 2000:
            return True


# =========================================================
# SLOT MACHINE
# SPACE = START
# SPACE = STOP
# =========================================================

def slot_machine(screen):

    symbols = [
        "🏹",
        "⚔️",
        "💣"
    ]

    reels = [
        random.choice(symbols),
        random.choice(symbols),
        random.choice(symbols)
    ]

    # Emoji font
    emoji_font = pygame.font.Font(
        r"C:\Windows\Fonts\seguiemj.ttf",
        100
    )

    title_font = pygame.font.Font(
        None,
        65
    )

    small_font = pygame.font.Font(
        None,
        40
    )

    reel_x = [
        480,
        705,
        930
    ]

    reel_y = 300

    spinning = False

    last_change = 0

    change_delay = 100

    clock = pygame.time.Clock()

    while True:

        # =================================================
        # EVENTS
        # =================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # SPACE = START / STOP
                if event.key == pygame.K_SPACE:

                    # START
                    if not spinning:

                        spinning = True

                    # STOP
                    else:

                        spinning = False
                        # Middle reel determines attack
                        selected_symbol = reels[1]
                        if selected_symbol == "🏹":
                            selected_attack = "BOW"
                        elif selected_symbol == "⚔️":
                            selected_attack = "SWORD"
                        elif selected_symbol == "💣":
                            selected_attack = "BOMB"
                        # Freeze the current slot machine result
                        # for 2 seconds
                        pygame.display.flip()
                        pygame.time.delay(2000)

                        return selected_attack

                elif event.key == pygame.K_ESCAPE:

                    return None

        # =================================================
        # UPDATE
        # =================================================

        current_time = pygame.time.get_ticks()

        if spinning:

            if current_time - last_change >= change_delay:

                for i in range(3):
                    reels[i] = random.choice(symbols)

                last_change = current_time

        # =================================================
        # DRAW
        # =================================================

        screen.fill(
            (25, 25, 30)
        )

        # Title
        title = title_font.render(
            "FOES & GOALS",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            (620, 100)
        )

        # Slot machine
        for i in range(3):

            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (
                    reel_x[i],
                    reel_y,
                    160,
                    160
                )
            )

            pygame.draw.rect(
                screen,
                (255, 215, 0),
                (
                    reel_x[i],
                    reel_y,
                    160,
                    160
                ),
                4
            )

            emoji = emoji_font.render(
                reels[i],
                True,
                (0, 0, 0)
            )

            screen.blit(
                emoji,
                (
                    reel_x[i] + 80 - emoji.get_width() // 2,
                    reel_y + 25
                )
            )

        draw_text(
            screen,
            "ATTACK",
            30,
            reel_x[1] + 45,
            reel_y - 45,
            (255, 215, 0)
        )

        # Instructions
        if spinning:
            message = "PRESS SPACE TO STOP"
        else:
            message = "PRESS SPACE TO START"

        text = small_font.render(
            message,
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (620, 600)
        )

        pygame.display.flip()

        clock.tick(60)


# =========================================================
# YOUR ATTACK ANIMATION
# PLACE YOUR REAL ANIMATION HERE LATER
# =========================================================

def attack_animation_placeholder(
    screen,
    attack,
    damage
):

    screen.fill(
        (15, 15, 20)
    )

    draw_text(
        screen,
        "[ANIMATION]",
        80,
        580,
        280
    )

    draw_text(
        screen,
        f"{attack} ATTACK!",
        55,
        590,
        390
    )

    draw_text(
        screen,
        f"DAMAGE: {damage}",
        45,
        620,
        470
    )

    pygame.display.update()

    # Placeholder only.
    # Your real animation can replace this.
    pygame.time.delay(1200)


# =========================================================
# PLAYER ATTACK POINTS
# DISPLAY FOR 2 SECONDS
# =========================================================

def player_attack_screen(
    screen,
    attack,
    damage
):

    start_time = pygame.time.get_ticks()

    while True:

        screen.fill(
            (20, 30, 20)
        )

        draw_text(
            screen,
            "PLAYER ATTACK",
            70,
            550,
            250
        )

        draw_text(
            screen,
            attack,
            65,
            650,
            350
        )

        draw_text(
            screen,
            f"-{damage} HP",
            70,
            620,
            450
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return

        # 2 seconds
        if pygame.time.get_ticks() - start_time >= 2000:
            return


# =========================================================
# ENEMY ATTACK POINTS
# DISPLAY FOR 2 SECONDS
# =========================================================

def enemy_attack_screen(
    screen,
    damage
):

    start_time = pygame.time.get_ticks()

    while True:

        screen.fill(
            (40, 15, 15)
        )

        draw_text(
            screen,
            "ENEMY ATTACK!",
            70,
            550,
            300
        )

        draw_text(
            screen,
            f"-{damage} HP",
            70,
            620,
            420
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return

        # 2 seconds
        if pygame.time.get_ticks() - start_time >= 2000:
            return


# =========================================================
# WIN SCREEN
# =========================================================

def win_screen(
    screen,
    coins
):

    screen.fill(
        (20, 70, 30)
    )

    draw_text(
        screen,
        "YOU WIN!",
        90,
        600,
        250
    )

    draw_text(
        screen,
        f"+{coins} COINS",
        60,
        620,
        380
    )

    draw_text(
        screen,
        "Press ENTER to continue",
        40,
        550,
        520
    )

    pygame.display.update()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return


# =========================================================
# HOSPITAL / LOSE SCREEN
# =========================================================

def hospital_screen(
    screen,
    seconds
):

    clock = pygame.time.Clock()

    start_time = pygame.time.get_ticks()

    while True:

        elapsed = (
            pygame.time.get_ticks() - start_time
        ) // 1000

        remaining = seconds - elapsed

        if remaining <= 0:
            break

        screen.fill(
            (230, 230, 230)
        )

        draw_text(
            screen,
            "HOSPITAL",
            80,
            610,
            220,
            (30, 30, 30)
        )

        draw_text(
            screen,
            "YOU LOST!",
            60,
            630,
            340,
            (150, 30, 30)
        )

        draw_text(
            screen,
            f"Recovery Time: {remaining}s",
            50,
            570,
            450,
            (30, 30, 30)
        )

        pygame.display.update()

        clock.tick(30)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    screen.fill(
        (30, 30, 30)
    )

    draw_text(
        screen,
        "RECOVERED!",
        70,
        580,
        350
    )

    pygame.display.update()

    pygame.time.delay(1000)


# =========================================================
# START BATTLE
# =========================================================

def start_battle(
    screen,
    level,
    game_data
):

    stats = LEVEL_DATA[level]

    # =====================================================
    # 1. PLACE
    # Automatically shown for 2 seconds
    # =====================================================

    continue_game = place_screen(screen)

    if not continue_game:
        return

    # =====================================================
    # 2. GET POKEMON
    # =====================================================

    player_hp = stats["hp"]

    enemy_hp = stats["hp"]

    pokemon_image, pokemon_name = get_pokemon()

    # =====================================================
    # 3. ENEMY INTRO
    # White background
    # Enemy in middle
    # 2 seconds
    # =====================================================

    continue_game = enemy_intro_screen(
        screen,
        pokemon_image,
        pokemon_name
    )

    if not continue_game:
        return

    # =====================================================
    # BATTLE LOOP
    # =====================================================

    while player_hp > 0 and enemy_hp > 0:

        # =================================================
        # 4. MATCH INTERFACE
        # 3 seconds
        # =================================================

        battle_interface(
            screen,
            level,
            player_hp,
            enemy_hp,
            stats["hp"],
            pokemon_image,
            pokemon_name
        )

        pygame.time.delay(3000)

        # =================================================
        # 5. SLOT MACHINE
        # SPACE = START
        # SPACE = STOP
        # =================================================

        attack = slot_machine(screen)

        if attack is None:
            return

        # =================================================
        # 6. CALCULATE PLAYER DAMAGE
        # =================================================

        damage_range = stats[
            attack.lower()
        ]

        damage = random.randint(
            damage_range[0],
            damage_range[1]
        )

        enemy_hp -= damage

        if enemy_hp < 0:
            enemy_hp = 0

        # =================================================
        # 7. YOUR ATTACK ANIMATION
        # =================================================

        attack_animation_placeholder(
            screen,
            attack,
            damage
        )

        # =================================================
        # 8. PLAYER ATTACK POINTS
        # 2 seconds
        # =================================================

        player_attack_screen(
            screen,
            attack,
            damage
        )

        # =================================================
        # 9. CHECK IF ENEMY IS DEAD
        # =================================================

        if enemy_hp <= 0:

            coins = random.randint(
                stats["coins"][0],
                stats["coins"][1]
            )

            game_data["coins"] += coins

            win_screen(
                screen,
                coins
            )

            return True

        # =================================================
        # 10. MATCH INTERFACE AGAIN
        # 3 seconds
        # =================================================

        battle_interface(
            screen,
            level,
            player_hp,
            enemy_hp,
            stats["hp"],
            pokemon_image,
            pokemon_name
        )

        pygame.time.delay(3000)

        # =================================================
        # 11. ENEMY ATTACK
        # =================================================

        enemy_damage = random.randint(
            stats["enemy_attack"][0],
            stats["enemy_attack"][1]
        )

        player_hp -= enemy_damage

        if player_hp < 0:
            player_hp = 0

        # =================================================
        # 12. ENEMY ATTACK POINTS
        # 2 seconds
        # =================================================

        enemy_attack_screen(
            screen,
            enemy_damage
        )

        # =================================================
        # 13. CHECK IF PLAYER IS DEAD
        # =================================================

        if player_hp <= 0:

            hospital_screen(
                screen,
                stats["hospital"]
            )

            return False

        # =================================================
        # 14. LOOP
        #
        # Goes back to MATCH INTERFACE
        # Then SLOT MACHINE
        # Then PLAYER ATTACK
        # Then MATCH
        # Then ENEMY ATTACK
        # =================================================


# =========================================================
# WORLD 1
# =========================================================

def world1(
    screen,
    game_data
):

    # ---------------------------------------------
    # WORLD 1 LEVEL PROGRESS
    # ---------------------------------------------

    if "world1_unlocked" not in game_data:
        game_data["world1_unlocked"] = 1

    while True:

        # ---------------------------------------------
        # LEVEL SELECTION
        # ---------------------------------------------

        level = level_selection(
            screen,
            game_data["world1_unlocked"]
        )

        if level is None:
            return

        # ---------------------------------------------
        # INSTRUCTIONS
        # ---------------------------------------------

        continue_game = instruction_screen(screen)

        if not continue_game:
            return

        # ---------------------------------------------
        # START BATTLE
        # ---------------------------------------------

        result = start_battle(
            screen,
            level,
            game_data
        )

        # ---------------------------------------------
        # UNLOCK NEXT LEVEL
        # ---------------------------------------------

        if result == True:

            if level == game_data["world1_unlocked"]:

                if game_data["world1_unlocked"] < 5:

                    game_data["world1_unlocked"] += 1

        # =================================================
        # 2. INSTRUCTIONS
        # Press ENTER to continue
        # =================================================

        continue_game = instruction_screen(screen)

        if not continue_game:
            return

        # =================================================
        # 3. START BATTLE
        # =================================================

        start_battle(
            screen,
            level,
            game_data
        )

