'''
x = 1
y = 6

while x <= 5:
    print(" " * x ,"*" * y )
    y -= 1
    x += 1

while x >= 1:
    print(" " * x ,"*" * y )
    y += 1
    x -= 1



x = 2
y = 1

j = 2
z = 8
print(" " * x + "   **")
while 1 <= x:
    print(" " * y + " " * x + "*" * y + "*" * j + "*" * y)
    x -= 1
    j += 2

while z >= 1:
    print(" " * y + " " * x + "*" * z)
    x += 1
    z -= 2

win = True
lose = False
x = 10
y = 5
while x > y:
    print("\n",win + win, end="")
    x = x-1


school = "NEUST"
N,E,U = "NUEVA","ECIJA","UNIVERSITY"
S,T="SCIENCE","TECHNOLOGY"
for i in school:
    if i == "U":
        print("STATE")
        continue
        print(i)
    elif i == "S":
        print(U)
    elif i == "T":
        break
    else:
        if i == "N":
            print(N)
        elif i == "E":
            print(E)
        else:
            print(i,"\n")


import random
even = 0
odd = 0
for i in range(1,11):
    ran = random.randint(1, 50)
    if ran % 2 == 0:
        print(ran,"is even")
        even += 1
    else:
        print(ran,"is odd")
        odd += 1
print("Total even: ",even)
print("Total odd: ",odd)


x = "*"
while x <= "******":
    print(x)
    x += "*"
'''
import time
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Game data
worlds = {
    1: {"levels": 5, "unlocked": True, "completed_levels": 0},
    2: {"levels": 5, "unlocked": False, "completed_levels": 0},
    3: {"levels": 5, "unlocked": False, "completed_levels": 0},
}

def play_level(world):
    """Play one level in the selected world"""
    current_level = worlds[world]["completed_levels"] + 1

    clear()
    print(f"🌍 World {world} - Level {current_level}")
    print("=" * 30)
    print("You are fighting through the challenge... ⚔️")
    input("Press Enter to complete the level ✅ ")

    # Mark level complete
    worlds[world]["completed_levels"] += 1
    print(f"🎉 Level {current_level} complete!")
    time.sleep(1)

    # Check if world finished
    if worlds[world]["completed_levels"] == worlds[world]["levels"]:
        print(f"🏆 You finished all levels in World {world}!")
        if world < 3:
            worlds[world + 1]["unlocked"] = True
            print(f"🔓 World {world + 1} is now unlocked!")
        else:
            print("🎉 You have finished the entire game! 🌟")
        time.sleep(2)
    else:
        print(f"Progress: {worlds[world]['completed_levels']}/{worlds[world]['levels']} levels done.")
        time.sleep(1.5)


def show_menu():
    """Display available worlds"""
    clear()
    print("🎮 WELCOME TO THE 3 WORLDS ADVENTURE")
    print("=====================================\n")

    for w, data in worlds.items():
        status = "Unlocked" if data["unlocked"] else "Locked"
        print(f"🌍 World {w}: {status} ({data['completed_levels']}/{data['levels']} levels done)")

    print("\nEnter 0 to exit the game.")


def main():
    while True:
        show_menu()

        try:
            choice = int(input("\nChoose a world to play: "))
        except ValueError:
            print("❌ Please enter a number.")
            time.sleep(1.5)
            continue

        if choice == 0:
            print("\n👋 Thanks for playing! Goodbye!")
            break
        elif choice not in worlds:
            print("❌ Invalid world choice.")
            time.sleep(1.5)
        elif not worlds[choice]["unlocked"]:
            print("🔒 That world is still locked. Finish the previous one first!")
            time.sleep(1.5)
        elif worlds[choice]["completed_levels"] == worlds[choice]["levels"]:
            print("✅ You've already completed this world!")
            time.sleep(1.5)
        else:
            play_level(choice)

# Run the game
main()

