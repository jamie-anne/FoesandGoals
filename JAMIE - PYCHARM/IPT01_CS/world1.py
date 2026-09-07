import os
import time
import random
import msvcrt

from hearts import (
    format_hearts_bar,
    update_hearts,
    lose_heart,
    has_hearts,
)


def clear_screen():
    os.system("cls")


def show_world1_title():
    print("""
==============================================================
                     WORLD 1 - LAND
                      SLOT ATTACK
==============================================================
""")


# ==============================================================
# SLOT ATTACK
# ==============================================================

def slot_attack(speed, double_damage_range, triple_damage_range):

    symbols = ["⚔️", "🔫", "💣"]

    clear_screen()

    print("""
==============================================================
                     WORLD 1 - LAND
                      SLOT ATTACK
==============================================================

                    WILD ENEMY

==============================================================
""")

    print("""
                  Press SPACE to spin!

==============================================================
""")

    input("Press ENTER to start...")

    # ==========================================================
    # SPINNING
    # ==========================================================

    slot1 = random.choice(symbols)
    slot2 = random.choice(symbols)
    slot3 = random.choice(symbols)

    frame_interval = speed / 10
    poll_interval = 0.01

    while True:

        clear_screen()

        print("""
==============================================================
                     WORLD 1 - LAND
                      SLOT ATTACK
==============================================================

                    WILD ENEMY

==============================================================
""")

        print(f"""
                    {slot1}     {slot2}     {slot3}

==============================================================

                 Press SPACE to STOP!

==============================================================
""")

        # Poll for SPACE while THIS frame is still on screen,
        # instead of only checking once right before it changes.
        stopped = False
        waited = 0.0

        while waited < frame_interval:

            if msvcrt.kbhit():

                key = msvcrt.getch()

                if key == b" ":
                    stopped = True
                    break

            time.sleep(poll_interval)
            waited += poll_interval

        if stopped:
            break

        # Only now move on to the next frame's symbols
        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)

    # ==========================================================
    # RESULT
    # ==========================================================

    clear_screen()

    print("""
==============================================================
                       RESULT!
==============================================================
""")

    print(f"""
                    {slot1}     {slot2}     {slot3}
""")

    print("""
==============================================================
""")

    # ==========================================================
    # CHECK COMBINATION
    # ==========================================================

    if slot1 == slot2 == slot3:

        damage = random.randint(*triple_damage_range)

        print(f"""
                    TRIPLE COMBO!

                       MASSIVE HIT!
                       DAMAGE: {damage}
""")

    elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:

        damage = random.randint(*double_damage_range)

        print(f"""
                    DOUBLE COMBO!

                       GOOD HIT!
                       DAMAGE: {damage}
""")

    else:

        damage = 0

        print("""
                    NO COMBO!

                       MISS!
                       DAMAGE: 0
""")

    print("""
==============================================================
""")

    input("Press ENTER to continue...")

    return damage


# ==============================================================
# ENEMY ATTACK
# ==============================================================

def enemy_attack(enemy_min_damage, enemy_max_damage):
    damage = random.randint(enemy_min_damage, enemy_max_damage)

    clear_screen()

    print("""
==============================================================
                      ENEMY'S TURN
==============================================================

                    WILD ENEMY ATTACKS!
==============================================================
""")

    print(f"                 Enemy dealt {damage} damage!")

    input("\nPress ENTER to continue...")

    return damage


# ==============================================================
# PLAY LEVEL
# ==============================================================

def play_level(
        player_data,
        level_number,
        player_max_hp,
        enemy_max_hp,
        speed,
        double_damage_range,
        triple_damage_range,
        enemy_min_damage,
        enemy_max_damage
):
    player_hp = player_max_hp
    enemy_hp = enemy_max_hp

    while player_hp > 0 and enemy_hp > 0:

        # =========================
        # PLAYER'S TURN
        # =========================

        clear_screen()

        print(f"""
==============================================================
                     WORLD 1 - LEVEL {level_number}
==============================================================

                    {format_hearts_bar(player_data)}

                    YOUR HP:   {player_hp}/{player_max_hp}
                    ENEMY HP:  {enemy_hp}/{enemy_max_hp}

==============================================================
""")

        damage = slot_attack(
            speed,
            double_damage_range,
            triple_damage_range
        )

        enemy_hp -= damage

        if enemy_hp < 0:
            enemy_hp = 0

        # Enemy defeated
        if enemy_hp <= 0:
            break

        # =========================
        # ENEMY'S TURN
        # =========================

        damage = enemy_attack(
            enemy_min_damage,
            enemy_max_damage
        )

        player_hp -= damage

        if player_hp < 0:
            player_hp = 0

    # =========================
    # BATTLE RESULT
    # =========================

    clear_screen()

    victory = player_hp > 0

    if victory:

        player_data["world1_cleared"].add(level_number)

        print(f"""
==============================================================
                         VICTORY!
==============================================================

                  You defeated the enemy!

                    LEVEL {level_number}
                    +50 COINS

==============================================================
""")

        print(f"                    YOUR HP: {player_hp}/{player_max_hp}")
        player_data["coins"] += 50

    else:

        lose_heart(player_data)
        update_hearts(player_data)

        print(f"""
==============================================================
                         DEFEATED
==============================================================

                  You lost Level {level_number}.

                    Better luck next time!

                    {format_hearts_bar(player_data)}

==============================================================
""")

    input("\nPress ENTER to continue...")

    return victory


LEVEL_CONFIGS = {
    1: dict(player_max_hp=100, enemy_max_hp=100, speed=2.50,
            double_damage_range=(15, 20), triple_damage_range=(20, 25),
            enemy_min_damage=10, enemy_max_damage=30),
    2: dict(player_max_hp=120, enemy_max_hp=120, speed=2.30,
            double_damage_range=(20, 25), triple_damage_range=(25, 30),
            enemy_min_damage=15, enemy_max_damage=35),
    3: dict(player_max_hp=150, enemy_max_hp=150, speed=2.00,
            double_damage_range=(25, 30), triple_damage_range=(30, 35),
            enemy_min_damage=20, enemy_max_damage=40),
    4: dict(player_max_hp=170, enemy_max_hp=170, speed=1.75,
            double_damage_range=(30, 35), triple_damage_range=(35, 40),
            enemy_min_damage=30, enemy_max_damage=50),
    5: dict(player_max_hp=200, enemy_max_hp=200, speed=1.30,
            double_damage_range=(40, 45), triple_damage_range=(45, 50),
            enemy_min_damage=40, enemy_max_damage=60),
}


def is_level_unlocked(player_data, level_number):
    if level_number == 1:
        return True
    return (level_number - 1) in player_data["world1_cleared"]


def attempt_level(player_data, level_number):
    if not is_level_unlocked(player_data, level_number):
        print("\nThis level is LOCKED! Clear the previous level first.")
        input("Press ENTER to continue...")
        return

    update_hearts(player_data)

    if not has_hearts(player_data):
        print("\nOut of hearts! Come back later.")
        input("Press ENTER to continue...")
        return

    play_level(player_data, level_number, **LEVEL_CONFIGS[level_number])


def world1_menu(player_data):

    while True:

        clear_screen()
        show_world1_title()

        update_hearts(player_data)

        print(format_hearts_bar(player_data))
        print()

        for level_number in range(1, 6):
            if is_level_unlocked(player_data, level_number):
                cleared_tag = " (CLEARED)" if level_number in player_data["world1_cleared"] else ""
                print(f"[{level_number}] LEVEL {level_number}{cleared_tag}")
            else:
                print(f"[{level_number}] LEVEL {level_number} - LOCKED")

        print("[6] BACK")

        print("\n==============================================================")

        choice = input("Enter your choice: ")

        if choice in ("1", "2", "3", "4", "5"):
            attempt_level(player_data, int(choice))

        elif choice == "6":
            break

        else:
            print("\nInvalid choice!")
            input("Press ENTER to continue...")