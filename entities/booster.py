import pygame

_GREEN       = ( 50, 210,  80)
_GREEN_DARK  = ( 20, 130,  40)
_GREEN_LIGHT = (160, 255, 180)


class Booster:
    SIZE = 18

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)

    def draw(self, screen):
        cx, cy = self.rect.center
        s = self.SIZE

        # Arrow body (rectangle, lower ~40% of the icon)
        shaft_w  = s // 3
        shaft_h  = s // 2
        shaft    = pygame.Rect(cx - shaft_w // 2, cy, shaft_w, shaft_h)
        pygame.draw.rect(screen, _GREEN, shaft, border_radius=2)
        pygame.draw.rect(screen, _GREEN_DARK, shaft, 1, border_radius=2)

        head_pts = [
            (cx,          cy - s // 2 + 2),
            (cx - s // 2 + 2, cy + 2),
            (cx + s // 2 - 2, cy + 2),
        ]
        pygame.draw.polygon(screen, _GREEN,      head_pts)
        pygame.draw.polygon(screen, _GREEN_DARK, head_pts, 1)

        shine_y = cy - s // 4
        pygame.draw.line(screen, _GREEN_LIGHT,
                         (cx - s // 5, shine_y),
                         (cx,          shine_y - 3), 2)