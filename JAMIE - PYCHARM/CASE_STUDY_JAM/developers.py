import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def programmers(player):
    print("Developers")
    input("\n[ Press Enter to continue... ]")
    from LP_STORY_MENU import main_menu
    clear()
    main_menu(player)  # Go back to main menu
