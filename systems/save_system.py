import os
import json
from settings import HIGHSCORE_FILE


class SaveSystem:
    def __init__(self):
        os.makedirs(os.path.dirname(HIGHSCORE_FILE), exist_ok=True)

    def load(self):
        """Вернуть (best_score, coins)."""
        if not os.path.exists(HIGHSCORE_FILE):
            return 0, 0
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
                return (
                    int(data.get("best_score", 0)),
                    int(data.get("coins",      0)),
                )
        except (json.JSONDecodeError, ValueError):
            return 0, 0

    def save(self, score, coins):
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"best_score": score, "coins": coins}, f, indent=2)

    def clear(self):
        self.save(0, 0)