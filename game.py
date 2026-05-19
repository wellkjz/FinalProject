import pygame
import random
import os

from settings import (
    WIDTH, HEIGHT, FPS,
    GRAVITY, JUMP_FORCE, PLAYER_SPEED,
    PLATFORM_W, PLATFORM_H, GAP_Y, LEFT_X, RIGHT_X,
    GREEN, DARK_GREEN, BLUE, PURPLE, GOLD,
    RED, DARK_RED, SKY, BLACK, GRAY, BROWN,
    ENEMY_SCORE_THRESHOLD,
    ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX,
    INVINCIBILITY_FRAMES,
)
from enemy import Enemy

pygame.init()
pygame.mixer.init()


def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


# ========================
# STAR
# ========================
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
            (cx,      cy - 10),
            (cx + 3,  cy - 3),
            (cx + 10, cy - 3),
            (cx + 5,  cy + 2),
            (cx + 7,  cy + 10),
            (cx,      cy + 5),
            (cx - 7,  cy + 10),
            (cx - 5,  cy + 2),
            (cx - 10, cy - 3),
            (cx - 3,  cy - 3),
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 2)


# ========================
# GAME
# ========================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jump Game")
        self.clock = pygame.time.Clock()
        self.font       = pygame.font.SysFont("consolas", 24)
        self.font_small = pygame.font.SysFont("consolas", 18)

        self.jump_sound  = load_sound("sounds/jump.wav")
        self.coin_sound  = load_sound("sounds/coin.wav")
        self.bad_sound   = load_sound("sounds/bad.wav")
        self.boost_sound = load_sound("sounds/boost.wav")

        self.state      = "menu"
        self.best_score = self.load_best_score()
        self.reset_game()

    # ========================
    # SAVE SYSTEM
    # ========================
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

    # ========================
    # RESET
    # ========================
    def reset_game(self):
        self.player = pygame.Rect(WIDTH // 2, HEIGHT - 120, 25, 25)
        self.vel_y  = 0
        self.score  = 0
        self.lives  = 3
        self.invincibility_timer = 0

        self.platforms = []
        self.stars     = []
        self.enemies   = []
        self.gravity   = GRAVITY

        self.enemy_spawn_timer    = 0
        self.enemy_spawn_interval = random.randint(
            ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX
        )
        self.generate_world()

    # ========================
    # CREATE OBJECTS
    # ========================
    def create_pair(self, y):
        left  = pygame.Rect(LEFT_X,  y, PLATFORM_W, PLATFORM_H)
        right = pygame.Rect(RIGHT_X, y, PLATFORM_W, PLATFORM_H)
        self.platforms.append(left)
        self.platforms.append(right)

        kinds = ["gold", "blue"]
        if random.random() < 0.3:
            kinds[random.randint(0, 1)] = "purple"

        self.stars.append(Star(LEFT_X  + 30, y - 20, kinds[0]))
        self.stars.append(Star(RIGHT_X + 30, y - 20, kinds[1]))

    def create_single(self, y):
        x = random.randint(40, WIDTH - 120)
        self.platforms.append(pygame.Rect(x, y, PLATFORM_W, PLATFORM_H))

    def generate_world(self):
        self.platforms.append(
            pygame.Rect(WIDTH // 2 - 40, HEIGHT - 60, PLATFORM_W, PLATFORM_H)
        )
        y = HEIGHT - 60 - GAP_Y
        for _ in range(11):
            if random.random() < 0.3:
                self.create_pair(y)
            else:
                self.create_single(y)
            y -= GAP_Y

    # ========================
    # SPAWN ENEMY
    # ========================
    def try_spawn_enemy(self):
        if self.score < ENEMY_SCORE_THRESHOLD:
            return

        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.enemy_spawn_timer    = 0
            self.enemy_spawn_interval = random.randint(
                ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX
            )
            spawn_y = random.randint(60, HEIGHT - 100)
            self.enemies.append(Enemy(spawn_y))

    # ========================
    # DRAW HEARTS
    # ========================
    def draw_hearts(self):
        heart_size = 20
        spacing    = 26
        start_x    = WIDTH - 10 - (3 * spacing)
        y          = 12

        for i in range(3):
            x  = start_x + i * spacing
            cx = x + heart_size // 2
            cy = y + heart_size // 2
            color = RED if i < self.lives else GRAY
            r = heart_size // 4
            pygame.draw.circle(self.screen, color, (cx - r, cy - 2), r)
            pygame.draw.circle(self.screen, color, (cx + r, cy - 2), r)
            pygame.draw.polygon(self.screen, color, [
                (cx - heart_size // 2, cy),
                (cx + heart_size // 2, cy),
                (cx, cy + heart_size // 2),
            ])

    # ========================
    # UPDATE
    # ========================
    def update(self):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player.x += PLAYER_SPEED

        # Wrap around
        if self.player.x < -30:
            self.player.x = WIDTH
        if self.player.x > WIDTH:
            self.player.x = -30

        self.vel_y     += self.gravity
        self.player.y  += self.vel_y

        # Platform collision
        for p in self.platforms:
            if self.player.colliderect(p) and self.vel_y > 0:
                self.vel_y = JUMP_FORCE
                if self.jump_sound:
                    self.jump_sound.play()

        # Star collision
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

        # Spawn enemy
        self.try_spawn_enemy()

        # Enemy update + collision
        for enemy in self.enemies[:]:
            enemy.update()
            if self.player.colliderect(enemy.rect) and self.invincibility_timer == 0:
                self.lives -= 1
                self.invincibility_timer = INVINCIBILITY_FRAMES
                if self.bad_sound:
                    self.bad_sound.play()
                if self.lives <= 0:
                    self._end_game()
                    return
            if enemy.rect.x < -100 or enemy.rect.x > WIDTH + 100:
                self.enemies.remove(enemy)

        # Camera scroll
        if self.player.y < HEIGHT // 3:
            diff = HEIGHT // 3 - self.player.y
            self.player.y = HEIGHT // 3
            self.score += diff
            for p in self.platforms:
                p.y += diff
            for s in self.stars:
                s.rect.y += diff
            for e in self.enemies:
                e.rect.y += diff

        # Remove off-screen objects
        self.platforms = [p for p in self.platforms if p.y < HEIGHT]
        self.stars     = [s for s in self.stars     if s.rect.y < HEIGHT]
        self.enemies   = [e for e in self.enemies   if e.rect.y < HEIGHT]

        # Generate new platforms
        while len(self.platforms) < 18:
            highest = min(self.platforms, key=lambda p: p.y)
            new_y   = highest.y - GAP_Y
            if random.random() < 0.25:
                self.create_pair(new_y)
            else:
                self.create_single(new_y)

        # Fell off screen
        if self.player.y > HEIGHT:
            self._end_game()

    def _end_game(self):
        self.state = "game_over"
        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()

    # ========================
    # DRAW
    # ========================
    def draw(self):
        self.screen.fill(SKY)

        for p in self.platforms:
            pygame.draw.rect(self.screen, GREEN, p)
            pygame.draw.rect(self.screen, DARK_GREEN, p, 2)

        for s in self.stars:
            s.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Player (blinks when invincible)
        if self.invincibility_timer == 0 or (self.invincibility_timer // 6) % 2 == 0:
            pygame.draw.rect(self.screen, RED,   self.player)
            pygame.draw.rect(self.screen, BLACK, self.player, 2)

        self.screen.blit(
            self.font.render(f"Score: {self.score}", True, BLACK), (10, 10)
        )
        self.screen.blit(
            self.font.render(f"Best: {self.best_score}", True, BLACK), (10, 40)
        )

        self.draw_hearts()

        if self.score < ENEMY_SCORE_THRESHOLD:
            remaining = ENEMY_SCORE_THRESHOLD - self.score
            hint = self.font_small.render(
                f"Birds at {ENEMY_SCORE_THRESHOLD}! ({remaining} away)", True, DARK_RED
            )
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))

    # ========================
    # MENU
    # ========================
    def draw_menu(self):
        self.screen.fill(SKY)
        title = self.font.render("JUMP GAME", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))

        start = self.font.render("SPACE - START", True, BLACK)
        self.screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 280))

        info = self.font_small.render("Avoid birds! You have 3 lives.", True, DARK_RED)
        self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 340))

        self.lives = 3
        self.draw_hearts()

    # ========================
    # GAME OVER
    # ========================
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

        self.lives = 0
        self.draw_hearts()

    # ========================
    # MAIN LOOP
    # ========================
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if self.state == "menu":
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.state = "playing"

                    elif self.state == "game_over":
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.state = "playing"
                        elif event.key == pygame.K_RETURN:
                            self.state = "menu"
                        elif event.key == pygame.K_BACKSPACE:
                            self.clear_best_score()

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "game_over":
                self.draw_game_over()
            else:
                self.update()
                self.draw()

            pygame.display.update()

        pygame.quit()