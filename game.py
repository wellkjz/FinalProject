import pygame
import random

pygame.init()

WIDTH = 400
HEIGHT = 600

FPS = 60

GRAVITY = 0.5
JUMP_FORCE = -12
PLAYER_SPEED = 5

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
BLUE = (70, 140, 255)
GREEN = (80, 200, 120)
DARK_GREEN = (40, 120, 70)
RED = (220, 70, 70)
YELLOW = (255, 220, 90)
SKY = (135, 206, 235)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Jump")

clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 30)

# =========================
# PLAYER
# =========================

player = pygame.Rect(180, 500, 30, 30)

player_y_velocity = 0

# =========================
# PLATFORMS
# =========================

platforms = []

for i in range(10):
    x = random.randint(0, WIDTH - 80)
    y = HEIGHT - i * 60
    platforms.append(pygame.Rect(x, y, 80, 12))

# =========================
# ENEMIES
# =========================

enemies = []

for i in range(3):
    x = random.randint(0, WIDTH - 30)
    y = random.randint(50, HEIGHT - 200)
    enemies.append(pygame.Rect(x, y, 25, 25))

# =========================
# BOOSTERS
# =========================

boosters = []

for i in range(3):
    x = random.randint(0, WIDTH - 20)
    y = random.randint(50, HEIGHT - 300)
    boosters.append(pygame.Rect(x, y, 20, 10))

# =========================
# GAME VARIABLES
# =========================

score = 0

game_over = False

# =========================
# GAME LOOP
# =========================

running = True

while running:

    clock.tick(FPS)

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # =========================
    # UPDATE
    # =========================

    if not game_over:

        # movement
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        # gravity
        player_y_velocity += GRAVITY
        player.y += player_y_velocity

        # screen wrap
        if player.x < -30:
            player.x = WIDTH

        if player.x > WIDTH:
            player.x = -30

        # collision with platforms
        for platform in platforms:

            if player.colliderect(platform):

                if player_y_velocity > 0:
                    player_y_velocity = JUMP_FORCE

        # collision with enemies
        for enemy in enemies:

            if player.colliderect(enemy):
                game_over = True

        # collision with boosters
        for booster in boosters:

            if player.colliderect(booster):
                player_y_velocity = -20

        # scrolling world
        if player.y < HEIGHT // 3:

            scroll = HEIGHT // 3 - player.y
            player.y = HEIGHT // 3

            score += scroll

            for platform in platforms:
                platform.y += scroll

            for enemy in enemies:
                enemy.y += scroll

            for booster in boosters:
                booster.y += scroll

        # remove old platforms
        platforms = [p for p in platforms if p.y < HEIGHT]

        # generate new platforms
        while len(platforms) < 10:

            x = random.randint(0, WIDTH - 80)
            y = random.randint(-50, 0)

            platforms.append(
                pygame.Rect(x, y, 80, 12)
            )

        # move enemies
        for enemy in enemies:
            enemy.x += random.choice([-1, 1])

        # game over
        if player.y > HEIGHT:
            game_over = True

    # =========================
    # DRAW
    # =========================

    screen.fill(SKY)

    # clouds
    pygame.draw.circle(screen, WHITE, (80, 100), 30)
    pygame.draw.circle(screen, WHITE, (120, 100), 25)

    # platforms
    for platform in platforms:

        pygame.draw.rect(screen, GREEN, platform)

        pygame.draw.rect(
            screen,
            DARK_GREEN,
            platform,
            3
        )

    # enemies
    for enemy in enemies:

        pygame.draw.rect(screen, RED, enemy)

        pygame.draw.rect(screen, BLACK, enemy, 2)

    # boosters
    for booster in boosters:

        pygame.draw.rect(screen, YELLOW, booster)

        pygame.draw.rect(screen, BLACK, booster, 2)

    # player
    pygame.draw.rect(screen, BLUE, player)

    pygame.draw.rect(screen, BLACK, player, 3)

    # eyes
    pygame.draw.rect(
        screen,
        WHITE,
        (player.x + 6, player.y + 8, 5, 5)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (player.x + 18, player.y + 8, 5, 5)
    )

    # score
    score_text = font.render(
        f"Score: {score}",
        True,
        BLACK
    )

    screen.blit(score_text, (10, 10))

    # game over
    if game_over:

        over_text = font.render(
            "GAME OVER",
            True,
            RED
        )

        restart_text = pygame.font.SysFont(
            "consolas",
            20
        ).render(
            "Close window to exit",
            True,
            BLACK
        )

        screen.blit(
            over_text,
            (WIDTH // 2 - 100, HEIGHT // 2)
        )

        screen.blit(
            restart_text,
            (WIDTH // 2 - 110, HEIGHT // 2 + 40)
        )

    pygame.display.update()

pygame.quit()