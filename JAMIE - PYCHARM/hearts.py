import time


HEART_REGEN_SECONDS = 120  # 2 minutes per heart


def init_player_hearts(player_data, max_hearts=5):
    """Call once when player_data is created."""
    player_data["hearts"] = max_hearts
    player_data["max_hearts"] = max_hearts
    player_data["next_heart_time"] = None  # no timer running while at full hearts


def format_hearts_bar(player_data):
    hearts = player_data["hearts"]
    max_hearts = player_data["max_hearts"]
    return f"❤  [{hearts}/{max_hearts}]"


def format_time_remaining(seconds):
    seconds = max(0, int(seconds))
    minutes, secs = divmod(seconds, 60)
    return f"{minutes:02d}:{secs:02d}"


def update_hearts(player_data):
    """Apply any regen that has completed since the last check.

    Call this before showing hearts anywhere (menus, battle screens).
    Returns seconds remaining until the next heart (0 if already full)."""

    if player_data["hearts"] >= player_data["max_hearts"]:
        player_data["next_heart_time"] = None
        return 0

    if player_data["next_heart_time"] is None:
        # Below max but no timer running yet (e.g. right after loading) - start one.
        player_data["next_heart_time"] = time.time() + HEART_REGEN_SECONDS

    now = time.time()

    while now >= player_data["next_heart_time"] and player_data["hearts"] < player_data["max_hearts"]:
        player_data["hearts"] += 1

        if player_data["hearts"] < player_data["max_hearts"]:
            player_data["next_heart_time"] += HEART_REGEN_SECONDS
        else:
            player_data["next_heart_time"] = None

    if player_data["hearts"] >= player_data["max_hearts"]:
        return 0

    return player_data["next_heart_time"] - time.time()


def lose_heart(player_data):
    """Call whenever the player loses a battle, in ANY world."""

    if player_data["hearts"] <= 0:
        return

    player_data["hearts"] -= 1

    if player_data["next_heart_time"] is None:
        # Was at full hearts - timer starts fresh at 2:00.
        player_data["next_heart_time"] = time.time() + HEART_REGEN_SECONDS
    else:
        # Timer was already running - tack on another 2:00.
        player_data["next_heart_time"] += HEART_REGEN_SECONDS


def has_hearts(player_data):
    return player_data["hearts"] > 0