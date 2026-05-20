import json
import os
from settings import HIGHSCORE_FILE

_SHOP_FILE = "data/shop.json"


def _ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


class SaveSystem:
    # ------------------------------------------------------------------ #
    #  Score / coins                                                       #
    # ------------------------------------------------------------------ #
    def load(self):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
            return data.get("best_score", 0), data.get("coins", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0, 0

    def save(self, best_score: int, coins: int):
        _ensure_dir(HIGHSCORE_FILE)
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"best_score": best_score, "coins": coins}, f)

    def save_coins(self, coins: int):
        """Update only the coin total without touching the best score."""
        best, _ = self.load()
        self.save(best, coins)

    def clear(self):
        _ensure_dir(HIGHSCORE_FILE)
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"best_score": 0, "coins": 0}, f)

    # ------------------------------------------------------------------ #
    #  Shop data                                                           #
    # ------------------------------------------------------------------ #
    def load_shop_data(self) -> dict:
        try:
            with open(_SHOP_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_shop_data(self, data: dict):
        _ensure_dir(_SHOP_FILE)
        with open(_SHOP_FILE, "w") as f:
            json.dump(data, f, indent=2)