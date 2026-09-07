import os


def clear_screen():
    os.system("cls")


def shop_menu(player_data):
    while True:
        clear_screen()

        print("""
==============================================================
                           SHOP
==============================================================

""")

        print(f"Coins: {player_data['coins']}")

        print("""
==============================================================

                    iPHONE 17 PARTS

[1] Battery          - 100 Coins
[2] Screen           - 150 Coins
[3] Camera           - 200 Coins
[4] Frame            - 250 Coins
[5] Back

==============================================================
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            buy_part(player_data, "Battery", 100)

        elif choice == "2":
            buy_part(player_data, "Screen", 150)

        elif choice == "3":
            buy_part(player_data, "Camera", 200)

        elif choice == "4":
            buy_part(player_data, "Frame", 250)

        elif choice == "5":
            break

        else:
            print("\nInvalid choice!")
            input("Press ENTER to continue...")


def buy_part(player_data, part_name, price):

    if player_data["iphone_parts"][part_name]:
        print(f"\nYou already own the {part_name}!")
        input("Press ENTER to continue...")
        return

    if player_data["coins"] < price:
        print("\nYou don't have enough coins!")
        input("Press ENTER to continue...")
        return

    player_data["coins"] -= price
    player_data["iphone_parts"][part_name] = True

    print(f"\nYou bought the {part_name}!")
    print(f"Remaining coins: {player_data['coins']}")

    input("\nPress ENTER to continue...")