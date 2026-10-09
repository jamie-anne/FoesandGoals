import string
import random
import time
import os
import pyfiglet

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def big(symbols):
    rendered = [pyfiglet.figlet_format(s, font="big").splitlines() for s in symbols]
    max_height = max(len(r) for r in rendered)
    max_width = max(max(len(line) for line in r) for r in rendered)

    normalized = []
    for r in rendered:
        padded = [line.ljust(max_width) for line in r]
        while len(padded) < max_height:
            padded.append(" " * max_width)
        normalized.append(padded)

    for _ in symbols:
        print(f"\t\t\t┌" + "─" * (max_width + 2) + "┐", end=" ")
    print()

    for line_idx in range(max_height):
        for r in normalized:
            print(f"\t\t\t│ " + r[line_idx] + " │", end=" ")
        print()

    for _ in symbols:
        print(f"\t\t\t└" + "─" * (max_width + 2) + "┘", end=" ")
    print()

def print_box(symbols):
    for _ in symbols:
        print(f"\t\t\t┌─────┐", end=" ")
    print()
    for s in symbols:
        print(f"\t\t\t│  {s}  │", end=" ")
    print()
    for _ in symbols:
        print("\t\t\t└─────┘", end=" ")
    print()

def symbol_guess_game():
    symbols = (
        ['@', '#', '$', '%', '^', '&', '*', '!', '?'] +
        list(string.ascii_uppercase) +
        list(string.ascii_lowercase) +
        list(string.digits)
    )
    secret = [random.choice(symbols) for _ in range(4)]
    lives = 3

    print("🎮 Welcome to the Symbol Guessing Game!")
    print("Possible symbols:", " ".join(symbols))
    print("\nMemorize these 4 symbols — they’ll appear BIG below!\n")

    big(secret)
    time.sleep(4)
    clear()

    print("🧠 Symbols hidden! Try to guess them (order matters). You have 3 lives.\n")

    while lives > 0:
        guess = input("Enter your 4-symbol guess: ").strip()

        if len(guess) != 4:
            print("❌ Your guess must be exactly 4 symbols long!")
            continue

        correct = sum(secret[i] == guess[i] for i in range(4))

        if correct == 4:
            clear()
            print(pyfiglet.figlet_format("YOU WIN!", font="starwars"))
            return True
        else:
            lives -= 1
            print(f"✅ You guessed {correct} correctly.")
            print(f"❤️ Lives remaining: {lives}\n")

    clear()
    print(pyfiglet.figlet_format("GAME OVER", font="doom"))
    print("💀 You've run out of lives.")
    print("The correct symbols were:")
    print_box(secret)
    return False
