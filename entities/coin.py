import pygame
from settings import GOLD, BLUE, BLACK

# Цвета пиксельной монетки
_COIN_DARK   = (139,  90,  10)
_COIN_MID    = (205, 140,  20)
_COIN_LIGHT  = (255, 215,   0)
_COIN_SHINE  = (255, 245, 150)


class Coin:
    SIZE = 23

    _SPIN_WIDTHS = [1.0, 0.85, 0.6, 0.3, 0.05, 0.3, 0.6, 0.85]
    _ANIM_SPEED  = 6   # тиков на фрейм

    def __init__(self, x, y, kind="gold"):
        self.rect   = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.kind   = kind          # "gold" | "blue" | "coin"
        self._frame = 0
        self._tick  = 0

    def update(self):
        if self.kind == "coin":
            self._tick += 1
            if self._tick >= self._ANIM_SPEED:
                self._tick   = 0
                self._frame  = (self._frame + 1) % len(self._SPIN_WIDTHS)

    def _star_points(self):
        cx, cy = self.rect.center
        return [
            (cx,      cy - 10), (cx + 3,  cy - 3),
            (cx + 10, cy - 3),  (cx + 5,  cy + 2),
            (cx + 7,  cy + 10), (cx,      cy + 5),
            (cx - 7,  cy + 10), (cx - 5,  cy + 2),
            (cx - 10, cy - 3),  (cx - 3,  cy - 3),
        ]

    def _draw_star(self, screen):
        color = GOLD if self.kind == "gold" else BLUE
        pts   = self._star_points()
        pygame.draw.polygon(screen, color, pts)
        pygame.draw.polygon(screen, BLACK, pts, 2)

    def _draw_coin(self, screen):
        cx, cy  = self.rect.center
        r       = self.SIZE // 2
        w_ratio = self._SPIN_WIDTHS[self._frame]
        w       = max(2, int(r * w_ratio))

        body = pygame.Rect(cx - w, cy - r, w * 2, r * 2)
        pygame.draw.ellipse(screen, _COIN_MID,  body)

        if w_ratio > 0.4:
            shine = pygame.Rect(cx - w + 2, cy - r + 2, max(2, w - 4), r - 2)
            pygame.draw.ellipse(screen, _COIN_SHINE, shine)

        pygame.draw.ellipse(screen, _COIN_DARK, body, 2)

        if w_ratio > 0.7:
            font = pygame.font.SysFont("consolas", 10, bold=True)
            lbl  = font.render("$", True, _COIN_DARK)
            screen.blit(lbl, (cx - lbl.get_width() // 2,
                               cy - lbl.get_height() // 2))

    def draw(self, screen):
        if self.kind == "coin":
            self._draw_coin(screen)
        else:
            self._draw_star(screen)