import time
import os
import sys
import pyfiglet

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def go_to_jail(world, level):
    clear()
    print(pyfiglet.figlet_format("JAIL", font="slant"))
    print(f"💀 You failed World {world}, Level {level}. You’re in jail!")
    print("Better luck next time!")
    time.sleep(2.5)


for i in range(10, 0, -1):
    sys.stdout.write(f"\rCountdown: {i} ")
    sys.stdout.flush()
    time.sleep(1)

print("\nTime’s up!")
