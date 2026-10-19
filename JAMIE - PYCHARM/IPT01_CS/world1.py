import pygame
import sys
import random
import requests
from io import BytesIO
from level_menu import level_selection, mark_cleared
from pokemon_book import record_defeat
pygame.mixer.init()

WIDTH = 1510
HEIGHT = 890
click = pygame.mixer.Sound("music/click.mp3")
# Level settings
LEVEL_DATA = {
    1: {"hp": 100, "two_combi": (20, 30), "three_combi": (25, 30), "enemy_attack": (20, 30), "coins": 100, "hospital": 30},
    2: {"hp": 120, "two_combi": (30, 40), "three_combi": (35, 40), "enemy_attack": (30, 40), "coins": 110, "hospital": 30},
    3: {"hp": 140, "two_combi": (40, 50), "three_combi": (45, 50), "enemy_attack": (40, 50), "coins":  120, "hospital": 30},
    4: {"hp": 160, "two_combi": (50, 60), "three_combi": (55, 60), "enemy_attack": (50, 60), "coins": 130, "hospital": 30},
    5: {"hp": 180, "two_combi": (60, 70), "three_combi": (65, 70), "enemy_attack": (60, 70), "coins": 150, "hospital": 40}
}

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
def battle_interface(
    screen,
    level,
    player_hp,
    enemy_hp,
    max_enemy_hp,
    pokemon_image,
    pokemon_name
):
    # Light gray background like World 2.
    screen.fill((235, 235, 235))

    # ENEMY INFORMATION - TOP RIGHT
    draw_text(
        screen,
        f"{pokemon_name} - LEVEL {level}",
        38,
        1050,
        55,
        (30, 30, 30)
    )

    draw_health_bar(
        screen,
        1050,
        105,
        330,
        30,
        enemy_hp,
        max_enemy_hp
    )

    draw_text(
        screen,
        f"HP: {enemy_hp}/{max_enemy_hp}",
        30,
        1050,
        145,
        (30, 30, 30)
    )


    # ENEMY POKEMON - RIGHT SIDE
    if pokemon_image:
        screen.blit(
            pokemon_image,
            (1030, 180)
        )

    draw_text(
        screen,
        "VS",
        70,
        WIDTH // 2,
        390,
        (30, 30, 30),
        center=True
    )

    # PLAYER INFORMATION - BOTTOM LEFT
    draw_text(
        screen,
        "PLAYER",
        42,
        100,
        610,
        (30, 30, 30))

    draw_health_bar(
        screen,
        100,
        670,
        330,
        30,
        player_hp,
        max_enemy_hp)

    draw_text(
        screen,
        f"HP: {player_hp}/{max_enemy_hp}",
        30,
        100,
        710,
        (30, 30, 30))

    pygame.display.update()


# PLACE SCREEN
# Automatically continues after 2 seconds
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
                (0, 0))
        else:
            screen.fill(
                (30, 30, 30))

            draw_text(
                screen,
                "PLACE 1",
                70,
                650,
                300)

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
        if pygame.time.get_ticks() - start_time >= 1500:
            return True



# ENEMY INTRO SCREEN
# White background + enemy in middle
# 2 seconds

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
            (25, 25, 30)
        )
        # Title
        title = title_font.render(
            "FOES & GOALS",
            True,
            (255, 255, 255))

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


def player_attack_screen(
    screen,
    attack,
    damage
):

    start_time = pygame.time.get_ticks()
    while True:
        screen.fill(
            (20, 30, 20))

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



def enemy_attack_screen(screen, damage, missed=False):
    start_time = pygame.time.get_ticks()
    while True:
        if missed:
            screen.fill((30, 30, 50))
            draw_text(
                screen,
                "ENEMY MISSED!",
                70,
                WIDTH // 2,
                300,
                (255, 215, 0),
                center=True
            )

            draw_text(
                screen,
                "You avoided the attack!",
                45,
                WIDTH // 2,
                420,
                (255, 255, 255),
                center=True
            )

        else:
            screen.fill((40, 15, 15))

            draw_text(
                screen,
                "ENEMY ATTACK!",
                70,
                WIDTH // 2,
                300,
                center=True
            )

            draw_text(
                screen,
                f"-{damage} HP",
                70,
                WIDTH // 2,
                420,
                center=True
            )

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
                    click.play()
                    return

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


def start_battle(
    screen,
    level,
    game_data
):
    stats = LEVEL_DATA[level]

    # 1. PLACE
    # Automatically shown for 2 seconds
    continue_game = place_screen(screen)
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


        # 7. YOUR ATTACK ANIMATION
        attack_animation_placeholder(
            screen,
            attack,
            damage
        )

        # 8. PLAYER ATTACK POINTS
        # 2 seconds
        player_attack_screen(
            screen,
            attack,
            damage
        )


        # 9. CHECK IF ENEMY IS DEAD
        if enemy_hp <= 0:
            coins = stats["coins"]
            game_data["coins"] += coins
            record_defeat(game_data, pokemon_name, 1, level)
            win_screen(
                screen,
                coins
            )
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

        level = level_selection(screen, game_data, "world1_unlocked", "mac",1)

        if level is None:
            return

        # ---------------------------------------------
        # INSTRUCTIONS
        # ---------------------------------------------

        continue_game = instruction_screen(screen)

        if not continue_game:
            return


        result = start_battle(screen, level, game_data)

        if result is True:
            mark_cleared(game_data, 'world1_unlocked', level)
            if level == game_data['world1_unlocked']:
                if game_data['world1_unlocked'] < 5:
                    game_data['world1_unlocked'] += 1
