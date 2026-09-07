import os
import time
import random
import string

from hearts import (
    format_hearts_bar,
    update_hearts,
    lose_heart,
    has_hearts,
)


# ==============================================================
# CLEAR SCREEN
# ==============================================================

def clear_screen():
    os.system("cls")


# ==============================================================
# WORLD 2 TITLE
# ==============================================================

def show_world2_title():
    print("""
==============================================================
                     WORLD 2 - MEMORY
                    MEMORY CHALLENGE
==============================================================
""")


# ==============================================================
# GENERATE JUMBLED CODE
# ==============================================================

def generate_code(length):

    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%&*?"
    )

    return "".join(random.choice(characters) for _ in range(length))


# ==============================================================
# MEMORY CHALLENGE
# ==============================================================

def memory_challenge(sequence_length, memorize_time):

    code = generate_code(sequence_length)

    clear_screen()

    print("""
==============================================================
                         MEMORIZE!
==============================================================

                  Remember the characters:

==============================================================
""")

    print(f"                    {code}")

    print(f"""

                 You have {memorize_time} seconds.

==============================================================
""")

    # Show the code
    time.sleep(memorize_time)

    # Hide the code
    clear_screen()

    print("""
==============================================================
                       MEMORY TEST
==============================================================

                  The code has disappeared!

                  Type what you remember:

==============================================================
""")

    answer = input("                    > ")

    # Check answer
    if answer == code:

        print("""
==============================================================
                    CORRECT!
==============================================================
""")

        input("Press ENTER to continue...")

        return True

    else:

        print("""
==============================================================
                     WRONG!
==============================================================

                 That was not the correct code.

==============================================================
""")

        print(f"                  Correct code: {code}")

        input("\nPress ENTER to continue...")

        return False


# ==============================================================
# ENEMY ATTACK
# ==============================================================

def enemy_attack(enemy_min_damage, enemy_max_damage):

    damage = random.randint(
        enemy_min_damage,
        enemy_max_damage
    )

    clear_screen()

    print("""
==============================================================
                      ENEMY'S TURN
==============================================================

                    WILD PIKACHU ATTACKS!
==============================================================
""")

    print(f"""
                 Enemy dealt {damage} damage!
""")

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
        sequence_length,
        memorize_time,
        enemy_min_damage,
        enemy_max_damage,
        critical_damage,
        normal_damage
):

    player_hp = player_max_hp
    enemy_hp = enemy_max_hp

    while player_hp > 0 and enemy_hp > 0:

        # ======================================================
        # PLAYER'S TURN
        # ======================================================

        clear_screen()

        print(f"""
==============================================================
                     WORLD 2 - LEVEL {level_number}
                     MEMORY CHALLENGE
==============================================================

                    {format_hearts_bar(player_data)}

                    YOUR HP:   {player_hp}/{player_max_hp}
                    ENEMY HP:  {enemy_hp}/{enemy_max_hp}

==============================================================
                         YOUR TURN
==============================================================
""")

        correct = memory_challenge(
            sequence_length,
            memorize_time
        )

        # ======================================================
        # CORRECT ANSWER
        # ======================================================

        if correct:

            # 30% chance of critical hit
            critical = random.random() < 0.30

            if critical:

                damage = critical_damage

                clear_screen()

                print("""
==============================================================
                    CRITICAL MEMORY!
==============================================================

                       CRITICAL HIT!
==============================================================
""")

                print(f"                    DAMAGE: {damage}")

            else:

                damage = normal_damage

                clear_screen()

                print("""
==============================================================
                     GOOD MEMORY!
==============================================================

                       NORMAL HIT!
==============================================================
""")

                print(f"                    DAMAGE: {damage}")

            enemy_hp -= damage

            if enemy_hp < 0:
                enemy_hp = 0

            input("\nPress ENTER to continue...")

        # ======================================================
        # WRONG ANSWER
        # ======================================================

        else:

            clear_screen()

            print("""
==============================================================
                         MISS!
==============================================================

                  You remembered incorrectly.

                    DAMAGE: 0

==============================================================
""")

            input("Press ENTER to continue...")

        # ======================================================
        # CHECK ENEMY HP
        # ======================================================

        if enemy_hp <= 0:
            break

        # ======================================================
        # ENEMY'S TURN
        # ======================================================

        damage = enemy_attack(
            enemy_min_damage,
            enemy_max_damage
        )

        player_hp -= damage

        if player_hp < 0:
            player_hp = 0

    # ==========================================================
    # BATTLE RESULT
    # ==========================================================

    clear_screen()

    victory = player_hp > 0

    if victory:

        player_data["world2_cleared"].add(level_number)
        player_data["coins"] += 50

        print(f"""
==============================================================
                         VICTORY!
==============================================================

                  You defeated the enemy!

                    WORLD 2 - LEVEL {level_number}
                    +50 COINS

==============================================================

                    YOUR HP: {player_hp}/{player_max_hp}
                    ENEMY HP: 0/{enemy_max_hp}

==============================================================
""")

        input("Press ENTER to continue...")

        return True

    else:

        lose_heart(player_data)
        update_hearts(player_data)

        print(f"""
==============================================================
                         DEFEATED
==============================================================

                  You lost Level {level_number}.

                    {format_hearts_bar(player_data)}

==============================================================

                    YOUR HP: 0/{player_max_hp}
                    ENEMY HP: {enemy_hp}/{enemy_max_hp}

==============================================================
""")

        input("Press ENTER to continue...")

        return False


LEVEL_CONFIGS = {
    1: dict(player_max_hp=100, enemy_max_hp=100, sequence_length=4, memorize_time=3,
            enemy_min_damage=10, enemy_max_damage=30, critical_damage=30, normal_damage=20),
    2: dict(player_max_hp=120, enemy_max_hp=120, sequence_length=5, memorize_time=4,
            enemy_min_damage=15, enemy_max_damage=35, critical_damage=35, normal_damage=25),
    3: dict(player_max_hp=150, enemy_max_hp=150, sequence_length=6, memorize_time=5,
            enemy_min_damage=20, enemy_max_damage=40, critical_damage=40, normal_damage=35),
    4: dict(player_max_hp=170, enemy_max_hp=170, sequence_length=7, memorize_time=5,
            enemy_min_damage=30, enemy_max_damage=50, critical_damage=50, normal_damage=35),
    5: dict(player_max_hp=200, enemy_max_hp=200, sequence_length=8, memorize_time=5,
            enemy_min_damage=40, enemy_max_damage=60, critical_damage=60, normal_damage=45),
}


# ==============================================================
# LEVEL LOCKING
# ==============================================================

def is_level_unlocked(player_data, level_number):
    if level_number == 1:
        return True
    return (level_number - 1) in player_data["world2_cleared"]


def attempt_level(player_data, level_number):
    if not is_level_unlocked(player_data, level_number):
        print("\n🔒 This level is LOCKED! Clear the previous level first.")
        input("Press ENTER to continue...")
        return

    update_hearts(player_data)

    if not has_hearts(player_data):
        print("\nOut of hearts! Come back later.")
        input("Press ENTER to continue...")
        return

    victory = play_level(player_data, level_number, **LEVEL_CONFIGS[level_number])

    if victory and level_number == 5:
        clear_screen()

        print("""
==============================================================
                    WORLD 2 CLEARED!
==============================================================

               Congratulations! You cleared
                    all 5 levels!

==============================================================
""")

        input("Press ENTER to continue...")


# ==============================================================
# WORLD 2 MENU
# ==============================================================

def world2_menu(player_data):

    while True:

        clear_screen()

        show_world2_title()

        update_hearts(player_data)

        print(f"                     {format_hearts_bar(player_data)}")

        print("""
==============================================================

                         LEVELS

==============================================================
""")

        for level in range(1, 6):
            if is_level_unlocked(player_data, level):
                cleared_tag = " (CLEARED)" if level in player_data["world2_cleared"] else ""
                print(f"[{level}] LEVEL {level}{cleared_tag}")
            else:
                print(f"[{level}] LEVEL {level} 🔒")

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

        if not has_hearts(player_data):

            clear_screen()

            update_hearts(player_data)

            print("""
==============================================================
                         OUT OF HEARTS
==============================================================

                  You have no hearts left.

==============================================================
""")

            input("Press ENTER to continue...")

            break


# ==============================================================
# START WORLD 2 (standalone testing)
# ==============================================================

if __name__ == "__main__":
    from hearts import init_player_hearts

    demo_player_data = {
        "coins": 500,
        "world2_cleared": set()
    }
    init_player_hearts(demo_player_data)

    world2_menu(demo_player_data)