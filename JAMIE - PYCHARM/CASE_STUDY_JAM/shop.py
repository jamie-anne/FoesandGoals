import os
import pygame
from CASE_STUDY_JAM.utils import show_bought_items
pygame.mixer.init()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

things = [
    {
        "art": [
            "LAMP"
        ]
    },
    {
        "art": [
            "FAN"
        ]
    },
    {
        "art": [
            "MOUSE"
        ]
    },
    {
        "art": [
            "KEYBOARD"
        ]
    },
    {
        "art": [
            "MIC"
        ]
    },
    {
        "art": [
            "HEADSET"
        ]
    },
    {
        "art": [
            "CHAIR"
        ]
    },
    {
        "art": [
            "MONITOR"
        ]
    },
    {
        "art": [
            "UNIT"
        ]
    }
]




def display_row(fruit_row):
    """Displays one horizontal row of fruits.
       ASCII always shows. Status + press option always show."""

    max_height = max(len(f["art"]) for f in fruit_row)

    # Print ASCII art first (always visible)
    for i in range(max_height):
        parts = []
        for fruit in fruit_row:
            if i < len(fruit["art"]):
                parts.append(fruit["art"][i])
            else:
                parts.append(" " * len(fruit["art"][0]))
        print("    ".join(parts))

    # Print STATUS (locked/unlocked)
    status_line = []
    for fruit in fruit_row:
        if fruit["unlocked"]:
            status_line.append("[UNLOCKED]")
        else:
            status_line.append("[LOCKED]")
    print("    ".join(status_line))

    # Print PRESS number
    press_line = []
    for fruit in fruit_row:
        press_line.append(f"[PRESS {fruit['id']}] - {fruit['name']}")
    print("    ".join(press_line))

    # Print PRICE
    price_line = []
    for fruit in fruit_row:
        price_line.append(f"Price: {fruit['price']}")
    print("    ".join(price_line))

    print("\n")


def shop_menu():
    clear()
    print("\n" + "█" * 150)
    print("\n\t\t\t\t\t      SHOP MENU\n")

    # Prepare rows
    first_row = []
    second_row = []

    # Attach ASCII & metadata into row objects
    for i, item in enumerate(shop_items):
        row_item = {
            "id": i + 1,
            "name": item["name"],
            "price": item["cost"],
            "unlocked": item["unlocked"],
            "art": things[i]["art"]
        }

        if i < 5:
            first_row.append(row_item)
        else:
            second_row.append(row_item)

    display_row(first_row)
    display_row(second_row)
    print("Press [0] to exit")
    print("█" * 150)


shop_items = [
    {"name": "Lamp", "cost": 10, "unlocked": True, "bought": False},
    {"name": "Fan", "cost": 15, "unlocked": False, "bought": False},
    {"name": "Mouse", "cost": 20, "unlocked": False, "bought": False},
    {"name": "Keyboard", "cost": 25, "unlocked": False, "bought": False},
    {"name": "Microphone", "cost": 40, "unlocked": False, "bought": False},
    {"name": "Headset", "cost": 45, "unlocked": False, "bought": False},
    {"name": "Chair", "cost": 50, "unlocked": False, "bought": False},
    {"name": "Monitor", "cost": 70, "unlocked": False, "bought": False},
    {"name": "Unit", "cost": 100, "unlocked": False, "bought": False},
]

def update_unlocks():
    for i in range(1, len(shop_items)):
        if shop_items[i-1]["bought"]:
            shop_items[i]["unlocked"] = True

def buy_item(player, item_name, price):
    if item_name in player['inventory']:
        print("\n\t\t\tYou already own this item!\n")
        input("\n\t\t\t[ Press Enter to continue... ]")
        return

    if player['coins'] < price:
        print("\n\t\t\tNot enough coins!\n")
        input("\n\t\t\t[ Press Enter to continue... ]")
        return

    player['coins'] -= price
    player['inventory'].append(item_name)
    player['last_bought_item'] = item_name

    show_bought_items(player)
    #get_house_ascii(item_name)
    for shop_item in shop_items:
        if shop_item["name"] == item_name:
            shop_item["bought"] = True
            break

def main(player, main_menu_func):
    shop = pygame.mixer.Sound("MUSIC/shop_music.mp3")
    shop.play()
    while True:
        clear()
        update_unlocks()
        shop_menu()
        print(f"\n\t\t\tYour Balance: {player['coins']} coins\n")
        choice = input("\t\t\tEnter your choice (1-9 or 0 to exit): ")

        if choice == '0':
            clear()
            shop.stop()
            main_menu_func(player)
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(shop_items):
            index = int(choice) - 1
            item = shop_items[index]

            if not item["unlocked"]:
                print("\n\t\t\tItem locked! Buy the previous item first.\n")
                input("\n\t\t\t[ Press Enter to continue... ]")
                continue

            buy_item(player, item["name"], item["cost"])
        else:
            print("\n\t\t\tInvalid choice.")
            input("\t\t\t[ Press Enter to continue... ]")
