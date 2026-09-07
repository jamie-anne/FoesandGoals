import os


def clear_screen():
    os.system("cls")


def iphone_menu(player_data):
    while True:
        clear_screen()

        print("""
==============================================================
                         IPHONE 17
==============================================================

                    iPHONE 17 PARTS

==============================================================
""")

        for part, installed in player_data["iphone_parts"].items():

            if installed:
                print(f"{part:<15} : ON THE PHONE")
            else:
                print(f"{part:<15} : NOT INSTALLED")

        print("""
==============================================================

[1] Back

==============================================================
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            break

        else:
            print("\nInvalid choice!")
            input("Press ENTER to continue...")