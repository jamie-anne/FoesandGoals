import os
import time
import random
import msvcrt


def clear_screen():
    os.system("cls")


# ==============================================================
# WORLD 3 - SLOT ATTACK (TRIAL)
# ==============================================================

def slot_attack():

    symbols = ["⚔️", "🔫", "💣"]

    # Starting symbols
    slot1 = random.choice(symbols)
    slot2 = random.choice(symbols)
    slot3 = random.choice(symbols)

    clear_screen()

    print("""
==============================================================
                     WORLD 3 - FIRE
                      SLOT ATTACK
==============================================================

                    WILD ENEMY

==============================================================
""")

    print("""
                  Press SPACE to spin!

==============================================================
""")

    input("Press ENTER to start...")

    # ==========================================================
    # SPINNING
    # ==========================================================

    start_time = time.time()

    while True:

        # Randomize the symbols
        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)

        clear_screen()

        print("""
==============================================================
                     WORLD 3 - FIRE
                      SLOT ATTACK
==============================================================

                    WILD ENEMY

==============================================================
""")

        print(f"""
                    {slot1}     {slot2}     {slot3}

==============================================================

                 Press SPACE to STOP!

==============================================================
""")

        # Check for SPACE
        if msvcrt.kbhit():

            key = msvcrt.getch()

            if key == b" ":
                break

        time.sleep(0.1)

    # ==========================================================
    # RESULT
    # ==========================================================

    clear_screen()

    print("""
==============================================================
                       RESULT!
==============================================================
""")

    print(f"""
                    {slot1}     {slot2}     {slot3}
""")

    print("""
==============================================================
""")

    # ==========================================================
    # CHECK COMBINATION
    # ==========================================================

    if slot1 == slot2 == slot3:

        if slot1 == "⚔️":

            print("""
                    ⚔️ SWORD COMBO! ⚔️

                       GREAT HIT!
                       DAMAGE: 40
""")

        elif slot1 == "🔫":

            print("""
                    🔫 GUN COMBO! 🔫

                       BULLSEYE!
                       DAMAGE: 50
""")

        elif slot1 == "💣":

            print("""
                    💣 BOMB JACKPOT! 💣

                       MASSIVE HIT!
                       DAMAGE: 70
""")

    elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:

        print("""
                    DOUBLE COMBO!

                       GOOD HIT!
                       DAMAGE: 25
""")

    else:

        print("""
                    NO COMBO!

                       WEAK HIT!
                       DAMAGE: 10
""")

    print("""
==============================================================
""")

    input("Press ENTER to try again...")


# ==============================================================
# TEST
# ==============================================================

while True:

    slot_attack()

    clear_screen()

    print("""
==============================================================
                    PLAY AGAIN?
==============================================================

                    [1] YES
                    [2] NO

==============================================================
""")

    choice = input("Choose: ")

    if choice == "2":
        break
