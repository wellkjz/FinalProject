import pygame
from settings import PLATFORM_W, PLATFORM_H


class Platform:
    image = pygame.image.load("assets/platform.png")
    image = pygame.transform.scale(image, (PLATFORM_W, PLATFORM_H))

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLATFORM_W, PLATFORM_H)

    def draw(self, screen):
        screen.blit(self.image, self.rect)