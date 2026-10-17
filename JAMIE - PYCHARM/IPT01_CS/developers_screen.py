# ==================================================
# DEVELOPERS SCREEN
# Replace your old developers() function with this one.
# (uses the screen, WIDTH, HEIGHT, pygame and sys already in your main file)
# ==================================================
import pygame
import sys

from developers_screen import developers

def wrap_text(font, text, max_width):
    """Split text into lines that fit inside max_width."""
    words = text.split(" ")
    lines = []
    line = ""
    for word in words:
        test = word if line == "" else line + " " + word
        if font.size(test)[0] <= max_width:
            line = test
        else:
            lines.append(line)
            line = word
    if line != "":
        lines.append(line)
    return lines


def developers():
    BACKGROUND_COLOR = (25, 30, 45)
    CARD_COLOR = (40, 45, 65)

    title_font = pygame.font.Font(None, 80)
    sub_font = pygame.font.Font(None, 36)
    initials_font = pygame.font.Font(None, 56)
    name_font = pygame.font.Font(None, 34)
    role_font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 30)

    team = [
        {"name": "Jamie Anne A. Banjola", "role": "Lead Developer",
         "initials": "JB", "color": (255, 220, 0)},
        {"name": "John Railey R. Mauro", "role": "Co-developer",
         "initials": "JM", "color": (90, 170, 255)},
        {"name": "Justin Lacanilao", "role": "QA Tester & API Specialist",
         "initials": "JL", "color": (90, 210, 130)},
        {"name": "Shermie Sta Ana", "role": "UI/UX Designer & IT Support",
         "initials": "SA", "color": (255, 120, 180)},
    ]

    card_w = 330
    card_h = 300
    gap = 30
    start_x = (WIDTH - (4 * card_w + 3 * gap)) // 2
    start_y = 270

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # ESC hint
        screen.blit(small_font.render("ESC = Back", True, (200, 200, 200)), (70, 28))

        # Title
        title = title_font.render("DEVELOPERS", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 90))

        sub = sub_font.render("The team behind Foes & Goals", True, (255, 220, 0))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 170))

        pygame.draw.line(screen, (90, 95, 120),
                         (WIDTH // 2 - 200, 215), (WIDTH // 2 + 200, 215), 2)

        # Cards
        for i, member in enumerate(team):
            x = start_x + i * (card_w + gap)
            y = start_y
            color = member["color"]
            cx = x + card_w // 2

            card = pygame.Rect(x, y, card_w, card_h)
            pygame.draw.rect(screen, CARD_COLOR, card, border_radius=14)
            pygame.draw.rect(screen, color, card, 3, border_radius=14)

            # Avatar circle with initials
            pygame.draw.circle(screen, color, (cx, y + 85), 52)
            pygame.draw.circle(screen, CARD_COLOR, (cx, y + 85), 46)
            initials = initials_font.render(member["initials"], True, color)
            screen.blit(initials, (cx - initials.get_width() // 2,
                                   y + 85 - initials.get_height() // 2))

            # Name
            name_lines = wrap_text(name_font, member["name"], card_w - 30)
            ty = y + 163
            for line in name_lines:
                text = name_font.render(line, True, (255, 255, 255))
                screen.blit(text, (cx - text.get_width() // 2, ty))
                ty += 32

            # Role
            ty += 8
            for line in wrap_text(role_font, member["role"], card_w - 30):
                text = role_font.render(line, True, color)
                screen.blit(text, (cx - text.get_width() // 2, ty))
                ty += 28

        # Footer
        footer = sub_font.render("Thank you for playing!", True, (255, 255, 255))
        screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, 640))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False