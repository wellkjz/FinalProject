import random
from settings import WIDTH, HEIGHT, GAP_Y, LEFT_X, RIGHT_X
from entities.platform import Platform
from entities.coin     import Coin
from entities.booster  import Booster


class LevelGenerator:
    def __init__(self):
        self.platforms = []
        self.coins     = []
        self.boosters  = []

    # ---- generation ----
    def generate_world(self):
        self.platforms.append(Platform(WIDTH // 2 - 40, HEIGHT - 60))
        y = HEIGHT - 60 - GAP_Y
        for _ in range(11):
            self._add_row(y)
            y -= GAP_Y

    def _add_row(self, y):
        if random.random() < 0.3:
            self._create_pair(y)
        else:
            self._create_single(y)

    def _create_pair(self, y):
        self.platforms.append(Platform(LEFT_X,  y))
        self.platforms.append(Platform(RIGHT_X, y))

        kinds = ["gold", "blue"]
        if random.random() < 0.3:
            kinds[random.randint(0, 1)] = "purple"

        for x, kind in zip([LEFT_X + 30, RIGHT_X + 30], kinds):
            if kind == "purple":
                self.boosters.append(Booster(x, y - 20))
            else:
                self.coins.append(Coin(x, y - 20, kind))

    def _create_single(self, y):
        x = random.randint(40, WIDTH - 120)
        self.platforms.append(Platform(x, y))

    # ---- camera ----
    def scroll(self, diff):
        for obj in self.platforms + self.coins + self.boosters:
            obj.rect.y += diff

    # ---- lifecycle ----
    def cleanup(self):
        self.platforms = [p for p in self.platforms if p.rect.y < HEIGHT]
        self.coins     = [c for c in self.coins     if c.rect.y < HEIGHT]
        self.boosters  = [b for b in self.boosters  if b.rect.y < HEIGHT]

    def extend(self):
        while len(self.platforms) < 18:
            highest = min(self.platforms, key=lambda p: p.rect.y)
            self._add_row(highest.rect.y - GAP_Y)

    # ---- draw ----
    def draw(self, screen):
        for obj in self.platforms + self.coins + self.boosters:
            obj.draw(screen)