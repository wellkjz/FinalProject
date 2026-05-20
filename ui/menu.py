import pygame
import math
import random
from settings import SKY, BLACK, DARK_RED, GOLD, GREEN, WIDTH, HEIGHT


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


class MenuScreen:
    def __init__(self, screen, font=None, font_small=None):
        self.screen = screen
        self.tick   = 0

        self.font_title = _load_font(38, bold=True)   # was 32
        self.font_sub   = _load_font(16)               # was 13
        self.font_hint  = _load_font(14)               # was 11
        self.font_small = _load_font(13)               # was 10

        random.seed(7)
        self._stars = [
            (random.randint(0, WIDTH), random.randint(0, HEIGHT // 2 + 60),
             random.randint(1, 2), random.random() * 6)
            for _ in range(50)
        ]

    def _draw_bg(self):
        top, bot = (18, 8, 55), (55, 110, 190)
        for y in range(HEIGHT):
            t = y / HEIGHT
            r = int(top[0] + (bot[0]-top[0])*t)
            g = int(top[1] + (bot[1]-top[1])*t)
            b = int(top[2] + (bot[2]-top[2])*t)
            pygame.draw.line(self.screen, (r,g,b), (0,y), (WIDTH,y))

    def _draw_stars(self):
        for sx, sy, sr, phase in self._stars:
            a = int(160 + 95 * math.sin(self.tick * 0.025 + phase))
            a = max(0, min(255, a))
            pygame.draw.circle(self.screen, (a, a, a), (sx, sy), sr)

    def _draw_platforms(self):
        bob = int(12 * math.sin(self.tick * 0.025))
        for px, py in [(55,290),(185,360),(285,255),(110,440),(300,415)]:
            r = pygame.Rect(px, py + bob, 72, 11)
            pygame.draw.rect(self.screen, GREEN,       r, border_radius=5)
            pygame.draw.rect(self.screen, (30,140,60), r, width=2, border_radius=5)

    def _draw_title(self):
        bob  = int(6 * math.sin(self.tick * 0.04))
        text = "JUMP GAME"
        shad = self.font_title.render(text, True, (0, 0, 0))
        cx   = WIDTH // 2 - shad.get_width() // 2
        self.screen.blit(shad, (cx + 3, 168 + bob))
        glow = self.font_title.render(text, True, (255, 200, 60))
        self.screen.blit(glow, (cx - 1, 165 + bob - 1))
        main = self.font_title.render(text, True, GOLD)
        self.screen.blit(main, (cx, 165 + bob))

    def _draw_info_card(self):
        lines = [
            ("← →",   "Move"),
            ("SPACE",  "Start"),
            ("S",      "Shop"),
        ]
        pad = 14
        lh  = 26
        cw  = 230
        cy  = HEIGHT - 160
        cx  = WIDTH // 2 - cw // 2
        _pill(self.screen, pygame.Rect(cx, cy, cw, pad*2 + lh*len(lines) + 4),
              color=(0,0,30), alpha=200, r=12)
        for i, (key, action) in enumerate(lines):
            y   = cy + pad + i * lh
            ks  = self.font_hint.render(key,    True, GOLD)
            as_ = self.font_hint.render(action, True, (200, 220, 255))
            self.screen.blit(ks,  (cx + pad, y))
            self.screen.blit(as_, (cx + cw - as_.get_width() - pad, y))

    def _draw_birds_warn(self):
        txt  = self.font_small.render("Avoid birds!  3 lives.", True, (255,150,80))
        pad  = 8
        pill = pygame.Rect(WIDTH//2 - txt.get_width()//2 - pad,
                           HEIGHT - 82,
                           txt.get_width() + pad*2,
                           txt.get_height() + 8)
        _pill(self.screen, pill, color=(60,20,0))
        self.screen.blit(txt, (pill.x+pad, pill.y+4))

    def _draw_press_space(self):
        a   = int(128 + 127 * math.sin(self.tick * 0.06))
        txt = self.font_hint.render("PRESS  SPACE  TO  PLAY", True, (a, 255, a))
        self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT - 44))

    def draw(self, draw_hearts_fn=None):
        self.tick += 1
        self._draw_bg()
        self._draw_stars()
        self._draw_platforms()
        self._draw_title()
        self._draw_info_card()
        self._draw_birds_warn()
        self._draw_press_space()