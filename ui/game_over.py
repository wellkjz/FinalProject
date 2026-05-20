import pygame
import math
from settings import SKY, BLACK, RED, GOLD, WIDTH, HEIGHT


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


class GameOverScreen:
    def __init__(self, screen, font=None, font_small=None):
        self.screen = screen
        self.tick   = 0

        self.font_big   = _load_font(38, bold=True)  # title:  26 → 38
        self.font_mid   = _load_font(22, bold=True)  # score value: 16 → 22
        self.font_small = _load_font(17)             # best value:  12 → 17
        self.font_hint  = _load_font(14)             # hint card:   10 → 14
        self.font_tiny  = _load_font(13)             # labels:      10 → 13

    def _draw_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(HEIGHT):
            t = abs(y - HEIGHT / 2) / (HEIGHT / 2)
            a = int(100 + 80 * t)
            pygame.draw.line(overlay, (25, 0, 0, a), (0, y), (WIDTH, y))
        self.screen.blit(overlay, (0, 0))

    def _draw_title(self):
        shake = int(2 * math.sin(self.tick * 0.18)) if self.tick < 50 else 0
        text  = "GAME  OVER"
        shad  = self.font_big.render(text, True, (0, 0, 0))
        main  = self.font_big.render(text, True, (255, 55, 55))
        cx    = WIDTH // 2 - main.get_width() // 2
        self.screen.blit(shad, (cx + 3 + shake, 98))
        self.screen.blit(main, (cx + shake,     95))

    def _draw_score_card(self, score, best):
        is_best = score > 0 and score >= best
        pad = 16
        cw  = 260
        # row heights based on new font sizes
        row1_h = max(self.font_tiny.get_height(), self.font_mid.get_height())
        row2_h = max(self.font_tiny.get_height(), self.font_small.get_height())
        ch = pad*2 + row1_h + 10 + row2_h + (26 if is_best else 0) + 8
        cx  = WIDTH // 2 - cw // 2
        cy  = 150

        _pill(self.screen, pygame.Rect(cx, cy, cw, ch), color=(0, 0, 40), alpha=215, r=14)

        # Score row
        lbl = self.font_tiny.render("YOUR SCORE", True, (150, 175, 215))
        val = self.font_mid.render(f"{score:,}", True, GOLD)
        y1  = cy + pad
        self.screen.blit(lbl, (cx + pad, y1 + (row1_h - lbl.get_height()) // 2))
        self.screen.blit(val, (cx + cw - val.get_width() - pad, y1))

        # Divider
        dy = cy + pad + row1_h + 5
        pygame.draw.line(self.screen, (55, 65, 95), (cx+pad, dy), (cx+cw-pad, dy), 1)

        # Best row
        lbl2 = self.font_tiny.render("BEST", True, (150, 175, 215))
        val2 = self.font_small.render(f"{best:,}", True, (175, 225, 255))
        y2   = dy + 6
        self.screen.blit(lbl2, (cx + pad, y2 + (row2_h - lbl2.get_height()) // 2))
        self.screen.blit(val2, (cx + cw - val2.get_width() - pad, y2))

        # New best badge
        if is_best:
            bob   = int(3 * math.sin(self.tick * 0.08))
            badge = self.font_tiny.render("* NEW BEST! *", True, GOLD)
            self.screen.blit(badge, (WIDTH//2 - badge.get_width()//2,
                                     cy + ch - 22 + bob))

        return cy + ch

    def _draw_hint_card(self, top_y):
        hints = [
            ("SPACE",     "Play again",  (110, 255, 130)),
            ("ENTER",     "Main menu",   (175, 205, 255)),
            ("BACKSPACE", "Clear best",  (255, 145, 100)),
        ]
        pad = 12
        lh  = 28          # was 22
        cw  = 280         # wider to fit bigger text
        cy  = top_y + 14
        cx  = WIDTH // 2 - cw // 2

        _pill(self.screen, pygame.Rect(cx, cy, cw, pad*2 + lh*len(hints)),
              color=(0, 0, 20), alpha=195, r=12)

        for i, (key, action, color) in enumerate(hints):
            y   = cy + pad + i * lh
            ks  = self.font_hint.render(key,    True, GOLD)
            as_ = self.font_hint.render(action, True, color)
            self.screen.blit(ks,  (cx + pad, y))
            self.screen.blit(as_, (cx + cw - as_.get_width() - pad, y))

    def _draw_footer(self):
        a   = int(128 + 127 * math.sin(self.tick * 0.05))
        txt = self.font_hint.render("PRESS  SPACE  TO  CONTINUE", True, (a, 255, a))
        self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT - 30))

    def draw(self, score, best_score, draw_hearts_fn=None):
        self.tick += 1
        self._draw_overlay()
        self._draw_title()
        card_bottom = self._draw_score_card(score, best_score)
        self._draw_hint_card(card_bottom)
        self._draw_footer()