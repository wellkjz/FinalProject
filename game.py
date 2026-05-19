
import pygame
import random

from settings import (
    WIDTH, HEIGHT, FPS, GRAVITY, SKY, BOOST_VEL,
    ENEMY_SCORE_THRESHOLD,
    ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX,
    SOUND_JUMP, SOUND_COIN, SOUND_BAD, SOUND_BOOST,
)
from entities.player import Player
from entities.enemy import Enemy
from systems.scoring import ScoreSystem
from systems.level_generator import LevelGenerator
from systems.save_system import SaveSystem
from ui.hud import HUD
from ui.menu import MenuScreen
from ui.game_over import GameOverScreen


def _load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jump Game")
        self.clock  = pygame.time.Clock()

        self.background = pygame.image.load("assets/background.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        font       = pygame.font.SysFont("consolas", 24)
        font_small = pygame.font.SysFont("consolas", 18)

        # Sounds
        self.snd_jump  = _load_sound(SOUND_JUMP)
        self.snd_coin  = _load_sound(SOUND_COIN)
        self.snd_bad   = _load_sound(SOUND_BAD)
        self.snd_boost = _load_sound(SOUND_BOOST)

        # Systems
        self.save_sys   = SaveSystem()
        self.best_score, self.total_coins = self.save_sys.load()


        # UI
        self.hud = HUD(self.screen, font, font_small)
        self.menu_screen = MenuScreen(self.screen, font, font_small)
        self.gameover_screen = GameOverScreen(self.screen, font, font_small)

        self.state   = "menu"
        self.scoring = ScoreSystem()
        self.scoring.coins = self.total_coins
        self.level   = LevelGenerator()
        self.player  = None
        self.enemies = []
        self._spawn_timer    = 0
        self._spawn_interval = ENEMY_SPAWN_INTERVAL_MIN

    # ========================
    # RESET
    # ========================
    def reset_game(self):
        self.player  = Player(WIDTH // 2, HEIGHT - 120)
        self.level   = LevelGenerator()
        self.enemies = []
        self.scoring.reset()
        self.level.generate_world()
        self._spawn_timer    = 0
        self._spawn_interval = random.randint(
            ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX
        )

    # ========================
    # ENEMY SPAWN
    # ========================
    def _try_spawn_enemy(self):
        if self.scoring.score < ENEMY_SCORE_THRESHOLD:
            return
        self._spawn_timer += 1
        if self._spawn_timer >= self._spawn_interval:
            self._spawn_timer    = 0
            self._spawn_interval = random.randint(
                ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX
            )
            self.enemies.append(Enemy(random.randint(60, HEIGHT - 100)))

    # ========================
    # UPDATE
    # ========================
    def update(self):
        self.level.update()
        self.player.tick(GRAVITY)

        # Platform collision
        for p in self.level.platforms:
            if self.player.rect.colliderect(p.rect) and self.player.vel_y > 0:
                self.player.jump()
                if self.snd_jump:
                    self.snd_jump.play()

        # Coin collision
        for c in self.level.coins[:]:

            if self.player.rect.colliderect(c.rect):

                # GOLD STAR (+1000)
                if c.kind == "gold":
                    self.scoring.score += 1000

                    if self.snd_coin:
                        self.snd_coin.play()

                # BLUE STAR (-200)
                elif c.kind == "blue":
                    self.scoring.score -= 200

                    if self.snd_bad:
                        self.snd_bad.play()

                # PURPLE STAR (BOOST)
                elif c.kind == "purple":
                    self.player.vel_y = BOOST_VEL

                    if self.snd_boost:
                        self.snd_boost.play()

                # REAL COIN
                elif c.kind == "coin":
                    self.scoring.coins += 5

                    if self.snd_coin:
                        self.snd_coin.play()

                self.level.coins.remove(c)

        # Booster collision
        for b in self.level.boosters[:]:
            if self.player.rect.colliderect(b.rect):
                self.player.vel_y = BOOST_VEL
                if self.snd_boost:
                    self.snd_boost.play()
                self.level.boosters.remove(b)

        # Enemies
        self._try_spawn_enemy()
        for e in self.enemies[:]:
            e.update()
            if self.player.rect.colliderect(e.rect) and not self.player.is_invincible:
                self.player.take_hit()
                if self.snd_bad:
                    self.snd_bad.play()
                if not self.player.is_alive:
                    self._end_game()
                    return
            if e.is_offscreen():
                self.enemies.remove(e)

        # Camera scroll
        if self.player.rect.y < HEIGHT // 3:
            diff = HEIGHT // 3 - self.player.rect.y
            self.player.rect.y = HEIGHT // 3
            self.scoring.add_scroll(diff)
            self.level.scroll(diff)
            for e in self.enemies:
                e.rect.y += diff

        self.level.cleanup()
        self.level.extend()

        if self.player.rect.y > HEIGHT:
            self._end_game()

    def _end_game(self):
        self.state = "game_over"
        if self.scoring.score > self.best_score:
            self.best_score = self.scoring.score
        self.save_sys.save(self.best_score, self.scoring.coins)
    # ========================
    # DRAW
    # ========================
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.level.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        self.player.draw(self.screen)
        self.hud.draw(self.scoring.score, self.best_score, self.player.lives, self.scoring.coins)

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
                            self.best_score = 0
                            self.save_sys.clear()

            if self.state == "menu":
                self.menu_screen.draw(self.hud.draw_hearts)
            elif self.state == "game_over":
                self.gameover_screen.draw(
                    self.scoring.score, self.best_score, self.hud.draw_hearts
                )
            else:
                self.update()
                self.draw()

            pygame.display.update()

        pygame.quit()