import pygame
import sys
import random
import requests
from io import BytesIO
from level_menu import level_selection, mark_cleared
from pokemon_book import record_defeat

WIDTH = 1510
HEIGHT = 890

LEVEL_DATA = {
    1: {'hp': 200,'speed': 1.0,'critical': 60,'strong': 50,'weak': 40,'miss': 0,'enemy_attack': (50, 60),'coins': 350,'hospital': 50},
    2: {'hp': 220,'speed': 1.2,'critical': 70,'strong': 55,'weak': 40,'miss': 0,'enemy_attack': (55, 70),'coins': 400,'hospital': 50},
    3: {'hp': 250,'speed':1.4,'critical': 80,'strong': 65,'weak': 50,'miss': 0,'enemy_attack': (65, 80),'coins': 450,'hospital': 50},
    4: {'hp': 270,'speed': 1.6,'critical': 90,'strong': 75,'weak': 60,'miss': 0,'enemy_attack': (75, 90),'coins': 500,'hospital': 50},
    5: {'hp': 300,'speed': 1.8,'critical': 100,'strong': 85,'weak': 65,'miss': 0,'enemy_attack': (85, 100),'coins': 1000,'hospital': 60}
}

# World 3 locations (levels 1-5). Coordinates are used for live weather.
LOCATION_DATA = {
    1: {"name": "Boracay", "latitude": 11.9674, "longitude": 121.9248},
    2: {"name": "Coron", "latitude": 11.9986, "longitude": 120.2043},
    3: {"name": "Big Lagoon, Miniloc Island", "latitude": 11.1470, "longitude": 119.3150},
    4: {"name": "Sirao Miracle Garden, Cebu", "latitude": 10.4000, "longitude": 123.8970},
    5: {"name": "General Luna, Siargao", "latitude": 9.7842, "longitude": 126.1580},
}

# Fire/lava/rock-themed Pokémon pools selected from the location's current weather.
WEATHER_POKEMON_POOLS = {
    "clear": ["charmander", "growlithe", "vulpix", "slugma", "numel"],
    "cloudy": ["ponyta", "magmar", "houndour", "torkoal", "larvitar"],
    "fog": ["slugma", "litwick", "houndour", "geodude", "numel"],
    "rain": ["geodude", "onix", "rhyhorn", "larvitar", "sandshrew"],
    "storm": ["magmar", "torkoal", "slugma", "growlithe", "heatmor"],
    "snow": ["vulpix", "ponyta", "magmar", "torkoal", "darumaka"],
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

        print(f"World 3 weather at {location['name']}: WMO {weather_code} -> {category}")
        return category
    except (requests.RequestException, KeyError, TypeError, ValueError) as error:
        print(f"Open-Meteo error for {location['name']}: {error}")
        print("World 3 fallback: using the clear-weather Pokémon pool.")
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
            draw_text(screen, 'WORLD 3', 70, WIDTH//2, 250, center=True)
            draw_text(screen, 'TIMING ATTACK', 45, WIDTH//2, 370, center=True)
            draw_text(screen, 'Press ENTER to continue', 40, WIDTH//2, 470, center=True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return True
                if event.key == pygame.K_ESCAPE: return False


def place_screen(screen, level):
    place_images = {
        1: 'pictures/places_11.png',
        2: 'pictures/places_12.png',
        3: 'pictures/places_13.png',
        4: 'pictures/places_14.png',
        5: 'pictures/places_15.png'
    }
    place_names = {
        1: 'Boracay',
        2: 'Coron',
        3: 'Big Lagoon - Miniloc Island',
        4: 'Sirao Miracle Garden',
        5: 'Siargao - General Luna, Surigao Del Norte'
    }
    image = load_image(place_images[level], (WIDTH, HEIGHT))
    if image:
        screen.blit(image, (0, 0))
    else:
        screen.fill((30, 30, 30))
        draw_text(screen, place_names[level], 55, WIDTH//2, HEIGHT//2, center=True)
    pygame.display.update()
    pygame.time.delay(2000)

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
    draw_text(screen, 'WORLD 3', 32, WIDTH//2, 830, (30,30,30), True)
    pygame.display.update()


TIMING_ZONES = [
    ('MISS', 80),
    ('WEAK HIT', 240),
    ('STRONG', 80),
    ('CRITICAL', 40),
    ('STRONG', 80),
    ('WEAK HIT', 240),
    ('MISS', 80)
]

TIMING_LINE_WIDTH = sum(
    width for _, width in TIMING_ZONES
)

TIMING_LINE_HEIGHT = 18
TIMING_MARKER_WIDTH = 7
TIMING_MARKER_HEIGHT = 100

def get_timing_result(marker_x, line_start_x):
    position = max(0, min(TIMING_LINE_WIDTH - 1, marker_x - line_start_x))
    current = 0
    for result, width in TIMING_ZONES:
        if current <= position < current + width:
            return result
        current += width
    return 'MISS'

def timing_attack(screen, level):
    stats = LEVEL_DATA[level]
    line_start_x = WIDTH // 2 - TIMING_LINE_WIDTH // 2
    line_y = 430
    marker_x = float(line_start_x)
    direction = 1
    speed = stats['speed'] * 10
    clock = pygame.time.Clock()
    colors = {'MISS': (210,210,210), 'WEAK HIT': (180,220,255), 'STRONG': (255,220,120), 'CRITICAL': (255,150,150)}
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, 0
                if event.key == pygame.K_SPACE:
                    result = get_timing_result(marker_x, line_start_x)
                    damage = {'CRITICAL': stats['critical'], 'STRONG': stats['strong'], 'WEAK HIT': stats['weak'], 'MISS': stats['miss']}[result]
                    return result, damage
        marker_x += speed * direction
        right_limit = line_start_x + TIMING_LINE_WIDTH - TIMING_MARKER_WIDTH
        if marker_x <= line_start_x:
            marker_x = line_start_x; direction = 1
        elif marker_x >= right_limit:
            marker_x = right_limit; direction = -1
        screen.fill((235,235,235))
        draw_text(screen, 'TIMING ATTACK', 60, WIDTH//2, 180, (30,30,30), True)
        draw_text(screen, 'PRESS SPACE TO STOP', 38, WIDTH//2, 245, (30,30,30), True)
        x = line_start_x
        for result, width in TIMING_ZONES:
            rect = pygame.Rect(x, line_y, width, 18)
            pygame.draw.rect(screen, colors[result], rect)
            pygame.draw.rect(screen, (30,30,30), rect, 2)
            draw_text(screen, result, 22, x + width//2, line_y + 55, (30,30,30), True)
            x += width
        pygame.draw.rect(screen, (30,30,30), (int(marker_x), line_y-45, TIMING_MARKER_WIDTH, 100))
        pygame.display.update()

def player_attack_screen(screen, result, damage):
    screen.fill((235,235,235))
    if result == 'CRITICAL':
        title, color = 'CRITICAL!', (200,30,30)
    elif result == 'STRONG':
        title, color = 'STRONG HIT!', (200,120,20)
    elif result == 'WEAK HIT':
        title, color = 'WEAK HIT!', (40,120,200)
    else:
        title, color = 'MISS!', (100,100,100)
    draw_text(screen, title, 75, WIDTH//2, 300, color, True)
    draw_text(screen, f'ATTACK POINTS: {damage}', 55, WIDTH//2, 410, (30,30,30), True)
    pygame.display.update(); pygame.time.delay(1500)

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


def start_battle(screen, level, game_data):
    stats = LEVEL_DATA[level]
    player_hp = stats['hp']
    enemy_hp = stats['hp']
    place_screen(screen, level)
    enemy_image, enemy_name = get_pokemon(level)
    enemy_intro_screen(screen, enemy_image, enemy_name)
    while player_hp > 0 and enemy_hp > 0:
        match_interface(screen, level, player_hp, enemy_hp, stats['hp'], enemy_image, enemy_name)
        pygame.time.delay(1000)
        result, damage = timing_attack(screen, level)
        if result is None:
            return False
        enemy_hp = max(0, enemy_hp - damage)
        player_attack_screen(screen, result, damage)
        if enemy_hp <= 0:
            game_data['coins'] += stats['coins']
            record_defeat(game_data, enemy_name, 3, level)
            result_screen(screen, 'YOU WIN!', f"+{stats['coins']} COINS")
            return True
        match_interface(screen, level, player_hp, enemy_hp, stats['hp'], enemy_image, enemy_name)
        pygame.time.delay(1000)
        enemy_damage = random.randint(
            stats['enemy_attack'][0],
            stats['enemy_attack'][1]
        )
        player_hp = max(0, player_hp - enemy_damage)
        enemy_attack_screen(screen, enemy_damage)
        if player_hp <= 0:
            result_screen(screen, 'YOU LOST!', f"Hospital: {stats['hospital']} seconds", (180,30,30))
            return False
        match_interface(screen, level, player_hp, enemy_hp, stats['hp'], enemy_image, enemy_name)
        pygame.time.delay(1000)
    return False

def world3(screen, game_data):
    if 'world3_unlocked' not in game_data:
        game_data['world3_unlocked'] = 1

    while True:
        level = level_selection(screen, game_data, 'world3_unlocked', 'bro',3)
        if level is None: return

        if not instruction_screen(screen): return

        result = start_battle(screen, level, game_data)

        if result is True:
            mark_cleared(game_data, 'world3_unlocked', level)
            if level == game_data['world3_unlocked']:
                if game_data['world3_unlocked'] < 5:
                    game_data['world3_unlocked'] += 1
