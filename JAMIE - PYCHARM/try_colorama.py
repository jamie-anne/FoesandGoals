import os
import time

# =====================================================
# ASCII ART for 10 fruits
# =====================================================
APPLE = [
"     _     ",
"  _ / \\ _  ",
" /       \\ ",
"|  ( )  |  ",
" \\  _  /   ",
"  \\/ \\/    "
]

BANANA = [
"   .-.     ",
"  (   )    ",
"   `-'     ",
"  .-.      ",
" (   )  __ ",
"  `-'  (  )",
"        `-' "
]

ORANGE = [
"   .-'''-. ",
"  /       \\",
" |  (o o) |",
"  \\   ^   /",
"   '-._.-' "
]

GRAPE = [
"   .-'''-. ",
"  ( o   o )",
"   \\  ^  / ",
"    '-.-'  ",
"     | |   ",
"    (___)  "
]

WATERMELON = [
"   .-~~~~-. ",
"  /        \\",
" |  🍉 🍉  |",
"  \\        /",
"   `-.__.-' "
]

MANGO = [
"   .-'''-.  ",
"  /       \\ ",
" |  (   ) | ",
"  \\   ^   / ",
"   '-._.-'  "
]

STRAWBERRY = [
"   .-'''-. ",
"  /       \\",
" |  (♥)   |",
"  \\  ^   / ",
"   '-.-.-' "
]

PINEAPPLE = [
"   \\|/   ",
"   -O-   ",
"   /|\\   ",
"  /___\\  ",
"  \\___/  "
]

CHERRY = [
"   ()  () ",
"    \\__/  ",
"     ||   ",
"     ||   ",
"     ||   "
]

KIWI = [
"   .-'''-. ",
"  /       \\",
" |  ( o ) |",
"  \\       /",
"   '-._.-' "
]

# =====================================================
# Fruit data (10 fruits total)
# =====================================================
fruits = [
    {"name": "Apple", "price": 30, "art": APPLE, "unlocked": True, "bought": False},
    {"name": "Banana", "price": 40, "art": BANANA, "unlocked": False, "bought": False},
    {"name": "Orange", "price": 50, "art": ORANGE, "unlocked": False, "bought": False},
    {"name": "Grape", "price": 60, "art": GRAPE, "unlocked": False, "bought": False},
    {"name": "Watermelon", "price": 70, "art": WATERMELON, "unlocked": False, "bought": False},
    {"name": "Mango", "price": 80, "art": MANGO, "unlocked": False, "bought": False},
    {"name": "Strawberry", "price": 90, "art": STRAWBERRY, "unlocked": False, "bought": False},
    {"name": "Pineapple", "price": 100, "art": PINEAPPLE, "unlocked": False, "bought": False},
    {"name": "Cherry", "price": 110, "art": CHERRY, "unlocked": False, "bought": False},
    {"name": "Kiwi", "price": 120, "art": KIWI, "unlocked": False, "bought": False}
]

balance = 500  # starting money

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_row(fruit_row):
    """Displays one horizontal row of fruits"""
    max_height = max(len(f["art"]) for f in fruit_row)
    for i in range(max_height):
        parts = []
        for fruit in fruit_row:
            if fruit["unlocked"]:
                if i < len(fruit["art"]):
                    parts.append(fruit["art"][i])
                else:
                    parts.append(" " * len(fruit["art"][0]))
            else:
                if i == max_height // 2:
                    parts.append(" [LOCKED] ")
                else:
                    parts.append(" " * 9)
        print("    ".join(parts))
    print("\n")


def display_shop():
    clear()
    print("🍎🍌🍊🍇🍉  WELCOME TO THE FRUIT SHOP  🍉🍇🍊🍌🍎\n")

    first_row = fruits[:5]
    second_row = fruits[5:]
    display_row(first_row)
    display_row(second_row)

    for idx, fruit in enumerate(fruits, start=1):
        if not fruit["unlocked"]:
            status = "🔒 Locked"
        elif fruit["bought"]:
            status = "✅ Purchased"
        else:
            status = f"₱{fruit['price']}"
        print(f"{idx}. {fruit['name']}: {status}")

    print(f"\nYour Balance: ₱{balance}")
    print("0. Exit\n")


def buy_fruit(choice):
    global balance

    if choice == "0":
        print("Thanks for shopping! 🛒")
        exit()

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(fruits):
        print("Invalid choice.")
        time.sleep(1)
        return

    idx = int(choice) - 1
    fruit = fruits[idx]

    if not fruit["unlocked"]:
        print(f"{fruit['name']} is locked! Buy the previous fruit to unlock it.")
        time.sleep(1)
        return

    if fruit["bought"]:
        print(f"You already bought {fruit['name']}! ✅")
        time.sleep(1)
        return

    if balance < fruit["price"]:
        print("Not enough balance.")
        time.sleep(1)
        return

    # Purchase logic
    balance -= fruit["price"]
    fruit["bought"] = True
    print(f"You bought {fruit['name']} for ₱{fruit['price']}!")

    # Unlock next fruit
    if idx + 1 < len(fruits):
        fruits[idx + 1]["unlocked"] = True
        print(f"{fruits[idx + 1]['name']} is now unlocked! 🎉")

    input("\nPress Enter to continue...")


def main():
    while True:
        display_shop()
        choice = input("Enter the number you want to buy: ").strip()
        buy_fruit(choice)


if __name__ == "__main__":
    main()
