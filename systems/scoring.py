from settings import COIN_GOLD_VALUE, COIN_BLUE_PENALTY, COIN_VALUE


class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.coins = 0          # валюта для скинов

    def collect_coin(self, kind):
        if kind == "gold":
            self.score += COIN_GOLD_VALUE
        elif kind == "blue":
            self.score -= COIN_BLUE_PENALTY
            if self.score < 0:
                self.score = 0
        elif kind == "coin":
            self.coins += COIN_VALUE

    def add_scroll(self, diff):
        self.score += diff

    def reset(self):
        self.score = 0
