import json
import os

SAVE_FILE = "game_old.json"


def save_game(game_data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(game_data, f)
    except OSError as error:
        print("Could not save:", error)


def load_game(game_data):
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE) as f:
                game_data.update(json.load(f))
        except (OSError, ValueError) as error:
            print("Could not load save:", error)

    # Old saves may still contain Pokemon book data; it is no longer used.
    game_data.pop("pokemon_book", None)
