# HOUSE.py

import os
from CASE_STUDY_JAM.utils import house_ascii

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def visit_house(player):
    clear()
    print("\n\t\t=== THIS IS MY HOUSE ===\n")

    last_item = player.get('last_bought_item')

    if not last_item:
        print("\n\t\tYou have not bought any items yet.\n")
    else:
        print(f"\n\t\t[ In your HOUSE: {last_item} ]\n")
        art = house_ascii.get(last_item)
        if art:
            print(art)
        else:
            print("\n\t\t[ ASCII art not found for this item ]\n")

    input("\n\t\t[ Press Enter to continue... ]")
