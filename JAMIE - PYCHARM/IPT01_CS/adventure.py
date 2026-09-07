import os

from world1 import world1_menu
from world2 import world2_menu
from world3 import world3_menu
from hearts import format_hearts_bar, update_hearts


def clear_screen():
    os.system("cls")


TOTAL_LEVELS_PER_WORLD = 5


def is_world_complete(player_data, world_key):
    return len(player_data.get(world_key, set())) >= TOTAL_LEVELS_PER_WORLD


def can_enter_world2(player_data):
    # Normally requires World 1 fully cleared, but a cheat can
    # force this open on its own, without touching World 1's progress.
    return (
        is_world_complete(player_data, "world1_cleared")
        or player_data.get("world2_unlocked", False)
    )


def can_enter_world3(player_data):
    # Normally requires World 2 fully cleared, but a cheat can
    # force this open on its own, without touching World 1/2 progress.
    return (
        is_world_complete(player_data, "world2_cleared")
        or player_data.get("world3_unlocked", False)
    )


def adventure_menu(player_data):

    while True:

        clear_screen()

        world2_accessible = can_enter_world2(player_data)
        world3_accessible = can_enter_world3(player_data)

        world2_label = (
            "WORLD 2 - SEA / ICE"
            if world2_accessible
            else "WORLD 2 - SEA / ICE (LOCKED)"
        )

        world3_label = (
            "WORLD 3 - FIRE / LAVA"
            if world3_accessible
            else "WORLD 3 - FIRE / LAVA (LOCKED)"
        )

        update_hearts(player_data)

        print(format_hearts_bar(player_data))

        print(r"""
==============================================================
                         ADVENTURE
==============================================================

                    Choose Your World

                [1] WORLD 1 - LAND""")

        print(f"                [2] {world2_label}")
        print(f"                [3] {world3_label}")

        print("""                [4] BACK TO MAIN MENU

==============================================================
""")

        choice = input("Enter your choice: ")

        # ======================================================
        # CHEAT CODES
        # ======================================================
        # Each cheat unlocks ONLY its own target world.
        # 1_world is the exception: World 1 has no lock of its own,
        # so "unlocking" it means clearing all its levels instead -
        # which naturally opens World 2's gate as a side effect.

        if choice == "1_world":

            player_data["world1_cleared"] = set(
                range(1, TOTAL_LEVELS_PER_WORLD + 1)
            )

            print("""
==============================================================
                     CHEAT ACTIVATED!
==============================================================

                WORLD 1 FULLY CLEARED!

                ✓ LEVEL 1
                ✓ LEVEL 2
                ✓ LEVEL 3
                ✓ LEVEL 4
                ✓ LEVEL 5

==============================================================
""")

            input("Press ENTER to continue...")

        elif choice == "2_world":

            player_data["world2_unlocked"] = True

            print("""
==============================================================
                     CHEAT ACTIVATED!
==============================================================

                    WORLD 2 UNLOCKED!

==============================================================
""")

            input("Press ENTER to continue...")

        elif choice == "3_world":

            player_data["world3_unlocked"] = True

            print("""
==============================================================
                     CHEAT ACTIVATED!
==============================================================

                    WORLD 3 UNLOCKED!

==============================================================
""")

            input("Press ENTER to continue...")

        # ======================================================
        # WORLD 1
        # ======================================================

        elif choice == "1":

            world1_menu(player_data)

        # ======================================================
        # WORLD 2
        # ======================================================

        elif choice == "2":

            if world2_accessible:

                world2_menu(player_data)

            else:

                print("""
==============================================================
                         LOCKED!
==============================================================

              WORLD 2 is LOCKED!

              Clear all of World 1 first.

==============================================================
""")

                input("Press ENTER to continue...")

        # ======================================================
        # WORLD 3
        # ======================================================

        elif choice == "3":

            if world3_accessible:

                world3_menu(player_data)

            else:

                print("""
==============================================================
                         LOCKED!
==============================================================

              WORLD 3 is LOCKED!

              Clear all of World 2 first.

==============================================================
""")

                input("Press ENTER to continue...")

        # ======================================================
        # BACK
        # ======================================================

        elif choice == "4":

            break

        # ======================================================
        # INVALID
        # ======================================================

        else:

            print("\nInvalid choice!")
            input("Press ENTER to continue...")