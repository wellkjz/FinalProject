import pygame
from settings import SKY, BLACK, RED, WIDTH


class GameOverScreen:
    def __init__(self, screen, font, font_small):
        self.screen     = screen
        self.font       = font
        self.font_small = font_small

    def draw(self, score, best_score, draw_hearts_fn):
        self.screen.fill(SKY)

        go = self.font.render("GAME OVER", True, RED)
        self.screen.blit(go, (WIDTH // 2 - go.get_width() // 2, 160))

        for text, y in [
            (f"Score: {score}",      210),
            (f"Best:  {best_score}", 240),
        ]:
            surf = self.font.render(text, True, BLACK)
            self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

        for text, y in [
            ("SPACE     - Restart",    300),
            ("ENTER     - Menu",       340),
        ]:
            surf = self.font.render(text, True, BLACK)
            self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))

        clr = self.font_small.render("BACKSPACE - Clear Best", True, BLACK)
        self.screen.blit(clr, (WIDTH // 2 - clr.get_width() // 2, 385))

        draw_hearts_fn(0)