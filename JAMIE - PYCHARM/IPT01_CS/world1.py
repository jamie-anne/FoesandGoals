import pygame
import sys
import random
import requests
from io import BytesIO
from level_menu import level_selection, mark_cleared
from character import draw_player_character, get_character_name
pygame.mixer.init()

WIDTH = 1510
HEIGHT = 890
click = pygame.mixer.Sound("music/click.mp3")
match_bg = pygame.mixer.Sound("music/match_1.mp3")
match_bg.set_volume(0.4)

# Level settings
LEVEL_DATA = {
    1: {"hp": 100, "two_combi": (20, 30), "three_combi": (25, 30), "enemy_attack": (20, 30), "coins": 100, "hospital": 30},
    2: {"hp": 120, "two_combi": (30, 40), "three_combi": (35, 40), "enemy_attack": (30, 40), "coins": 110, "hospital": 30},
    3: {"hp": 140, "two_combi": (40, 50), "three_combi": (45, 50), "enemy_attack": (40, 50), "coins":  120, "hospital": 30},
    4: {"hp": 160, "two_combi": (50, 60), "three_combi": (55, 60), "enemy_attack": (50, 60), "coins": 130, "hospital": 30},
    5: {"hp": 180, "two_combi": (60, 70), "three_combi": (65, 70), "enemy_attack": (60, 70), "coins": 150, "hospital": 40}
}
# Coins paid to skip the hospital after losing
LOSS_FEE = {1: 50, 2: 60, 3: 70, 4: 80, 5: 90}

LOCATION_DATA = {
    1: {"name": "Intramuros", "latitude": 14.5896, "longitude": 120.9747},
    2: {"name": "Rizal Park", "latitude": 14.5827, "longitude": 120.9793},
    3: {"name": "Tagaytay City", "latitude": 14.1153, "longitude": 120.9621},
    4: {"name": "Gapan City", "latitude": 15.3077, "longitude": 120.9469},
    5: {"name": "Dingalan", "latitude": 15.3897, "longitude": 121.3929}
}


WEATHER_POKEMON_POOLS = {
    "clear": [
        "charmander", "growlithe", "vulpix",
        "sandshrew", "geodude", "bellsprout", "oddish"
    ],
    "cloudy": [
        "pidgey", "spearow", "rattata",
        "eevee", "meowth", "farfetchd", "venonat"
    ],
    "fog": [
        "gastly", "drowzee", "abra",
        "zubat", "haunter", "misdreavus"
    ],
    "rain": [
        "squirtle", "psyduck", "poliwag",
        "oddish", "bellsprout", "lotad", "wingull"
    ],
    "storm": [
        "pikachu", "magnemite", "voltorb",
        "electabuzz", "plusle", "minun"
    ],
    "snow": [
        "seel", "swinub", "spheal",
        "snorunt", "snover", "sneasel"
    ]
}


# IMAGE LOADING
def load_image(filename, size=None):
    try:
        image = pygame.image.load(filename).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error:
        print(f"Could not load image: {filename}")
        return None

# GET CURRENT WEATHER FROM OPEN-METEO
def get_weather_category(level):
    location = LOCATION_DATA[level]
    try:
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "weather_code",
            "timezone": "auto"
        }

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        if response.status_code != 200:
            print("Open-Meteo error:", response.status_code)
            return "clear"

        data = response.json()
        weather_code = data["current"]["weather_code"]

        if weather_code in [0, 1]:
            category = "clear"
        elif weather_code in [2, 3]:
            category = "cloudy"
        elif weather_code in [45, 48]:
            category = "fog"
        elif weather_code in [51, 53, 55, 56, 57, 61, 63, 65,
                              66, 67, 80, 81, 82]:
            category = "rain"
        elif weather_code in [95, 96, 97, 99]:
            category = "storm"
        elif weather_code in [71, 73, 75, 77, 85, 86]:
            category = "snow"
        else:
            category = "clear"

        print(
            f"Weather at {location['name']}: "
            f"WMO {weather_code} -> {category}"
        )

        return category
    except Exception as error:
        print("Open-Meteo error:", error)
        print("Using clear-weather Pokémon pool as fallback.")
        return "clear"


# GET POKEMON FROM WEATHER + POKEAPI
def get_pokemon(level):

    weather_category = get_weather_category(level)
    pokemon_pool = WEATHER_POKEMON_POOLS[weather_category]
    pokemon_name = random.choice(pokemon_pool)

    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(
            url,
            timeout=5
        )
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


# TEXT HELPER
def draw_text(
    screen,
    text,
    size,
    x,
    y,
    color=(255, 255, 255),
    center=False
):

    font = pygame.font.Font(None, size)
    surface = font.render(
        str(text),
        True,
        color
    )

    if center:
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)
    else:
        screen.blit(surface, (x, y))


def instruction_screen(screen):
    image = load_image(
        "pictures/instruction_world1.png",
        (WIDTH, HEIGHT)
    )
    while True:

        if image:
            screen.blit(
                image,
                (0, 0))
        else:
            screen.fill(
                (20, 20, 20))

            draw_text(
                screen,
                "WORLD 1",
                70,
                650,
                250)

            draw_text(
                screen,
                "Press ENTER to continue",
                45,
                560,
                400)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click.play()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    click.play()
                    return True
                elif event.key == pygame.K_ESCAPE:
                    click.play()
                    return False



# HEALTH BAR
def draw_health_bar(
    screen,
    x,
    y,
    width,
    height,
    current_hp,
    max_hp):

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



# MATCH INTERFACE
def battle_interface(screen, level, player_hp, enemy_hp, max_enemy_hp,
                     pokemon_image, pokemon_name):
    screen.fill((235, 235, 235))

    # ---------- ADJUST THESE ----------
    PLAYER_X = 500        # center x of the player (left)
    ENEMY_X = 1080        # center x of the enemy (right)
    CENTER_Y = 470        # vertical center of both fighters
    BAR_W = 330

    # ----------------------------------

    bar_y = CENTER_Y - 165 - 70     # above the head
    name_y = CENTER_Y + 165 + 45    # below the feet

    draw_text(screen, f"LEVEL {level}", 45, WIDTH // 2, 60, (30, 30, 30), True)

    # ENEMY (right)
    draw_health_bar(screen, ENEMY_X - BAR_W // 2, bar_y, BAR_W, 30, enemy_hp, max_enemy_hp)
    draw_text(screen, f"HP: {enemy_hp}/{max_enemy_hp}", 30, ENEMY_X, bar_y - 22, (30, 30, 30), True)
    if pokemon_image:
        screen.blit(pokemon_image, pokemon_image.get_rect(center=(ENEMY_X, CENTER_Y)))
    draw_text(screen, pokemon_name, 45, ENEMY_X, name_y, (30, 30, 30), True)

    # PLAYER (left)
    draw_health_bar(screen, PLAYER_X - BAR_W // 2, bar_y, BAR_W, 30, player_hp, max_enemy_hp)
    draw_text(screen, f"HP: {player_hp}/{max_enemy_hp}", 30, PLAYER_X, bar_y - 22, (30, 30, 30), True)
    draw_player_character(screen, position=(PLAYER_X - 165, CENTER_Y - 165))
    draw_text(screen, get_character_name(), 45, PLAYER_X, name_y, (30, 30, 30), True)

    pygame.display.update()


# PLACE SCREEN
# Automatically continues after 2 seconds
# PLACE SCREEN
# Automatically continues after 1.5 seconds
def place_screen(screen, level):

    PLACE_SCALE = 0.8     # <-- CHANGE THIS: 1.0 = full screen, 0.8 = smaller, 0.5 = half

    # Background (drawn first)
    place_bg = load_image("pictures/place_background.png", (WIDTH, HEIGHT))

    # Badge (drawn on top), resized by PLACE_SCALE
    place_image = load_image(
        f"pictures/places_{level}.png",
        (int(WIDTH * PLACE_SCALE), int(HEIGHT * PLACE_SCALE))
    )
    start_time = pygame.time.get_ticks()
    while True:

        # 1. BACKGROUND
        if place_bg:
            screen.blit(place_bg, (0, 0))
        else:
            screen.fill((20, 70, 130))

        # 2. BADGE (centered on the screen)
        if place_image:
            screen.blit(place_image, place_image.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        else:
            draw_text(screen, LOCATION_DATA[level]["name"], 70,
                      WIDTH // 2, HEIGHT // 2, center=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        if pygame.time.get_ticks() - start_time >= 1500:
            return True

def enemy_intro_screen(
    screen,
    pokemon_image,
    pokemon_name):

    start_time = pygame.time.get_ticks()
    while True:
        screen.fill(
            (255, 255, 255))

        # Enemy in the middle
        if pokemon_image:
            image_rect = pokemon_image.get_rect(
                center=(WIDTH // 2, 390))

            screen.blit(
                pokemon_image,
                image_rect)

        # Enemy name
        font = pygame.font.Font(
            None,
            50)

        name_surface = font.render(
            pokemon_name,
            True,
            (20, 20, 20))

        name_rect = name_surface.get_rect(
            center=(WIDTH // 2, 700))

        screen.blit(
            name_surface,
            name_rect)

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
                        # Determine the attack from the slot-machine combination.
                        if reels[0] == reels[1] == reels[2]:
                            combination = 3
                        elif (
                            reels[0] == reels[1]
                            or reels[0] == reels[2]
                            or reels[1] == reels[2]
                        ):
                            combination = 2
                        else:
                            combination = 0

                        # Freeze the current slot machine result
                        # for 2 seconds
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        return combination
                elif event.key == pygame.K_ESCAPE:
                    return None

        current_time = pygame.time.get_ticks()
        if spinning:
            if current_time - last_change >= change_delay:
                for i in range(3):
                    reels[i] = random.choice(symbols)
                last_change = current_time

        screen.fill(
            (255, 255, 255)
        )
        # Title
        title = title_font.render(
            "FOES & GOALS",
            True,
            (30,30,30))

        screen.blit(
            title,
            (620, 100))

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
                (30,30,30),
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
            (30,30,30)
        )

        # Instructions
        if spinning:
            message = "PRESS SPACE TO STOP"
        else:
            message = "PRESS SPACE TO START"

        text = small_font.render(
            message,
            True,
            (30,30,30)
        )

        screen.blit(
            text,
            (620, 600)
        )

        pygame.display.flip()

        clock.tick(60)


def player_attack_screen(
    screen,
    attack,
    damage
):

    start_time = pygame.time.get_ticks()
    while True:
        screen.fill((255, 255, 255))           # was (20, 30, 20)

        draw_text(screen, "PLAYER ATTACK", 70,
                  WIDTH // 2, 250, (30, 30, 30), True)

        draw_text(screen, f"-{damage} HP", 70,
                  WIDTH // 2, 450, (180, 30, 30), True)

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



def enemy_attack_screen(screen, damage, missed=False):
    start_time = pygame.time.get_ticks()
    while True:
        screen.fill((255, 255, 255))           # was dark red / dark blue

        if missed:
            draw_text(screen, "ENEMY MISSED!", 70,
                      WIDTH // 2, 300, (200, 140, 0), True)

            draw_text(screen, "You avoided the attack!", 45,
                      WIDTH // 2, 420, (30, 30, 30), True)

        else:
            draw_text(screen, "ENEMY ATTACK!", 70,
                      WIDTH // 2, 300, (30, 30, 30), True)

            draw_text(screen, f"-{damage} HP", 70,
                      WIDTH // 2, 420, (180, 30, 30), True)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        if pygame.time.get_ticks() - start_time >= 2000:
            return


def win_screen(screen, coins):
    COIN_TEXT_Y = int(HEIGHT * 0.37)   # <-- move up/down: smaller = higher, bigger = lower
    COIN_TEXT_SIZE = 80

    bg = load_image("pictures/player_won.png", (WIDTH, HEIGHT))
    if bg:
        screen.blit(bg, (0, 0))
    else:
        screen.fill((20, 70, 30))      # fallback if the picture is missing

    # gold text with a dark outline so it's readable on the picture
    font = pygame.font.Font(None, COIN_TEXT_SIZE)
    text = f"+{coins} COINS"
    gold = font.render(text, True, (255, 215, 60))
    outline = font.render(text, True, (60, 30, 5))
    cx = WIDTH // 2
    for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, -2), (-2, 2), (2, 2)]:
        screen.blit(outline, outline.get_rect(center=(cx + dx, COIN_TEXT_Y + dy)))
    screen.blit(gold, gold.get_rect(center=(cx, COIN_TEXT_Y)))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    click.play()
                    return

def hospital_screen(screen, seconds):
    clock = pygame.time.Clock()

    # ---- adjust these to move the timer on the plank ----
    TIMER_X = int(WIDTH * 0.518)      # horizontal center of the plain wood
    TIMER_Y = int(HEIGHT * 0.175)     # vertical center of the plain wood
    TIMER_SIZE = 95
    TIMER_COLOR = (255, 240, 200)     # light cream so it stands out on the wood
    OUTLINE_COLOR = (60, 30, 10)

    bg = load_image("pictures/hospital.png", (WIDTH, HEIGHT))
    font = pygame.font.Font(None, TIMER_SIZE)

    start_time = pygame.time.get_ticks()
    while True:
        elapsed_ms = pygame.time.get_ticks() - start_time
        remaining = (seconds * 1000 - elapsed_ms + 999) // 1000   # counts down 30, 29, ... 1
        if remaining <= 0:
            break

        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((230, 230, 230))
            draw_text(screen, "HOSPITAL", 80, WIDTH // 2, 220, (30, 30, 30), True)

        # timer text with a dark outline so it's easy to read on the wood
        text = f"{remaining}s"
        main = font.render(text, True, TIMER_COLOR)
        outline = font.render(text, True, OUTLINE_COLOR)
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, -2), (-2, 2), (2, 2)]:
            screen.blit(outline, outline.get_rect(center=(TIMER_X + dx, TIMER_Y + dy)))
        screen.blit(main, main.get_rect(center=(TIMER_X, TIMER_Y)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(30)

    screen.fill((30, 30, 30))
    draw_text(screen, "RECOVERED!", 70, WIDTH // 2, HEIGHT // 2, (255, 255, 255), True)
    pygame.display.update()
    pygame.time.delay(1000)

def defeat_choice_screen(screen, level, game_data):
    fee = LOSS_FEE[level]
    hospital_seconds = LEVEL_DATA[level]["hospital"]
    clock = pygame.time.Clock()

    # ---- adjust these to move things on the parchment ----
    CHOICE1_Y = int(HEIGHT * 0.52)
    CHOICE2_Y = int(HEIGHT * 0.62)
    COINS_Y   = int(HEIGHT * 0.72)
    MESSAGE_Y = int(HEIGHT * 0.79)
    TEXT_COLOR = (70, 25, 15)          # dark brown to match the picture

    bg = load_image("pictures/player_lost.png", (WIDTH, HEIGHT))

    message = ""
    message_time = 0

    while True:
        if bg:
            screen.blit(bg, (0, 0))
        else:
            # fallback if the picture is missing
            screen.fill((230, 230, 230))
            draw_text(screen, "YOU LOST!", 90, WIDTH // 2, 170, (150, 30, 30), True)
            draw_text(screen, "Choose what to do:", 50, WIDTH // 2, 270, (30, 30, 30), True)

        draw_text(screen, f"1. Lose {fee} coins (no waiting)", 55,
                  WIDTH // 2, CHOICE1_Y, TEXT_COLOR, True)
        draw_text(screen, f"2. Stay in the hospital ({hospital_seconds}s)", 55,
                  WIDTH // 2, CHOICE2_Y, TEXT_COLOR, True)

        draw_text(screen, f"Your coins: {game_data['coins']}", 45,
                  WIDTH // 2, COINS_Y, TEXT_COLOR, True)

        if message and pygame.time.get_ticks() - message_time < 1500:
            draw_text(screen, message, 50, WIDTH // 2, MESSAGE_Y, (180, 30, 30), True)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # OPTION 1: PAY COINS
                if event.key in (pygame.K_1, pygame.K_KP1):
                    if game_data["coins"] >= fee:
                        click.play()
                        game_data["coins"] -= fee

                        screen.fill((30, 30, 30))
                        draw_text(screen, f"-{fee} COINS", 80,
                                  WIDTH // 2, 380, (255, 215, 0), True)
                        draw_text(screen, "Returning to level selection...", 40,
                                  WIDTH // 2, 470, (255, 255, 255), True)
                        pygame.display.update()
                        pygame.time.delay(1500)
                        return
                    else:
                        message = "NOT ENOUGH COINS!"
                        message_time = pygame.time.get_ticks()

                # OPTION 2: HOSPITAL
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    click.play()
                    hospital_screen(screen, hospital_seconds)
                    return


def start_battle(
    screen,
    level,
    game_data
):
    stats = LEVEL_DATA[level]

    # 1. PLACE
    # Automatically shown for 2 seconds
    continue_game = place_screen(screen, level)
    if not continue_game:
        return


    # 2. GET POKEMON
    player_hp = stats["hp"]
    enemy_hp = stats["hp"]
    pokemon_image, pokemon_name = get_pokemon(level)


    # 3. ENEMY INTRO
    # White background
    # Enemy in middle
    # 2 seconds
    continue_game = enemy_intro_screen(
        screen,
        pokemon_image,
        pokemon_name
    )
    if not continue_game:
        return

    # BATTLE LOOP
    while player_hp > 0 and enemy_hp > 0:


        # 4. MATCH INTERFACE
        # 3 seconds
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


        # 5. SLOT MACHINE
        # SPACE = START
        # SPACE = STOP
        attack = slot_machine(screen)

        if attack is None:
            return


        # 6. CALCULATE PLAYER DAMAGE
        if attack == 3:
            damage = random.randint(stats["three_combi"][0], stats["three_combi"][1])
        elif attack == 2:
            damage = random.randint(stats["two_combi"][0], stats["two_combi"][1])
        else:
            damage = 0

        enemy_hp -= damage

        if enemy_hp < 0:
            enemy_hp = 0

        # 8. PLAYER ATTACK POINTS
        # 2 seconds
        player_attack_screen(
            screen,
            attack,
            damage
        )


        # 9. CHECK IF ENEMY IS DEAD
        if enemy_hp <= 0:
            match_bg.stop()  # STOP on win
            coins = stats["coins"]
            game_data["coins"] += coins
            win_screen(screen, coins)
            return True


        # 10. MATCH INTERFACE AGAIN
        # 3 seconds
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

        # 11. ENEMY ATTACK
        # 30% chance that the enemy misses
        if random.random() < 0.30:
            enemy_damage = 0
            enemy_missed = True
        else:
            enemy_damage = random.randint(
                stats["enemy_attack"][0],
                stats["enemy_attack"][1]
            )
            enemy_missed = False

        # Apply damage only if the enemy hits
        player_hp -= enemy_damage

        if player_hp < 0:
            player_hp = 0

        # 12. ENEMY ATTACK POINTS
        # 2 seconds
        enemy_attack_screen(
            screen,
            enemy_damage,
            enemy_missed
        )

        # 13. CHECK IF PLAYER IS DEAD
        if player_hp <= 0:
            match_bg.stop()  # STOP on lose
            defeat_choice_screen(screen, level, game_data)
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

def world1(screen, game_data):
    if "world1_unlocked" not in game_data:
        game_data["world1_unlocked"] = 1

    while True:
        level = level_selection(screen, game_data, "world1_unlocked", "mac", 1)

        # World 1 finished (works for real wins and for the mac5 cheat)
        if 5 in game_data.get("world1_cleared", []):
            game_data["world2_unlocked"] = max(1, game_data.get("world2_unlocked", 0))

        if level is None:
            return

        continue_game = instruction_screen(screen)
        if not continue_game:
            return

        # ---------- PLAY: after the instructions ----------
        match_bg.play(-1)

        result = start_battle(screen, level, game_data)

        # ---------- STOP: safety net (e.g. ESC out of the match) ----------
        match_bg.stop()

        if result is True:
            mark_cleared(game_data, 'world1_unlocked', level)
            if level == game_data['world1_unlocked']:
                if game_data['world1_unlocked'] < 5:
                    game_data['world1_unlocked'] += 1
