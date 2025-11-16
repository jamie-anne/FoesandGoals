import os
from CASE_STUDY_JAM.utils import show_bought_items, house_ascii, get_house_ascii
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def shop_menu():
    menu_shop = """
    \t█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
   
    \t\t\t                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀       ⢠⡄⠂⠐⢐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    \t\t\t                 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀         ⠐⠿⢕⣤⣾⠩⢜⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    \t\t\t                 ⠀⠀⣴⣶⣶⣶⣶⣦⣴⡀⠀         ⠰⠀⠀⣹⡏⠀⠠⠃⠀ ⠀     ⠐⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀            ⣤⣤⣤⡄⠀⠀⠀⠀⠀
    \t\t\t                 ⠀⢠⣿⣿⣿⣿⣿⢿⣿⣇⠀⠀         ⠁⠸⢮⠛⠄⠉⠀   ⠀   ⣠⣼⣾⣿⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀             ⣽⣷⣿⠁⠀⠀⠀⠀⠀
    \t\t\t                 ⠀⠀⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⠀⠀         ⠘⠀⠀⠀⠀⠀⠀     ⠘⢿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀   ⠀      ⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠀⠀        ⢠⣼⣷⣿⣢⣤⠀⠘⠃⠀
    \t\t\t                 ⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀         ⢸⠆⠀⠀⠀⠀⠀⠀      ⠈⠻⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠀⠀        ⠈⠙⠛⠛⢹⡇⡄⠊⠑⡄
    \t\t\t                 ⠀⠀⠀⠀⠀⢺⠀⠀⠀⠀⠀⠀⠀⠀         ⢸⡃⠀⠀⠀⠀⠀⠀⠀⠀       ⢻⣿⣿⣿⣿⣿⣿⡇⠀⠀       ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠀⠀⠀⠀  ⠀⠀      ⢸⡇⠁⣀⠐⠁
    \t\t\t                 ⠀⠀⠀⠀⠀⡎⡀⠀⠀⠀⠀⠀⠀⠀         ⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀       ⠙⠻⢿⣿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀            ⠤⠄⠸⠷⠀⠀⠀⠀
    \t\t\t                 ⠀⠀⠀⠐⠛⠛⠛⠓⠀⠀⠀⠀         ⢾⣽⣟⣛⣯⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    \t\t\t
    \t\t\t
    \t\t\t               PRESS[1] - LAMP   PRESS [2] - FAN    PRESS[3] - MOUSE     PRESS[4] - KEYBOARD     PRESS[5] - MIC 
    \t\t\t                  PHP 10.00         PHP 15.00          PHP 20.00             PHP 25.00              PHP 40.00
    \t\t\t                 
    \t\t\t                 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      ⢀⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                       ⢀⣀⣀⠀⠀⠀⠀⠀⠀
    \t\t\t                 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      ⢰⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                  ⣀⣾⣿⣿⣿⣿⣶⣶⣆⠀⠀
    \t\t\t                 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      ⢠⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                   ⣠⣴⣿⣿⣿⣿⣿⡟⣟⣻⣿⢿⠀⠀
    \t\t\t                 ⠀⠀⠀⠀⣤⠞⠛⠛⠓⠣⡠⠀⠀⠀ ⠀       ⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀         ⣀⣀⣀⣀⣀⣀⢀⡀⣀⣀⣀⣀⣀⣀⠀⠀⠀          ⣿⣿⣿⡿⢿⣟⣿⣿⣧⣙⡟⣿⠀⠀
    \t\t\t                 ⠀⠀⠀⡾⠁⠀⠀⠀⠀⠀⢳⡆⠀⠀⠀⠀⠀      ⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀        ⡟⠊⠗⡈⠘⠈⠄⠙⠀⠫⠘⠌⠼⣸⠀⠀⠀         ⣯⠀⢞⡇⡸⣿⣿⣿⣿⡿⣿⣿⣿⠀⠀
    \t\t\t                 ⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀      ⢼⣿⣿⣿⣿⣿⣿⣷⠆⠀⠀⠀⠀        ⠦⠄⠀⠀⠈⠀⠀⠀⠀⠀⠈⠀⠀ ⠀⠀          ⣿⣿⣶⣃⣱⠇⣹⣿⣧⠝⠟⣿⣿⠀⠀
    \t\t\t                 ⠀⠀⢸⣇⣀⡀⠀⠀⠀⣼⡟⠀⠀⠀⠀⠀⠀      ⢸⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀        ⡃⠐⠒⠀⠐⠚⠒⡻⠒⠃⠁⠚⠉⢹⠀⠀         ⢀⣿⣿⡶⠿⡇⣀⣿⣿⣿⣷⣷⣿⣿⠇⠀
    \t\t\t                 ⠀⠀⢠⣿⣼⣿⣦⣾⣿⣿⣆⠀⠀⠀⠀⠀⠀      ⠈⠉⠉⢹⡏⠉⠉⠁⠀⠀⠀⠀⠀        ⣿⣷⣶⣴⣾⣶⣵⣶⣶⣦⣶⣮⣿⣾⠀⠀         ⠠⣿⣿⡟⠺⠧⠈⣿⣿⣿⠫⣽⣿⣿⡆⠀
    \t\t\t                 ⣀⠀⠈⠿⣿⣿⠿⣿⣿⣿⡿⠀⠀⠀⠀⠀       ⣀⣤⠴⢾⡷⠶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀        ⣀⣀⣼⣧⣀⣀⠀⠀⠀⠀⠀⠀         ⢐⡏⠀⢨⠐⡄⠡⢸⣿⣿⣍⣫⣽⣿⡅⠀
    \t\t\t                 ⠉⠛⠒⠒⠒⠒⠚⢛⠋⠉⠀⠀⠀⠀⠀⠀      ⠘⠃⠀⠀⢰⡇⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀ ⠀       ⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀         ⠘⠱⠶⠙⠲⠸⠶⠿⠟⠛⠛⠻⠿⠛⠃⠀
    \t\t\t
    \t\t\t
    \t\t\t             PRESS[6] - HEADSET     PRESS[7] - CHAIR       PRESS[8] - MONITOR      PRESS[9] - SYSTEM UNIT
    \t\t\t                  PHP 45.00            PHP 50.00                PHP 70.00                PHP 100.00
    
    \t█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
    """
    print(menu_shop)


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
        print("\n\t\tYou already own this item!\n")
        input("\n\t\t[ Press Enter to continue... ]")
        return

    if player['coins'] < price:
        print("\n\t\tNot enough coins!\n")
        input("\n\t\t[ Press Enter to continue... ]")
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
    while True:
        clear()
        update_unlocks()
        shop_menu()
        print(f"\n\t\tYour Balance: {player['coins']} coins\n")
        choice = input("\t\tEnter your choice (1-9 or 0 to exit): ")

        if choice == '0':
            clear()
            main_menu_func(player)
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(shop_items):
            index = int(choice) - 1
            item = shop_items[index]

            if not item["unlocked"]:
                print("\n\t\tItem locked! Buy the previous item first.\n")
                input("\n\t\t[ Press Enter to continue... ]")
                continue

            buy_item(player, item["name"], item["cost"])
        else:
            print("\n\t\tInvalid choice.")
            input("\t\tPress Enter to continue...")
