import pygame
from settings import PLATFORM_W, PLATFORM_H, GREEN, DARK_GREEN


class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLATFORM_W, PLATFORM_H)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN,      self.rect)
        pygame.draw.rect(screen, DARK_GREEN, self.rect, 2)