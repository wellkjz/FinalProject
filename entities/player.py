import pygame
from settings import WIDTH, PLAYER_SPEED, JUMP_FORCE, INVINCIBILITY_FRAMES, RED, BLACK


class Player:
    W = 25
    H = 25
    SCALE = 0.20   # default scale — overridden by constructor arg

    def __init__(self, x, y, skin_path: str = "assets/player.png", scale: float = None):
        self.rect  = pygame.Rect(x, y, self.W, self.H)
        self.vel_y = 0
        self.lives = 3
        self.invincibility_timer = 0
        self.facing_right = True

        _scale = scale if scale is not None else self.SCALE
        raw_img = pygame.image.load(skin_path).convert_alpha()
        w = max(1, int(raw_img.get_width()  * _scale))
        h = max(1, int(raw_img.get_height() * _scale))
        self.skin = pygame.transform.scale(raw_img, (w, h))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True
        if self.rect.x < -30:
            self.rect.x = WIDTH
        if self.rect.x > WIDTH:
            self.rect.x = -30

    def apply_gravity(self, gravity):
        self.vel_y  += gravity
        self.rect.y += self.vel_y

    def jump(self):
        self.vel_y = JUMP_FORCE

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

    def draw(self, screen):
        if not self.is_invincible or (self.invincibility_timer // 6) % 2 == 0:
            img = (self.skin if self.facing_right
                   else pygame.transform.flip(self.skin, True, False))
            sprite_rect = img.get_rect(midbottom=self.rect.midbottom)
            screen.blit(img, sprite_rect)

    @property
    def sprite_rect(self):
        return self.skin.get_rect(midbottom=self.rect.midbottom)

    @property
    def collect_rect(self):
        return pygame.Rect(
            self.rect.x,
            self.rect.y - 15,
            self.rect.width,
            self.rect.height + 15,
        )