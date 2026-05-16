import pygame
import random

pygame.init()

# =========================
# SETTINGS
# =========================

WIDTH = 400
HEIGHT = 600
FPS = 60

GRAVITY = 0.5
JUMP_FORCE = -12
PLAYER_SPEED = 5

PLATFORM_W = 80
PLATFORM_H = 12
GAP_Y = 90

LEFT_X = 50
RIGHT_X = WIDTH - 130

GREEN = (70, 200, 120)
DARK_GREEN = (40, 120, 70)
BLUE = (80, 140, 255)
RED = (220, 70, 70)
GOLD = (255, 215, 0)
SKY = (135, 206, 235)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

# =========================
# STATES
# =========================

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

state = MENU

score = 0
best_score = 0

# =========================
# PLAYER
# =========================

player = pygame.Rect(WIDTH//2, HEIGHT-120, 25, 25)
vel_y = 0

# =========================
# OBJECTS
# =========================

platforms = []
stars = []

# =========================
# STAR
# =========================

class Star:
    def __init__(self, x, y, kind):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.kind = kind

    def draw(self):
        color = GOLD if self.kind == "gold" else BLUE
        pygame.draw.circle(screen, color, self.rect.center, 8)
        pygame.draw.circle(screen, BLACK, self.rect.center, 8, 2)

# =========================
# RESET GAME
# =========================

def reset_game():

    global player, vel_y, score, platforms, stars

    player = pygame.Rect(WIDTH//2, HEIGHT-120, 25, 25)
    vel_y = 0
    score = 0

    platforms = []
    stars = []

    generate_world()

# =========================
# WORLD GENERATION
# =========================

def create_pair(y):

    left = pygame.Rect(LEFT_X, y, PLATFORM_W, PLATFORM_H)
    right = pygame.Rect(RIGHT_X, y, PLATFORM_W, PLATFORM_H)

    platforms.append(left)
    platforms.append(right)

    if random.random() < 0.5:
        stars.append(Star(LEFT_X+30, y-20, "gold"))
        stars.append(Star(RIGHT_X+30, y-20, "blue"))
    else:
        stars.append(Star(RIGHT_X+30, y-20, "gold"))
        stars.append(Star(LEFT_X+30, y-20, "blue"))

def create_single(y):

    x = random.randint(40, WIDTH - 120)
    platforms.append(pygame.Rect(x, y, PLATFORM_W, PLATFORM_H))

def generate_world():

    # 🔥 ВАЖНО: первая платформа всегда под игроком
    platforms.append(
        pygame.Rect(WIDTH//2 - 40, HEIGHT - 60, PLATFORM_W, PLATFORM_H)
    )

    y = HEIGHT - 60 - GAP_Y

    for i in range(11):

        if random.random() < 0.3:
            create_pair(y)
        else:
            create_single(y)

        y -= GAP_Y

# =========================
# INIT
# =========================

generate_world()

# =========================
# LOOP
# =========================

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # =========================
    # MENU
    # =========================

    if state == MENU:

        screen.fill(SKY)

        title = font.render("JUMP GAME", True, BLACK)
        start = font.render("ENTER - Start Game", True, BLACK)

        screen.blit(title, (WIDTH//2 - 70, 200))
        screen.blit(start, (WIDTH//2 - 120, 300))

        if keys[pygame.K_RETURN]:
            reset_game()
            state = PLAYING

    # =========================
    # GAME OVER MENU
    # =========================

    elif state == GAME_OVER:

        screen.fill(SKY)

        over = font.render("GAME OVER", True, RED)
        restart = font.render("R - Restart", True, BLACK)
        menu = font.render("M - Main Menu", True, BLACK)

        screen.blit(over, (WIDTH//2 - 70, 200))
        screen.blit(restart, (WIDTH//2 - 70, 300))
        screen.blit(menu, (WIDTH//2 - 90, 340))

        if keys[pygame.K_r]:
            reset_game()
            state = PLAYING

        if keys[pygame.K_m]:
            state = MENU

    # =========================
    # GAMEPLAY
    # =========================

    elif state == PLAYING:

        screen.fill(SKY)

        # MOVE
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        # GRAVITY
        vel_y += GRAVITY
        player.y += vel_y

        # PLATFORM COLLISION
        for p in platforms:
            if player.colliderect(p) and vel_y > 0:
                vel_y = JUMP_FORCE

        # STAR COLLISION
        for s in stars[:]:
            if player.colliderect(s.rect):

                if s.kind == "gold":
                    score += 50
                    vel_y = -14
                else:
                    score += 10
                    vel_y = -10

                stars.remove(s)

        # SCROLL
        if player.y < HEIGHT // 3:

            diff = HEIGHT // 3 - player.y
            player.y = HEIGHT // 3
            score += diff

            for p in platforms:
                p.y += diff

            for s in stars:
                s.rect.y += diff

        # CLEAN
        platforms[:] = [p for p in platforms if p.y < HEIGHT]
        stars[:] = [s for s in stars if s.rect.y < HEIGHT]

        # GENERATE
        while len(platforms) < 18:

            highest = min(platforms, key=lambda p: p.y)
            new_y = highest.y - GAP_Y

            if random.random() < 0.25:
                create_pair(new_y)
            else:
                create_single(new_y)

        # GAME OVER
        if player.y > HEIGHT:
            state = GAME_OVER

            if score > best_score:
                best_score = score

        # DRAW
        for p in platforms:
            pygame.draw.rect(screen, GREEN, p)
            pygame.draw.rect(screen, DARK_GREEN, p, 2)

        for s in stars:
            s.draw()

        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, BLACK, player, 2)

        # UI
        screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Best: {best_score}", True, BLACK), (10, 40))

    pygame.display.update()

pygame.quit()