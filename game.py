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
from systems.shop_system import ShopSystem
from ui.hud import HUD
from ui.menu import MenuScreen
from ui.game_over import GameOverScreen
from ui.shop import ShopScreen


def _load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


def _load_bg(path: str) -> pygame.Surface:
    try:
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    except Exception:
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill(SKY)
        return surf


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jump Game")
        self.clock = pygame.time.Clock()

        font       = pygame.font.SysFont("consolas", 24)
        font_small = pygame.font.SysFont("consolas", 18)

        # Sounds
        self.snd_jump  = _load_sound(SOUND_JUMP)
        self.snd_coin  = _load_sound(SOUND_COIN)
        self.snd_bad   = _load_sound(SOUND_BAD)
        self.snd_boost = _load_sound(SOUND_BOOST)

        # Systems  ← save_sys FIRST, then shop_sys
        self.save_sys             = SaveSystem()
        self.best_score, self.total_coins = self.save_sys.load()
        self.shop_sys             = ShopSystem(self.save_sys)

        # UI
        self.hud             = HUD(self.screen, font, font_small)
        self.menu_screen     = MenuScreen(self.screen, font, font_small)
        self.gameover_screen = GameOverScreen(self.screen, font, font_small)
        self.shop_screen     = ShopScreen(self.screen, self.shop_sys)

        self.state   = "menu"
        self.scoring = ScoreSystem()
        self.scoring.coins = self.total_coins
        self.level   = LevelGenerator()
        self.player  = None
        self.enemies = []
        self._spawn_timer    = 0
        self._spawn_interval = ENEMY_SPAWN_INTERVAL_MIN

        # Background & music — loaded from the equipped background item
        self._current_bg_id = None
        self.background     = None
        self._apply_equipped_bg()   # load background + start music

    # ================================================================== #
    #  Background / music helpers                                          #
    # ================================================================== #
    def _apply_equipped_bg(self):
        """Load the background surface and play its music track."""
        bg_item = self.shop_sys.get_equipped_bg()
        if bg_item["id"] == self._current_bg_id:
            return  # nothing changed
        self._current_bg_id = bg_item["id"]
        self.background = _load_bg(bg_item["image"])
        self._start_music(bg_item.get("music"))

    @staticmethod
    def _start_music(path):
        """Stop current music and play a new track, or stop if path is None."""
        pygame.mixer.music.stop()
        if not path:
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)   # loop indefinitely
        except Exception:
            pass  # file missing — play silently

    # ================================================================== #
    #  RESET                                                               #
    # ================================================================== #
    def reset_game(self):
        char_item = self.shop_sys.get_equipped_char()
        self.player  = Player(
            WIDTH // 2, HEIGHT - 120,
            skin_path=char_item["image"],
            scale=char_item["scale"],
        )
        self.level   = LevelGenerator()
        self.enemies = []
        self.scoring.reset()
        self.level.generate_world()
        self._spawn_timer    = 0
        self._spawn_interval = random.randint(
            ENEMY_SPAWN_INTERVAL_MIN, ENEMY_SPAWN_INTERVAL_MAX
        )
        # Make sure background / music match the latest equipped item
        self._apply_equipped_bg()

    # ================================================================== #
    #  ENEMY SPAWN                                                         #
    # ================================================================== #
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

    # ================================================================== #
    #  UPDATE                                                              #
    # ================================================================== #
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
            if self.player.collect_rect.colliderect(c.rect):
                if c.kind == "gold":
                    self.scoring.score += 1000
                    if self.snd_coin:
                        self.snd_coin.play()
                elif c.kind == "blue":
                    self.scoring.score -= 200
                    if self.snd_bad:
                        self.snd_bad.play()
                elif c.kind == "purple":
                    self.player.vel_y = BOOST_VEL
                    if self.snd_boost:
                        self.snd_boost.play()
                elif c.kind == "coin":
                    self.scoring.coins += 5
                    if self.snd_coin:
                        self.snd_coin.play()
                self.level.coins.remove(c)

        # Booster collision
        for b in self.level.boosters[:]:
            if self.player.collect_rect.colliderect(b.rect):
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

    # ================================================================== #
    #  DRAW                                                                #
    # ================================================================== #
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.level.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        self.player.draw(self.screen)
        self.hud.draw(
            self.scoring.score, self.best_score,
            self.player.lives, self.scoring.coins
        )

    # ================================================================== #
    #  MAIN LOOP                                                           #
    # ================================================================== #
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # ── mouse click in shop ─────────────────────────────────
                if event.type == pygame.MOUSEBUTTONDOWN and self.state == "shop":
                    if event.button == 1:
                        self.shop_screen.handle_click(event.pos, self.scoring)
                        # Immediately apply any bg/skin change
                        self._apply_equipped_bg()

                if event.type == pygame.KEYDOWN:
                    if self.state == "menu":
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.state = "playing"
                        if event.key == pygame.K_s:
                            self.state = "shop"

                    elif self.state == "game_over":
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.state = "playing"
                        elif event.key == pygame.K_RETURN:
                            self.state = "menu"
                        elif event.key == pygame.K_BACKSPACE:
                            self.best_score = 0
                            self.save_sys.clear()

                    elif self.state == "shop":
                        action = self.shop_screen.handle_key(event.key)
                        if action == "close":
                            # Re-apply in case the player equipped something
                            self._apply_equipped_bg()
                            self.state = "menu"

            # ── render ─────────────────────────────────────────────────
            if self.state == "menu":
                self.menu_screen.draw(self.hud.draw_hearts)
            elif self.state == "game_over":
                self.gameover_screen.draw(
                    self.scoring.score, self.best_score, self.hud.draw_hearts
                )
            elif self.state == "shop":
                self.shop_screen.draw(self.scoring.coins)
            else:
                self.update()
                self.draw()

            pygame.display.update()

        pygame.quit()