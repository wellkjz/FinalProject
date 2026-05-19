import pygame
from settings import BLACK, RED, GRAY, DARK_RED, WIDTH, HEIGHT, ENEMY_SCORE_THRESHOLD


class HUD:
    def __init__(self, screen, font, font_small):
        self.screen     = screen
        self.font       = font
        self.font_small = font_small

    def draw(self, score, best_score, lives):
        self.screen.blit(self.font.render(f"Score: {score}",      True, BLACK), (10, 10))
        self.screen.blit(self.font.render(f"Best:  {best_score}", True, BLACK), (10, 40))
        self.draw_hearts(lives)

        if score < ENEMY_SCORE_THRESHOLD:
            remaining = ENEMY_SCORE_THRESHOLD - score
            hint = self.font_small.render(
                f"Birds at {ENEMY_SCORE_THRESHOLD}! ({remaining} away)", True, DARK_RED
            )
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))

    def draw_hearts(self, lives):
        size    = 20
        spacing = 26
        start_x = WIDTH - 10 - (3 * spacing)
        y       = 12

        for i in range(3):
            x     = start_x + i * spacing
            cx    = x + size // 2
            cy    = y + size // 2
            color = RED if i < lives else GRAY
            r     = size // 4
            pygame.draw.circle(self.screen, color, (cx - r, cy - 2), r)
            pygame.draw.circle(self.screen, color, (cx + r, cy - 2), r)
            pygame.draw.polygon(self.screen, color, [
                (cx - size // 2, cy),
                (cx + size // 2, cy),
                (cx, cy + size // 2),
            ])