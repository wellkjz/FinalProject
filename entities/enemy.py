import pygame
import random
from settings import WIDTH, BROWN, BLACK


class Enemy:
    W = 35
    H = 20

    def __init__(self, y):
        direction = random.choice(["left", "right"])
        if direction == "left":
            x     = WIDTH
            speed = random.randint(3, 6) * -1
        else:
            x     = -40
            speed = random.randint(3, 6)

        self.rect  = pygame.Rect(x, y, self.W, self.H)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

    def is_offscreen(self):
        return self.rect.x < -100 or self.rect.x > WIDTH + 100

    def draw(self, screen):
        body  = pygame.Rect(self.rect.x, self.rect.y, self.W, self.H)
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