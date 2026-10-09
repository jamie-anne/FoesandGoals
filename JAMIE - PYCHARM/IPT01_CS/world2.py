import pygame
import sys
import random
import string
import requests
from io import BytesIO
from level_menu import level_selection, mark_cleared

WIDTH = 1510
HEIGHT = 890

LEVEL_DATA = {
    1: {'hp': 160, 'characters': 5, 'memorize_time': 5, 'damage': {5: 40, 4: 30, 3: 20, 2: 10, 1: 5, 0: 0},'enemy_attack': (20, 40), 'coins': 200, 'hospital':40},
    2: {'hp': 170, 'characters': 6, 'memorize_time': 6,'damage': {6: 40, 5: 30, 4: 20, 3: 20, 2: 10, 1: 10, 0: 0},'enemy_attack': (30, 40), 'coins': 220, 'hospital':40},
    3: {'hp': 180, 'characters': 7, 'memorize_time': 7,'damage': {7: 50, 6: 45, 5: 40, 4: 35, 3: 30, 2: 20, 1: 20, 0: 0},'enemy_attack': (40, 50), 'coins': 240, 'hospital':40},
    4: {'hp': 190, 'characters': 8, 'memorize_time': 8,'damage': {8: 70, 7: 65, 6: 60, 5: 50, 4: 45, 3: 40, 2: 35, 1: 30, 0: 0},'enemy_attack': (60, 70), 'coins': 260, 'hospital':40},
    5: {'hp': 200, 'characters': 8, 'memorize_time': 7,'damage': {8: 75, 7: 65, 6: 60, 5: 50, 4: 45, 3: 40, 2: 35, 1: 30, 0: 0},'enemy_attack': (60, 75), 'coins': 300, 'hospital':50}
}

# World 2 locations (levels 1-5). Coordinates are used for live weather.
LOCATION_DATA = {
    1: {"name": "Baguio City", "latitude": 16.4023, "longitude": 120.5960},
    2: {"name": "Vigan, Ilocos Sur", "latitude": 17.5747, "longitude": 120.3869},
    3: {"name": "Banaue Rice Terraces", "latitude": 16.9190, "longitude": 121.0590},
    4: {"name": "Mayon Volcano, Albay", "latitude": 13.2570, "longitude": 123.6850},
    5: {"name": "Chocolate Hills, Bohol", "latitude": 9.8290, "longitude": 124.1650},
}

# Water/ice-themed Pokémon pools selected from the location's current weather.
WEATHER_POKEMON_POOLS = {
    "clear": ["squirtle", "seel", "lapras", "spheal", "wingull"],
    "cloudy": ["slowpoke", "shellder", "lapras", "wingull", "psyduck"],
    "fog": ["slowpoke", "seel", "snorunt", "spheal", "swinub"],
    "rain": ["squirtle", "psyduck", "shellder", "wingull", "chinchou"],
    "storm": ["lapras", "wingull", "psyduck", "chinchou", "shellder"],
    "snow": ["spheal", "snorunt", "swinub", "seel", "lapras"],
}


def get_weather_category(level):
    """Return the current Open-Meteo weather category for this level's place."""
    location = LOCATION_DATA[level]
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "weather_code",
                "timezone": "auto",
            },
            timeout=5,
        )
        response.raise_for_status()
        weather_code = response.json()["current"]["weather_code"]

        if weather_code in (0, 1):
            category = "clear"
        elif weather_code in (2, 3):
            category = "cloudy"
        elif weather_code in (45, 48):
            category = "fog"
        elif weather_code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
            category = "rain"
        elif weather_code in (95, 96, 99):
            category = "storm"
        elif weather_code in (71, 73, 75, 77, 85, 86):
            category = "snow"
        else:
            category = "clear"

        print(f"World 2 weather at {location['name']}: WMO {weather_code} -> {category}")
        return category
    except (requests.RequestException, KeyError, TypeError, ValueError) as error:
        print(f"Open-Meteo error for {location['name']}: {error}")
        print("World 2 fallback: using the clear-weather Pokémon pool.")
        return "clear"


def load_image(filename, size=None):
    try:
        image = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(image, size) if size else image
    except pygame.error:
        print(f'Could not load image: {filename}')
        return None


def draw_text(screen, text, size, x, y, color=(255, 255, 255), center=False):
    surface = pygame.font.Font(None, size).render(str(text), True, color)
    screen.blit(surface, surface.get_rect(center=(x, y)) if center else (x, y))


def get_pokemon(level):
    # The selected level determines the location, its live weather, and the enemy pool.
    weather_category = get_weather_category(level)
    name = random.choice(WEATHER_POKEMON_POOLS[weather_category])
    try:
        r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}', timeout=5)
        r.raise_for_status()
        data = r.json()
        url = data['sprites']['other']['official-artwork']['front_default']
        if not url:
            raise ValueError(f'No official artwork available for {name}')
        img_r = requests.get(url, timeout=5)
        img_r.raise_for_status()
        img = pygame.image.load(BytesIO(img_r.content)).convert_alpha()
        return pygame.transform.scale(img, (330, 330)), data['name'].capitalize()
    except Exception as e:
        print('PokéAPI error:', e)
        return None, name.capitalize()



def instruction_screen(screen):
    image = load_image('pictures/instruction_world1.png', (WIDTH, HEIGHT))
    while True:
        if image:
            screen.blit(image, (0,0))
        else:
            screen.fill((20,20,20))
            draw_text(screen, 'WORLD 2', 70, WIDTH//2, 250, center=True)
            draw_text(screen, 'MEMORIZE THE CHARACTERS', 45, WIDTH//2, 370, center=True)
            draw_text(screen, 'Press ENTER to continue', 40, WIDTH//2, 470, center=True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return True
                if event.key == pygame.K_ESCAPE: return False



def place_screen(screen, level):
    place_number = level + 5
    image = load_image(
        f'pictures/places_{place_number}.png',
        (WIDTH, HEIGHT)
    )

    if image:
        screen.blit(image, (0, 0))
    else:
        screen.fill((30, 30, 30))
        draw_text(
            screen,
            f'WORLD 2 - PLACE {place_number}',
            70,
            WIDTH // 2,
            HEIGHT // 2,
            center=True
        )

    pygame.display.update()
    pygame.time.delay(1500)



def enemy_intro_screen(screen, image, name):
    screen.fill((255,255,255))
    if image: screen.blit(image, (WIDTH//2-165, 120))
    draw_text(screen, name, 55, WIDTH//2, 510, (30,30,30), True)
    pygame.display.update()
    pygame.time.delay(2000)


def draw_health_bar(screen, x, y, width, height, hp, max_hp):
    pygame.draw.rect(screen, (60,60,60), (x,y,width,height))
    pct = max(0, min(1, hp/max_hp))
    pygame.draw.rect(screen, (40,200,70), (x,y,int(width*pct),height))
    pygame.draw.rect(screen, (255,255,255), (x,y,width,height), 3)


def match_interface(screen, level, player_hp, enemy_hp, max_hp, enemy_image, enemy_name):
    screen.fill((235,235,235))
    draw_text(screen, f'{enemy_name} - LEVEL {level}', 38, 1050, 55, (30,30,30))
    draw_health_bar(screen, 1050, 105, 330, 30, enemy_hp, max_hp)
    draw_text(screen, f'HP: {enemy_hp}/{max_hp}', 30, 1050, 145, (30,30,30))
    if enemy_image: screen.blit(enemy_image, (1030,180))
    draw_text(screen, 'VS', 70, WIDTH//2, 390, (30,30,30), True)
    draw_text(screen, 'PLAYER', 42, 100, 610, (30,30,30))
    draw_health_bar(screen, 100, 670, 330, 30, player_hp, max_hp)
    draw_text(screen, f'HP: {player_hp}/{max_hp}', 30, 100, 710, (30,30,30))
    draw_text(screen, 'WORLD 2', 32, WIDTH//2, 830, (30,30,30), True)
    pygame.display.update()


def generate_sequence(amount):
    chars = string.ascii_letters + string.digits + '!@#$%&*?+-='
    return [random.choice(chars) for _ in range(amount)]


def draw_character_boxes(screen, values, y, active_index=None, box_size=75):
    gap = 15
    total = len(values)*box_size + (len(values)-1)*gap
    start = WIDTH//2 - total//2
    for i, value in enumerate(values):
        x = start + i*(box_size+gap)
        border = (255,215,0) if i == active_index else (30,30,30)
        width = 5 if i == active_index else 3
        pygame.draw.rect(screen, (255,255,255), (x,y,box_size,box_size))
        pygame.draw.rect(screen, border, (x,y,box_size,box_size), width)
        if value:
            draw_text(screen, value, 48, x+box_size//2, y+box_size//2, (30,30,30), True)


def memory_game(screen, level):
    stats = LEVEL_DATA[level]
    amount = stats['characters']
    sequence = generate_sequence(amount)

    # Memorize phase with visible countdown.
    start = pygame.time.get_ticks()
    while True:
        elapsed = (pygame.time.get_ticks()-start)/1000
        remaining = stats['memorize_time'] - int(elapsed)
        if remaining <= 0: break
        screen.fill((235,235,235))
        draw_text(screen, 'MEMORIZE!', 60, WIDTH//2, 145, (30,30,30), True)
        draw_text(screen, f'Time: {remaining}', 40, WIDTH//2, 220, (30,30,30), True)
        draw_character_boxes(screen, sequence, 350)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return None, None

    # Input phase: one character per box.
    user = [''] * amount
    current = 0
    message = ''
    while True:
        screen.fill((235,235,235))
        draw_text(screen, 'TYPE THE SEQUENCE', 55, WIDTH//2, 145, (30,30,30), True)
        draw_text(screen, 'Type one character per box', 32, WIDTH//2, 210, (30,30,30), True)
        draw_character_boxes(screen, user, 350, current if current < amount else None)
        if message: draw_text(screen, message, 32, WIDTH//2, 500, (180,30,30), True)
        draw_text(screen, 'ENTER = Submit   BACKSPACE = Delete   ESC = Back', 28, WIDTH//2, 600, (50,50,50), True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type != pygame.KEYDOWN: continue
            if event.key == pygame.K_ESCAPE: return None, None
            if event.key == pygame.K_BACKSPACE:
                if current > 0:
                    current -= 1; user[current] = ''
                message = ''
                continue
            if event.key == pygame.K_RETURN:
                if current < amount:
                    message = 'Please complete all boxes.'
                    continue
                correct = sum(user[i] == sequence[i] for i in range(amount))
                return correct, stats['damage'][correct]
            if event.unicode and event.unicode.isprintable() and current < amount:
                user[current] = event.unicode
                current += 1
                message = ''


def player_attack_screen(screen, correct, total, damage):
    screen.fill((235,235,235))
    draw_text(screen, 'PLAYER ATTACK!', 70, WIDTH//2, 260, (30,30,30), True)
    draw_text(screen, f'CORRECT: {correct}/{total}', 55, WIDTH//2, 365, (30,30,30), True)
    draw_text(screen, f'DAMAGE: {damage}', 65, WIDTH//2, 455, (180,30,30), True)
    pygame.display.update()
    pygame.time.delay(1500)


def enemy_attack_screen(screen, damage):
    screen.fill((235,235,235))
    draw_text(screen, 'ENEMY ATTACK!', 70, WIDTH//2, 300, (30,30,30), True)
    draw_text(screen, f'DAMAGE: {damage}', 65, WIDTH//2, 410, (180,30,30), True)
    pygame.display.update()
    pygame.time.delay(1500)


def result_screen(screen, title, subtitle, title_color=(30,30,30)):
    screen.fill((235,235,235))
    draw_text(screen, title, 80, WIDTH//2, 320, title_color, True)
    draw_text(screen, subtitle, 50, WIDTH//2, 430, (30,30,30), True)
    draw_text(screen, 'Press ENTER to continue', 35, WIDTH//2, 540, (30,30,30), True)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE): return


def hospital_screen(screen, seconds):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        remaining = seconds - elapsed

        if remaining <= 0:
            break

        screen.fill((230, 230, 230))

        draw_text(
            screen, "HOSPITAL", 80,
            WIDTH // 2, 220, (30, 30, 30), True
        )

        draw_text(
            screen, "YOU LOST!", 60,
            WIDTH // 2, 340, (180, 30, 30), True
        )

        draw_text(
            screen, f"Recovery Time: {remaining}s", 45,
            WIDTH // 2, 450, (30, 30, 30), True
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(30)

    screen.fill((30, 30, 30))

    draw_text(
        screen, "RECOVERED!", 70,
        WIDTH // 2, 350, (255, 255, 255), True
    )

    draw_text(
        screen, "Returning to level selection...", 35,
        WIDTH // 2, 440, (255, 255, 255), True
    )

    pygame.display.update()
    pygame.time.delay(1500)

def start_battle(screen, level, game_data):
    stats = LEVEL_DATA[level]
    player_hp = stats['hp']
    enemy_hp = stats['hp']

    place_screen(screen, level)
    enemy_image, enemy_name = get_pokemon(level)
    enemy_intro_screen(screen, enemy_image, enemy_name)

    while player_hp > 0 and enemy_hp > 0:
        match_interface(screen, level, player_hp, enemy_hp, stats['hp'], enemy_image, enemy_name)
        pygame.time.delay(2000)

        correct, damage = memory_game(screen, level)
        if correct is None: return False

        enemy_hp = max(0, enemy_hp - damage)
        player_attack_screen(screen, correct, stats['characters'], damage)

        if enemy_hp <= 0:
            game_data['coins'] += stats['coins']
            result_screen(screen, 'YOU WIN!', f"+{stats['coins']} COINS")
            return True

        match_interface(screen, level, player_hp, enemy_hp, stats['hp'], enemy_image, enemy_name)
        pygame.time.delay(2000)

        enemy_damage = random.randint(*stats['enemy_attack'])
        player_hp = max(0, player_hp - enemy_damage)
        enemy_attack_screen(screen, enemy_damage)

        if player_hp <= 0:
            hospital_screen(screen, stats['hospital'])
            return False

    return False


def world2(screen, game_data):
    if 'world2_unlocked' not in game_data:
        game_data['world2_unlocked'] = 1

    while True:
        level = level_selection(screen, game_data, 'world2_unlocked', 'evo',2)
        if level is None: return

        if not instruction_screen(screen): return

        result = start_battle(screen, level, game_data)
        if result is True:
            mark_cleared(game_data, 'world2_unlocked', level)
            if level == game_data['world2_unlocked']:
                if game_data['world2_unlocked'] < 5:
                    game_data['world2_unlocked'] += 1
