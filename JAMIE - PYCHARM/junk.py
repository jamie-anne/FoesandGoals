import time
import threading
import sys

stop_timer = False  # flag to stop the timer

def wait_for_enter():
    global stop_timer
    input()  # waits until ENTER is pressed
    stop_timer = True

# Start a thread to listen for ENTER
threading.Thread(target=wait_for_enter, daemon=True).start()

print("Timer started... (press ENTER to stop)\n")

counter = 0.00

while not stop_timer:
    counter += 0.01
    sys.stdout.write(f"\r{counter:.2f} seconds")
    sys.stdout.flush()
    time.sleep(0.01)

print(f"\nFinal time: {counter:.2f} seconds")
