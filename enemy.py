import pygame
import random

from settings import WIDTH, BROWN, BLACK


class Enemy:
    def __init__(self, y):
        self.width = 35
        self.height = 20
        self.direction = random.choice(["left", "right"])

        if self.direction == "left":
            self.x = WIDTH
            self.speed = random.randint(3, 6) * -1
        else:
            self.x = -40
            self.speed = random.randint(3, 6)

        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        body = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)

        wing1 = [
            (self.rect.x + 5,  self.rect.y + 10),
            (self.rect.x - 5,  self.rect.y),
            (self.rect.x + 10, self.rect.y + 5),
        ]
        wing2 = [
            (self.rect.x + 25, self.rect.y + 10),
            (self.rect.x + 40, self.rect.y),
            (self.rect.x + 20, self.rect.y + 5),
        ]

        pygame.draw.ellipse(screen, BROWN, body)
        pygame.draw.polygon(screen, BLACK, wing1)
        pygame.draw.polygon(screen, BLACK, wing2)