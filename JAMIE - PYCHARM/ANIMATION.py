'''
mport time
import sys


def progress_bar(duration=10, bar_length=70):
    """
    Creates a progress bar animation in the console that fills up over a given duration.
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        # Calculate current progress (0 to 100%)
        elapsed = time.time() - (end_time - duration)
        progress = min(100, int((elapsed / duration) * 100))

        # Calculate filled and empty bar segments
        filled_length = int(bar_length * progress // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        # Print the progress bar (overwrites the line)
        sys.stdout.write(f'\rProgress: |{bar}| {progress}%')  # \r for overwrite
        sys.stdout.flush()
        time.sleep(0.1)  # Small delay for smooth animation

    # Final full bar
    print(f'\rProgress: |{"█" * bar_length}| 100% - Complete!')


# Run the animation for 10 seconds
if __name__ == "__main__":
    print("Starting progress bar animation...")
    progress_bar(10)
    print("\nAnimation complete!")
'''
"""
PYTHON CONSOLE ANIMATIONS - Complete Guide
Various techniques for creating animations in the terminal
"""

import time
import sys
import os
from itertools import cycle


# ==================== BASIC TECHNIQUES ====================

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def simple_loading_animation():
    """Simple loading animation with dots"""
    print("Loading", end="")
    for i in range(10):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print(" Done!")


def spinning_loader():
    """Spinning loader animation"""
    spinners = ['|', '/', '-', '\\']

    print("Processing: ", end="")
    for _ in range(20):
        for spinner in spinners:
            print(f"\rProcessing: {spinner}", end="", flush=True)
            time.sleep(0.1)
    print("\rProcessing: Done!     ")


def progress_bar(total=100):
    """Animated progress bar"""
    print("\nProgress Bar:")
    for i in range(total + 1):
        # Calculate percentage
        percent = (i / total) * 100
        filled = int(i / 2)  # 50 chars total
        bar = '█' * filled + '░' * (50 - filled)

        # Print progress bar
        print(f"\r[{bar}] {percent:.1f}%", end="", flush=True)
        time.sleep(0.05)

    print("\n✅ Complete!")


def typewriter_effect(text, delay=0.05):
    """Typewriter effect for text"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def bouncing_ball():
    """Bouncing ball animation"""
    width = 50
    ball_pos = 0
    direction = 1

    print("\nBouncing Ball (Press Ctrl+C to stop):")

    try:
        while True:
            # Create the animation frame
            frame = ' ' * ball_pos + '●' + ' ' * (width - ball_pos)
            print(f"\r{frame}", end="", flush=True)

            # Update position
            ball_pos += direction

            # Bounce at edges
            if ball_pos >= width or ball_pos <= 0:
                direction *= -1

            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n\nAnimation stopped!")


def countdown_timer(seconds):
    """Animated countdown timer"""
    print("\n⏱️  Countdown Timer:")

    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"\r⏰ Time remaining: {timer}", end="", flush=True)
        time.sleep(1)

    print("\n\n🔔 Time's up!")


# ==================== ADVANCED ANIMATIONS ====================

def matrix_rain():
    """Matrix-style falling characters"""
    import random
    import string

    width = 80
    height = 20

    # Initialize columns
    columns = [0] * width
    chars = string.ascii_letters + string.digits

    print("\nMatrix Rain (Press Ctrl+C to stop):\n")

    try:
        for _ in range(100):  # Limited iterations for demo
            # Create frame
            frame = [[' ' for _ in range(width)] for _ in range(height)]

            for col in range(width):
                if random.random() < 0.1:
                    columns[col] = 0

                if columns[col] < height:
                    frame[columns[col]][col] = random.choice(chars)
                    columns[col] += 1

            # Clear and print frame
            clear_screen()
            for row in frame:
                print(''.join(row))

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nMatrix stopped!")


def loading_spinner_fancy():
    """Fancy loading spinner with multiple styles"""
    spinners = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['|', '/', '-', '\\'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'dots_bounce': ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈'],
        'box': ['◰', '◳', '◲', '◱'],
        'circle': ['◐', '◓', '◑', '◒'],
        'squares': ['◻', '◼', '◻', '◼'],
        'braille': ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],
    }

    print("\nFancy Loading Spinners:\n")

    for name, frames in spinners.items():
        print(f"{name.upper()}: ", end="")

        for _ in range(15):
            for frame in frames:
                print(f"\r{name.upper()}: {frame}", end="", flush=True)
                time.sleep(0.08)

        print(" ✓")
        time.sleep(0.3)


def animated_text_wave(text):
    """Wave animation for text"""
    print("\nWave Animation:")

    for offset in range(10):
        output = ""
        for i, char in enumerate(text):
            # Calculate vertical position
            height = int(2 * (1 + (i + offset) % 4))
            output += '\n' * (4 - height) + char

        clear_screen()
        print(output)
        time.sleep(0.2)


def health_bar_animation(max_health=100):
    """Animated health bar taking damage"""
    health = max_health

    print("\n❤️  Health Bar Animation:")

    while health > 0:
        # Calculate bar
        bar_length = 30
        filled = int((health / max_health) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)

        # Color based on health
        if health > 70:
            color = "🟢"
        elif health > 30:
            color = "🟡"
        else:
            color = "🔴"

        # Display
        print(f"\r{color} HP: [{bar}] {health}/{max_health}  ", end="", flush=True)

        # Take damage
        health -= 5
        time.sleep(0.3)

    print("\n💀 Health depleted!")


def race_animation():
    """Racing cars animation"""
    track_length = 50
    car1_pos = 0
    car2_pos = 0

    print("\n🏁 Racing Animation:\n")

    while car1_pos < track_length and car2_pos < track_length:
        # Move cars
        car1_pos += random.randint(1, 3)
        car2_pos += random.randint(1, 3)

        # Create tracks
        track1 = ' ' * min(car1_pos, track_length) + '🏎️'
        track2 = ' ' * min(car2_pos, track_length) + '🏎️'

        # Display
        print(f"\r🔴 {track1:<{track_length + 2}}", end="")
        print(f"\n🔵 {track2:<{track_length + 2}}", end="", flush=True)
        print("\r", end="")  # Return cursor

        time.sleep(0.1)

    winner = "Red" if car1_pos >= track_length else "Blue"
    print(f"\n\n🏆 {winner} wins!")


def typing_effect_with_cursor(text):
    """Typewriter with blinking cursor"""
    import random

    print("\nTyping Animation:")

    for i in range(len(text) + 1):
        # Simulate typing with occasional pauses
        if random.random() < 0.1:
            time.sleep(0.3)  # Thinking pause

        # Print text with cursor
        current_text = text[:i]
        cursor = '|' if i % 2 == 0 else ' '
        print(f"\r{current_text}{cursor}", end="", flush=True)
        time.sleep(0.1)

    print()  # New line


def explosion_animation():
    """Explosion effect"""
    frames = [
        "     ●     ",
        "    ◉◉◉    ",
        "   ◉◉◉◉◉   ",
        "  ◉◉◉◉◉◉◉  ",
        " ◉◉◉◉◉◉◉◉◉ ",
        "◉◉◉◉◉◉◉◉◉◉◉",
        " ◉◉◉ ◉ ◉◉◉ ",
        "  ◉   ◉   ◉  ",
        "   ·   ·   · ",
        "             "
    ]

    print("\n💥 Explosion Animation:\n")

    for frame in frames:
        print(f"\r{frame}", end="", flush=True)
        time.sleep(0.15)

    print()


def snake_animation():
    """Simple snake moving animation"""
    width = 40
    snake_length = 5
    snake_pos = [0] * snake_length

    print("\n🐍 Snake Animation (Press Ctrl+C to stop):\n")

    try:
        pos = 0
        direction = 1

        for _ in range(100):  # Limited for demo
            # Update snake position
            snake_pos.pop()
            snake_pos.insert(0, pos)

            # Create frame
            frame = [' '] * width
            for segment in snake_pos:
                if 0 <= segment < width:
                    frame[segment] = '█'

            # Display
            print(f"\r{''.join(frame)}", end="", flush=True)

            # Move
            pos += direction
            if pos >= width - 1 or pos <= 0:
                direction *= -1

            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n\nSnake stopped!")


def menu_selection_animation():
    """Animated menu selection"""
    menu_items = [
        "Start Game",
        "Load Game",
        "Settings",
        "Quit"
    ]

    print("\n🎮 Animated Menu:\n")

    for i in range(len(menu_items)):
        clear_screen()
        print("\n🎮 GAME MENU\n" + "=" * 30 + "\n")

        for idx, item in enumerate(menu_items):
            if idx == i:
                # Animated selection
                print(f"  ▶  {item}  ◀")
            else:
                print(f"     {item}")

        time.sleep(0.5)


# ==================== DEMO MENU ====================

def main():
    """Main demonstration menu"""

    demos = {
        '1': ('Simple Loading', simple_loading_animation),
        '2': ('Spinning Loader', spinning_loader),
        '3': ('Progress Bar', lambda: progress_bar(100)),
        '4': ('Typewriter Effect', lambda: typewriter_effect("Hello! This is a typewriter effect animation!")),
        '5': ('Bouncing Ball', bouncing_ball),
        '6': ('Countdown Timer', lambda: countdown_timer(10)),
        '7': ('Fancy Spinners', loading_spinner_fancy),
        '8': ('Health Bar', health_bar_animation),
        '9': ('Race Animation', race_animation),
        '10': ('Typing with Cursor', lambda: typing_effect_with_cursor("Python is awesome!")),
        '11': ('Explosion', explosion_animation),
        '12': ('Snake', snake_animation),
        '13': ('Menu Selection', menu_selection_animation),
    }

    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("  🎨 PYTHON CONSOLE ANIMATION DEMOS 🎨")
        print("=" * 50 + "\n")

        for key, (name, _) in demos.items():
            print(f"  {key}. {name}")

        print(f"  0. Exit")
        print("\n" + "=" * 50)

        choice = input("\nSelect demo (0-13): ").strip()

        if choice == '0':
            print("\n👋 Goodbye!")
            break

        if choice in demos:
            clear_screen()
            print(f"\n▶️  Running: {demos[choice][0]}\n")
            print("-" * 50)

            try:
                demos[choice][1]()
            except Exception as e:
                print(f"\n❌ Error: {e}")

            input("\n\nPress Enter to return to menu...")
        else:
            print("\n❌ Invalid choice!")
            time.sleep(1)


if __name__ == "__main__":
    # Show basic examples first
    print("🎬 CONSOLE ANIMATION BASICS\n")

    print("1️⃣ Progress Bar:")
    progress_bar(50)

    print("\n2️⃣ Typewriter Effect:")
    typewriter_effect("Welcome to Python console animations!", 0.03)

    print("\n3️⃣ Loading Spinner:")
    spinning_loader()

    print("\n4️⃣ Countdown:")
    countdown_timer(5)

    print("\n" + "=" * 50)
    input("\nPress Enter to see the full demo menu...")

    # Run main menu
    main()


