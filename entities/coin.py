import pygame
from settings import GOLD, BLUE, BLACK


class Coin:
    SIZE = 18

    def __init__(self, x, y, kind="gold"):
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.kind = kind  # "gold" | "blue"

    def _points(self):
        cx, cy = self.rect.center
        return [
            (cx,      cy - 10), (cx + 3,  cy - 3),
            (cx + 10, cy - 3),  (cx + 5,  cy + 2),
            (cx + 7,  cy + 10), (cx,      cy + 5),
            (cx - 7,  cy + 10), (cx - 5,  cy + 2),
            (cx - 10, cy - 3),  (cx - 3,  cy - 3),
        ]

    def draw(self, screen):
        color  = GOLD if self.kind == "gold" else BLUE
        pts    = self._points()
        pygame.draw.polygon(screen, color, pts)
        pygame.draw.polygon(screen, BLACK, pts, 2)