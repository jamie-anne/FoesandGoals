import pygame


def world1(screen, game_data):

    running = True

    font = pygame.font.Font(None, 60)

    while running:

        screen.fill((0, 100, 0))

        title = font.render(
            "WORLD 1",
            True,
            (255, 255, 255)
        )

        screen.blit(title, (500, 250))

        coins = font.render(
            f"Coins: {game_data['coins']}",
            True,
            (255, 255, 0)
        )

        screen.blit(coins, (500, 320))

        info = pygame.font.Font(None, 35).render(
            "Press ESC to return",
            True,
            (255, 255, 255)
        )

        screen.blit(info, (500, 400))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False