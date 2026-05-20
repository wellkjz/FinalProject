import pygame
from settings import BLACK, RED, GRAY, DARK_RED, GOLD, WIDTH, HEIGHT, ENEMY_SCORE_THRESHOLD

_COIN_DARK = (139, 90, 10)


def _pill(surface, rect, color=(10, 10, 30), alpha=175, r=8):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=r)
    surface.blit(s, rect.topleft)


def _load_font(size, bold=False):
    for name in ("Consolas", "Courier New", "Lucida Console", "monospace"):
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except Exception:
            pass
    return pygame.font.Font(None, size + 8)


class HUD:
    def __init__(self, screen, font=None, font_small=None):
        self.screen     = screen
        self.font       = _load_font(18, bold=True)
        self.font_small = _load_font(13)
        self.font_label = _load_font(11)
        self._heart_surf = self._make_heart(18)

    @staticmethod
    def _make_heart(size):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        r  = size // 4
        cx = size // 2
        pygame.draw.circle(surf, RED,       (cx - r, r + 1), r)
        pygame.draw.circle(surf, RED,       (cx + r, r + 1), r)
        pygame.draw.polygon(surf, RED, [(1, r+1),(cx, size-1),(size-1, r+1)])
        return surf

    def draw(self, score, best_score, lives, coins):
        self._draw_score_panel(score, best_score)
        self._draw_lives(lives)
        self._draw_coins(coins)
        self._draw_enemy_hint(score)

    def _draw_score_panel(self, score, best):
        pad   = 8
        lbl_s = self.font_label.render("SCORE", True, (170, 190, 220))
        val_s = self.font.render(f"{score:,}", True, GOLD)
        lbl_b = self.font_label.render("BEST",  True, (170, 190, 220))
        val_b = self.font_small.render(f"{best:,}", True, (180, 220, 255))
        w = max(lbl_s.get_width(), val_s.get_width(),
                lbl_b.get_width(), val_b.get_width()) + pad * 2
        h = (lbl_s.get_height() + val_s.get_height() +
             lbl_b.get_height() + val_b.get_height() + pad * 2 + 12)
        rect = pygame.Rect(8, 8, w, h)
        _pill(self.screen, rect)
        y = rect.y + pad
        self.screen.blit(lbl_s, (rect.x + pad, y)); y += lbl_s.get_height() + 1
        self.screen.blit(val_s, (rect.x + pad, y)); y += val_s.get_height() + 5
        pygame.draw.line(self.screen, (60, 70, 100),
                         (rect.x + pad, y), (rect.right - pad, y), 1)
        y += 4
        self.screen.blit(lbl_b, (rect.x + pad, y)); y += lbl_b.get_height() + 1
        self.screen.blit(val_b, (rect.x + pad, y))

    def _draw_lives(self, lives):
        size = self._heart_surf.get_width()
        gap  = 5
        n    = 3
        total_w = n * size + (n - 1) * gap
        x0 = WIDTH - total_w - 14
        y0 = 12
        _pill(self.screen, pygame.Rect(x0 - 7, y0 - 5, total_w + 14, size + 10))
        for i in range(n):
            x = x0 + i * (size + gap)
            if i < lives:
                self.screen.blit(self._heart_surf, (x, y0))
            else:
                empty = pygame.Surface((size, size), pygame.SRCALPHA)
                r, cx = size // 4, size // 2
                dim = (80, 30, 30)
                pygame.draw.circle(empty, dim, (cx - r, r + 1), r)
                pygame.draw.circle(empty, dim, (cx + r, r + 1), r)
                pygame.draw.polygon(empty, dim, [(1,r+1),(cx,size-1),(size-1,r+1)])
                self.screen.blit(empty, (x, y0))

    def _draw_coins(self, coins):
        pad      = 8
        icon_r   = 7
        coin_txt = self.font_small.render(f"x {coins}", True, GOLD)
        total_w  = icon_r * 2 + 6 + coin_txt.get_width() + pad * 2
        pill     = pygame.Rect(WIDTH - total_w - 8, 44,
                               total_w, coin_txt.get_height() + 8)
        _pill(self.screen, pill, color=(50, 35, 0))
        cx = pill.x + pad + icon_r
        cy = pill.y + pill.height // 2
        pygame.draw.circle(self.screen, GOLD,      (cx, cy), icon_r)
        pygame.draw.circle(self.screen, _COIN_DARK,(cx, cy), icon_r, 2)
        self.screen.blit(coin_txt, (cx + icon_r + 5, pill.y + 4))

    def _draw_enemy_hint(self, score):
        if score >= ENEMY_SCORE_THRESHOLD:
            return
        remaining = ENEMY_SCORE_THRESHOLD - score
        txt  = self.font_label.render(
            f"Birds appear at {ENEMY_SCORE_THRESHOLD}  ({remaining} to go)",
            True, (255, 160, 80))
        pad  = 6
        pill = pygame.Rect(WIDTH // 2 - txt.get_width() // 2 - pad,
                           HEIGHT - 30,
                           txt.get_width() + pad * 2,
                           txt.get_height() + 6)
        _pill(self.screen, pill, color=(60, 20, 0))
        self.screen.blit(txt, (pill.x + pad, pill.y + 3))

    def draw_hearts(self, lives, x=None, y=None, size=22, surface=None):
        """Backward-compat: old callers pass just `lives`."""
        surf  = surface or self.screen
        heart = pygame.transform.scale(self._heart_surf, (size, size))
        gap   = 6
        x0    = x if x is not None else WIDTH // 2 - (3 * (size + gap)) // 2
        y0    = y if y is not None else HEIGHT // 2
        for i in range(lives):
            surf.blit(heart, (x0 + i * (size + gap), y0))