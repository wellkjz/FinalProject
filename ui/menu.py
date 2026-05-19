import pygame
from settings import SKY, BLACK, DARK_RED, WIDTH


class MenuScreen:
    def __init__(self, screen, font, font_small):
        self.screen     = screen
        self.font       = font
        self.font_small = font_small

    def draw(self, draw_hearts_fn):
        self.screen.fill(SKY)

        title = self.font.render("JUMP GAME", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))

        start = self.font.render("SPACE - START", True, BLACK)
        self.screen.blit(start, (WIDTH // 2 - start.get_width() // 2, 280))

        info = self.font_small.render("Avoid birds! You have 3 lives.", True, DARK_RED)
        self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 340))

        draw_hearts_fn(3)