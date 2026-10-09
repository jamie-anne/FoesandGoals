import time
import os
import pyfiglet

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def go_to_jar(world, level):
    clear()
    print(pyfiglet.figlet_format("JAR", font="slant"))
    print(f"🎉 Congratulations! You passed World {world}, Level {level}!")
    print("You collected a new item for your jar! 🏆")
    time.sleep(2.5)
