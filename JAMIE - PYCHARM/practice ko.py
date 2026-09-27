import pygame
import random

pygame.init()

# =========================
# WINDOW
# =========================

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Foes & Goals - Slot Machine")

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# =========================
# EMOJI FONT
# =========================

emoji_font = pygame.font.Font(
    r"C:\Windows\Fonts\seguiemj.ttf",
    80
)

small_font = pygame.font.Font(None, 40)

# =========================
# SYMBOLS
# =========================

symbols = ["🏹", "⚔️", "💣"]

# Starting symbols
reels = [
    random.choice(symbols),
    random.choice(symbols),
    random.choice(symbols)
]

# =========================
# REEL POSITIONS
# =========================

reel_x = [220, 360, 500]
reel_y = 190

# =========================
# SPINNING
# =========================

spinning = False

# Controls how quickly the symbols change
last_change = 0
change_delay = 100

running = True

while running:

    # =========================
    # EVENTS
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # SPACE = START / STOP
            if event.key == pygame.K_SPACE:

                # Start spinning
                if not spinning:

                    spinning = True

                # Stop spinning
                else:

                    spinning = False

    # =========================
    # UPDATE
    # =========================

    current_time = pygame.time.get_ticks()

    if spinning:

        if current_time - last_change >= change_delay:

            # Change all 3 symbols
            for i in range(3):
                reels[i] = random.choice(symbols)

            last_change = current_time

    # =========================
    # DRAW
    # =========================

    screen.fill(WHITE)

    # Title
    title = small_font.render(
        "FOES & GOALS",
        True,
        BLACK
    )

    screen.blit(
        title,
        (320, 80)
    )

    # =========================
    # DRAW REELS
    # =========================

    for i in range(3):

        # Slot box
        pygame.draw.rect(
            screen,
            GRAY,
            (reel_x[i], reel_y, 100, 110)
        )

        # Emoji
        emoji = emoji_font.render(
            reels[i],
            True,
            BLACK
        )

        screen.blit(
            emoji,
            (
                reel_x[i] + 50 - emoji.get_width() // 2,
                reel_y + 10
            )
        )

    # =========================
    # INSTRUCTION
    # =========================

    if spinning:

        message = "PRESS SPACE TO STOP"

    else:

        message = "PRESS SPACE TO START"

    text = small_font.render(
        message,
        True,
        BLACK
    )

    screen.blit(
        text,
        (
            290,
            370
        )
    )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()