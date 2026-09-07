import os
import time
import msvcrt
import random

from hearts import (
    format_hearts_bar,
    update_hearts,
    lose_heart,
    has_hearts,
)


def clear_screen():
    os.system("cls")


def show_world3_title():
    print("""
==============================================================
                     WORLD 3 - LAND
                     TIMING CHALLENGE
==============================================================
""")


def show_battle_status(player_hp, enemy_hp):
    print(f"""
==============================================================
                         BATTLE
==============================================================

                    YOUR HP:   {player_hp}/150
                    ENEMY HP:  {enemy_hp}/150

==============================================================
""")


def timing_attack(speed, critical_damage, normal_damage):
    bar_length = 21

    travel_time = speed

    start_time = time.perf_counter()

    while True:
        elapsed = time.perf_counter() - start_time

        cycle_time = travel_time * 2
        current_time = elapsed % cycle_time

        if current_time <= travel_time:
            progress = current_time / travel_time
        else:
            progress = 2 - (current_time / travel_time)

        position = round(progress * (bar_length - 1))

        clear_screen()

        print("""
==============================================================
                     YOUR TURN
==============================================================

                    WILD PIKACHU
==============================================================

                 Press SPACE to attack!

==============================================================
""")

        bar = ["-"] * bar_length

        for i in range(5, 9):
            bar[i] = "-"

        for i in range(12, 16):
            bar[i] = "-"

        for i in range(9, 12):
            bar[i] = "-"

        bar[position] = "^"

        print("              " + "".join(bar))

        print("==============================================================")
        print("                      PRESS [SPACE]")
        print("==============================================================")

        if msvcrt.kbhit():
            key = msvcrt.getch()

            if key == b" ":
                break

        time.sleep(0.005)

    # Determine damage
    if 9 <= position <= 11:
        result = "CRITICAL HIT!"
        damage = critical_damage

    elif 5 <= position <= 8 or 12 <= position <= 15:
        result = "NORMAL HIT!"
        damage = normal_damage

    else:
        result = "MISS!"
        damage = 0

    clear_screen()

    print("""
==============================================================
                         ATTACK!
==============================================================
""")

    print(f"                    {result}")
    print(f"                    DAMAGE: {damage}")

    print("""
==============================================================
""")

    input("Press ENTER to continue...")

    return damage


def enemy_attack(enemy_min_damage, enemy_max_damage):
    damage = random.randint(enemy_min_damage, enemy_max_damage)

    clear_screen()

    print("""
==============================================================
                      ENEMY'S TURN
==============================================================

                    WILD PIKACHU ATTACKS!
==============================================================
""")

    print(f"                 Enemy dealt {damage} damage!")

    input("\nPress ENTER to continue...")

    return damage


def play_level(
        player_data,
        level_number,
        player_max_hp,
        enemy_max_hp,
        speed,
        enemy_min_damage,
        enemy_max_damage,
        critical_damage,
        normal_damage
):
    player_hp = player_max_hp
    enemy_hp = enemy_max_hp

    while player_hp > 0 and enemy_hp > 0:

        clear_screen()

        print(f"""
==============================================================
                     WORLD 3 - LEVEL {level_number}
==============================================================

                    {format_hearts_bar(player_data)}

                    YOUR HP:   {player_hp}/{player_max_hp}
                    ENEMY HP:  {enemy_hp}/{enemy_max_hp}

==============================================================
""")

        damage = timing_attack(
            speed,
            critical_damage,
            normal_damage
        )

        enemy_hp -= damage

        if enemy_hp < 0:
            enemy_hp = 0

        # Enemy defeated
        if enemy_hp <= 0:
            break


        damage = enemy_attack(
            enemy_min_damage,
            enemy_max_damage
        )

        player_hp -= damage

        if player_hp < 0:
            player_hp = 0


    clear_screen()

    victory = player_hp > 0

    if victory:

        player_data["world3_cleared"].add(level_number)

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
    1: dict(player_max_hp=100, enemy_max_hp=100, speed=2.00,
            enemy_min_damage=10, enemy_max_damage=30,
            critical_damage=30, normal_damage=20),
    2: dict(player_max_hp=120, enemy_max_hp=120, speed=2.00,
            enemy_min_damage=15, enemy_max_damage=35,
            critical_damage=35, normal_damage=25),
    3: dict(player_max_hp=150, enemy_max_hp=150, speed=1.7,
            enemy_min_damage=20, enemy_max_damage=40,
            critical_damage=40, normal_damage=35),
    4: dict(player_max_hp=170, enemy_max_hp=170, speed=1.0,
            enemy_min_damage=30, enemy_max_damage=50,
            critical_damage=50, normal_damage=35),
    5: dict(player_max_hp=200, enemy_max_hp=200, speed=0.7,
            enemy_min_damage=40, enemy_max_damage=60,
            critical_damage=60, normal_damage=45),
}


def is_level_unlocked(player_data, level_number):
    if level_number == 1:
        return True
    return (level_number - 1) in player_data["world3_cleared"]


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


def world3_menu(player_data):

    while True:

        clear_screen()
        show_world3_title()

        update_hearts(player_data)

        print(format_hearts_bar(player_data))
        print()

        for level_number in range(1, 6):
            if is_level_unlocked(player_data, level_number):
                cleared_tag = " (CLEARED)" if level_number in player_data["world3_cleared"] else ""
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