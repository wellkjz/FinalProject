import pygame
from settings import WIDTH, PLAYER_SPEED, JUMP_FORCE, INVINCIBILITY_FRAMES, RED, BLACK


class Player:
    W = 25
    H = 25

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.W, self.H)
        self.vel_y = 0
        self.lives = 3
        self.invincibility_timer = 0

    # ---- input ----
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if self.rect.x < -30:
            self.rect.x = WIDTH
        if self.rect.x > WIDTH:
            self.rect.x = -30

    # ---- physics ----
    def apply_gravity(self, gravity):
        self.vel_y  += gravity
        self.rect.y += self.vel_y

    def jump(self):
        self.vel_y = JUMP_FORCE

    # ---- state ----
    def take_hit(self):
        self.lives -= 1
        self.invincibility_timer = INVINCIBILITY_FRAMES

    def tick(self, gravity):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
        self.handle_input()
        self.apply_gravity(gravity)

    @property
    def is_invincible(self):
        return self.invincibility_timer > 0

    @property
    def is_alive(self):
        return self.lives > 0

    # ---- draw ----
    def draw(self, screen):
        if not self.is_invincible or (self.invincibility_timer // 6) % 2 == 0:
            pygame.draw.rect(screen, RED,   self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)