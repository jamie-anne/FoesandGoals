import os

from adventure import adventure_menu
from shop import shop_menu
from iphone import iphone_menu
from hearts import init_player_hearts


def clear_screen():
    os.system("cls")


def show_title():
    print("""
==============================================================
                      FOES & GOALS
==============================================================

                    AN ADVENTURE GAME

==============================================================
""")


def main_menu():

    player_data = {
        "coins": 0,

        "iphone_parts": {
            "Battery": False,
            "Screen": False,
            "Camera": False,
            "Frame": False
        },

        # ---- LEVEL PROGRESS ----
        # Levels the player has cleared, per world.
        "world1_cleared": set(),
        "world2_cleared": set(),
        "world3_cleared": set(),

        # ---- CHEAT-CODE WORLD ACCESS ----
        # Lets 2_world / 3_world open a world's gate directly,
        # without needing the earlier world(s) actually cleared.
        "world2_unlocked": False,
        "world3_unlocked": False
    }

    # ---- HEART SYSTEM (global - shared across every world) ----
    init_player_hearts(player_data)

    while True:

        clear_screen()
        show_title()

        print(f"Coins: {player_data['coins']}\n")

        print("[1] ADVENTURE")
        print("[2] SHOP")
        print("[3] IPHONE 17")
        print("[4] EXIT GAME")

        print("\n==============================================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            adventure_menu(player_data)

        elif choice == "2":
            shop_menu(player_data)

        elif choice == "3":
            iphone_menu(player_data)

        elif choice == "4":
            clear_screen()

            print("""
==============================================================
                  THANK YOU FOR PLAYING!
                       FOES & GOALS
==============================================================
""")
            break

        else:
            print("\nInvalid choice!")
            input("Press ENTER to continue...")


if __name__ == "__main__":
    main_menu()