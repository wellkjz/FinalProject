import pygame
import random
import os

pygame.init()
pygame.mixer.init()

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
PURPLE = (180, 70, 255)
GOLD = (255, 215, 0)
RED = (220, 70, 70)
SKY = (135, 206, 235)
BLACK = (0, 0, 0)
BROWN = (120, 70, 30)
GRAY = (180, 180, 180)
DARK_RED = (160, 30, 30)

ENEMY_SCORE_THRESHOLD = 2000
ENEMY_SPAWN_INTERVAL_MIN = 120  # frames
ENEMY_SPAWN_INTERVAL_MAX = 300  # frames
INVINCIBILITY_FRAMES = 90       # ~1.5 seconds of invincibility after hit


def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jump Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 24)
        self.font_small = pygame.font.SysFont("consolas", 18)

        self.jump_sound = load_sound("sounds/jump.wav")
        self.coin_sound = load_sound("sounds/coin.wav")
        self.bad_sound = load_sound("sounds/bad.wav")
        self.boost_sound = load_sound("sounds/boost.wav")

        self.state = "menu"

        self.best_score = self.load_best_score()

        self.reset_game()

    # =========================
    # SAVE SYSTEM
    # =========================

    def clear_best_score(self):

        self.best_score = 0

        with open("best_score.txt", "w") as f:
            f.write("0")

    def load_best_score(self):

        if not os.path.exists("best_score.txt"):
            return 0

        with open("best_score.txt", "r") as f:
            return int(f.read())

    def save_best_score(self):

        with open("best_score.txt", "w") as f:
            f.write(str(self.best_score))

    # =========================
    # RESET GAME
    # =========================

    def reset_game(self):

        self.player = pygame.Rect(WIDTH // 2, HEIGHT - 120, 25, 25)

        self.vel_y = 0

        self.score = 0

        self.lives = 3
        self.invincibility_timer = 0

        self.platforms = []
        self.stars = []
        self.enemies = []

        self.gravity = GRAVITY

        # Timer for random enemy spawning
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = random.randint(
            ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX
        )

        self.generate_world()

    # =========================
    # STAR
    # =========================

    class Star:

        def __init__(self, x, y, kind):
            self.rect = pygame.Rect(x, y, 18, 18)
            self.kind = kind

        def draw(self, screen):

            if self.kind == "gold":
                color = GOLD
            elif self.kind == "blue":
                color = BLUE
            else:
                color = PURPLE

            cx, cy = self.rect.center

            points = [
                (cx, cy - 10),
                (cx + 3, cy - 3),
                (cx + 10, cy - 3),
                (cx + 5, cy + 2),
                (cx + 7, cy + 10),
                (cx, cy + 5),
                (cx - 7, cy + 10),
                (cx - 5, cy + 2),
                (cx - 10, cy - 3),
                (cx - 3, cy - 3)
            ]

            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, BLACK, points, 2)

    # =========================
    # ENEMY (BIRD)
    # =========================

    class Enemy:

        def __init__(self, y):

            self.width = 35
            self.height = 20

            self.direction = random.choice(["left", "right"])

            if self.direction == "left":
                self.x = WIDTH
                self.speed = random.randint(3, 6) * -1
            else:
                self.x = -40
                self.speed = random.randint(3, 6)

            self.y = y

            self.rect = pygame.Rect(
                self.x,
                self.y,
                self.width,
                self.height
            )

        def update(self):

            self.rect.x += self.speed

        def draw(self, screen):

            body = pygame.Rect(
                self.rect.x,
                self.rect.y,
                self.width,
                self.height
            )

            wing1 = [
                (self.rect.x + 5, self.rect.y + 10),
                (self.rect.x - 5, self.rect.y),
                (self.rect.x + 10, self.rect.y + 5)
            ]

            wing2 = [
                (self.rect.x + 25, self.rect.y + 10),
                (self.rect.x + 40, self.rect.y),
                (self.rect.x + 20, self.rect.y + 5)
            ]

            pygame.draw.ellipse(screen, BROWN, body)
            pygame.draw.polygon(screen, BLACK, wing1)
            pygame.draw.polygon(screen, BLACK, wing2)

    # =========================
    # CREATE OBJECTS
    # =========================

    def create_pair(self, y):

        left = pygame.Rect(LEFT_X, y, PLATFORM_W, PLATFORM_H)
        right = pygame.Rect(RIGHT_X, y, PLATFORM_W, PLATFORM_H)

        self.platforms.append(left)
        self.platforms.append(right)

        kinds = ["gold", "blue"]

        if random.random() < 0.3:
            kinds[random.randint(0, 1)] = "purple"

        self.stars.append(self.Star(LEFT_X + 30, y - 20, kinds[0]))
        self.stars.append(self.Star(RIGHT_X + 30, y - 20, kinds[1]))

    def create_single(self, y):

        x = random.randint(40, WIDTH - 120)

        self.platforms.append(
            pygame.Rect(x, y, PLATFORM_W, PLATFORM_H)
        )

    def generate_world(self):

        self.platforms.append(
            pygame.Rect(WIDTH // 2 - 40, HEIGHT - 60, PLATFORM_W, PLATFORM_H)
        )

        y = HEIGHT - 60 - GAP_Y

        for i in range(11):

            if random.random() < 0.3:
                self.create_pair(y)
            else:
                self.create_single(y)

            y -= GAP_Y

    # =========================
    # SPAWN RANDOM ENEMY
    # =========================

    def try_spawn_enemy(self):
        """Spawn a bird at a random Y position visible on screen."""

        if self.score < ENEMY_SCORE_THRESHOLD:
            return

        self.enemy_spawn_timer += 1

        if self.enemy_spawn_timer >= self.enemy_spawn_interval:

            self.enemy_spawn_timer = 0
            self.enemy_spawn_interval = random.randint(
                ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX
            )

            # Spawn at a random vertical position within the visible screen
            spawn_y = random.randint(60, HEIGHT - 100)
            self.enemies.append(self.Enemy(spawn_y))

    # =========================
    # DRAW HEARTS
    # =========================

    def draw_hearts(self):
        """Draw 3 hearts in the top-right corner."""

        heart_size = 20
        spacing = 26
        start_x = WIDTH - 10 - (3 * spacing)
        y = 12

        for i in range(3):
            x = start_x + i * spacing
            cx = x + heart_size // 2
            cy = y + heart_size // 2

            color = RED if i < self.lives else GRAY

            # Draw heart shape using two circles + triangle
            r = heart_size // 4

            pygame.draw.circle(self.screen, color, (cx - r, cy - 2), r)
            pygame.draw.circle(self.screen, color, (cx + r, cy - 2), r)
            pygame.draw.polygon(self.screen, color, [
                (cx - heart_size // 2, cy),
                (cx + heart_size // 2, cy),
                (cx, cy + heart_size // 2)
            ])

    # =========================
    # UPDATE
    # =========================

    def update(self):

        # Tick invincibility
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.player.x -= PLAYER_SPEED

        if keys[pygame.K_RIGHT]:
            self.player.x += PLAYER_SPEED

        if self.player.x < -30:
            self.player.x = WIDTH

        if self.player.x > WIDTH:
            self.player.x = -30

        self.vel_y += self.gravity
        self.player.y += self.vel_y

        # PLATFORM COLLISION
        for p in self.platforms:

            if self.player.colliderect(p) and self.vel_y > 0:

                self.vel_y = JUMP_FORCE

                if self.jump_sound:
                    self.jump_sound.play()

        # STAR COLLISION
        for s in self.stars[:]:

            if self.player.colliderect(s.rect):

                if s.kind == "gold":

                    self.score += 1000

                    if self.coin_sound:
                        self.coin_sound.play()

                elif s.kind == "blue":

                    self.score -= 200

                    if self.bad_sound:
                        self.bad_sound.play()

                    if self.score < 0:
                        self.score = 0

                elif s.kind == "purple":

                    self.vel_y = -25

                    if self.boost_sound:
                        self.boost_sound.play()

                self.stars.remove(s)

        # TRY SPAWN RANDOM ENEMY
        self.try_spawn_enemy()

        # ENEMY UPDATE
        for enemy in self.enemies[:]:

            enemy.update()

            # HIT PLAYER (only if not invincible)
            if self.player.colliderect(enemy.rect) and self.invincibility_timer == 0:

                self.lives -= 1
                self.invincibility_timer = INVINCIBILITY_FRAMES

                if self.bad_sound:
                    self.bad_sound.play()

                if self.lives <= 0:

                    self.state = "game_over"

                    if self.score > self.best_score:
                        self.best_score = self.score
                        self.save_best_score()

            # REMOVE ENEMY
            if enemy.rect.x < -100 or enemy.rect.x > WIDTH + 100:
                self.enemies.remove(enemy)

        # CAMERA MOVEMENT
        if self.player.y < HEIGHT // 3:

            diff = HEIGHT // 3 - self.player.y

            self.player.y = HEIGHT // 3

            self.score += diff

            for p in self.platforms:
                p.y += diff

            for s in self.stars:
                s.rect.y += diff

            for enemy in self.enemies:
                enemy.rect.y += diff

        # REMOVE OLD OBJECTS
        self.platforms = [p for p in self.platforms if p.y < HEIGHT]
        self.stars = [s for s in self.stars if s.rect.y < HEIGHT]
        self.enemies = [e for e in self.enemies if e.rect.y < HEIGHT]

        # GENERATE NEW PLATFORMS
        while len(self.platforms) < 18:

            highest = min(self.platforms, key=lambda p: p.y)

            new_y = highest.y - GAP_Y

            if random.random() < 0.25:
                self.create_pair(new_y)
            else:
                self.create_single(new_y)

        # GAME OVER (fell off screen)
        if self.player.y > HEIGHT:

            self.state = "game_over"

            if self.score > self.best_score:
                self.best_score = self.score
                self.save_best_score()

    # =========================
    # DRAW
    # =========================

    def draw(self):

        self.screen.fill(SKY)

        # PLATFORMS
        for p in self.platforms:
            pygame.draw.rect(self.screen, GREEN, p)
            pygame.draw.rect(self.screen, DARK_GREEN, p, 2)

        # STARS
        for s in self.stars:
            s.draw(self.screen)

        # ENEMIES
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # PLAYER — blink when invincible
        if self.invincibility_timer == 0 or (self.invincibility_timer // 6) % 2 == 0:
            pygame.draw.rect(self.screen, RED, self.player)
            pygame.draw.rect(self.screen, BLACK, self.player, 2)

        # TEXT
        self.screen.blit(
            self.font.render(f"Score: {self.score}", True, BLACK),
            (10, 10)
        )

        self.screen.blit(
            self.font.render(f"Best: {self.best_score}", True, BLACK),
            (10, 40)
        )

        # HEARTS
        self.draw_hearts()

        # HINT: birds appear after 5000
        if self.score < ENEMY_SCORE_THRESHOLD:
            remaining = ENEMY_SCORE_THRESHOLD - self.score
            hint = self.font_small.render(
                f"Birds at {ENEMY_SCORE_THRESHOLD}! ({remaining} away)", True, DARK_RED
            )
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))

    # =========================
    # MENU
    # =========================

    def draw_menu(self):

        self.screen.fill(SKY)

        title = self.font.render("JUMP GAME", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))

        start = self.font.render("SPACE - START", True, BLACK)
        self.screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 280))

        info = self.font_small.render("Avoid birds! You have 3 lives.", True, DARK_RED)
        self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 340))

        # Draw example hearts
        self.lives = 3
        self.draw_hearts()

    # =========================
    # GAME OVER
    # =========================

    def draw_game_over(self):

        self.screen.fill(SKY)

        go = self.font.render("GAME OVER", True, RED)
        self.screen.blit(go, (WIDTH // 2 - go.get_width() // 2, 160))

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 210))

        best_text = self.font.render(f"Best: {self.best_score}", True, BLACK)
        self.screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, 240))

        restart = self.font.render("SPACE - Restart", True, BLACK)
        self.screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 300))

        menu = self.font.render("ENTER - Menu", True, BLACK)
        self.screen.blit(menu, (WIDTH // 2 - menu.get_width() // 2, 340))

        clr = self.font_small.render("BACKSPACE - Clear Best", True, BLACK)
        self.screen.blit(clr, (WIDTH // 2 - clr.get_width() // 2, 385))

        # Show 0 hearts on game over
        self.lives = 0
        self.draw_hearts()

    # =========================
    # MAIN LOOP
    # =========================

    def run(self):

        running = True

        while running:

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    # MENU
                    if self.state == "menu":

                        if event.key == pygame.K_SPACE:

                            self.reset_game()
                            self.state = "playing"

                    # GAME OVER
                    elif self.state == "game_over":

                        # RESTART
                        if event.key == pygame.K_SPACE:

                            self.reset_game()
                            self.state = "playing"

                        # MENU
                        elif event.key == pygame.K_RETURN:

                            self.state = "menu"

                        # CLEAR SCORE
                        elif event.key == pygame.K_BACKSPACE:

                            self.clear_best_score()

            # DRAW STATES
            if self.state == "menu":

                self.draw_menu()

            elif self.state == "game_over":

                self.draw_game_over()

            else:

                self.update()
                self.draw()

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()