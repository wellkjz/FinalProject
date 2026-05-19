import pygame
import random
from settings import WIDTH

class Enemy:
    FRAME_COUNT = 6
    def __init__(self, y):
        direction = random.choice(["left", "right"])
        if direction == "left":
            x = WIDTH
            speed = random.randint(3, 6) * -1
        else:
            x = -40
            speed = random.randint(3, 6)
        self.speed = speed
        self.direction = direction
        self.sheet = pygame.image.load("assets/bird_sheet.png").convert_alpha()

        SCALE = 0.05
        new_w = int(self.sheet.get_width() * SCALE)
        new_h = int(self.sheet.get_height() * SCALE)
        self.sheet = pygame.transform.scale(self.sheet, (new_w, new_h))
        self.FRAME_WIDTH = new_w // self.FRAME_COUNT
        self.FRAME_HEIGHT = new_h
        self.frames = []
        for i in range(self.FRAME_COUNT):
            frame = self.sheet.subsurface(
                pygame.Rect(i * self.FRAME_WIDTH, 0,
                            self.FRAME_WIDTH, self.FRAME_HEIGHT)
            )
            if self.direction == "left":
                frame = pygame.transform.flip(frame, True, False)
            self.frames.append(frame)

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.rect = self.frames[0].get_rect(topleft=(x, y))

    def update(self):
        self.rect.x += self.speed
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % self.FRAME_COUNT

    def is_offscreen(self):
        return self.rect.x < -100 or self.rect.x > WIDTH + 100

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], self.rect)