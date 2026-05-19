import pygame
from settings import PURPLE, BLACK


class Booster:
    SIZE = 18

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)

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
        pts = self._points()
        pygame.draw.polygon(screen, PURPLE, pts)
        pygame.draw.polygon(screen, BLACK,  pts, 2)