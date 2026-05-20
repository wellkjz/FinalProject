from settings import SHOP_CHARACTERS, SHOP_BACKGROUNDS


class ShopSystem:
    def __init__(self, save_sys):
        self.save_sys = save_sys
        self._load()

    # ------------------------------------------------------------------ #
    #  Persistence helpers                                                 #
    # ------------------------------------------------------------------ #
    def _load(self):
        data = self.save_sys.load_shop_data()
        # Sets of unlocked item-IDs
        self.unlocked_chars = set(data.get("unlocked_chars", ["default"]))
        self.unlocked_bgs   = set(data.get("unlocked_bgs",   ["default"]))
        # Currently equipped IDs
        self.equipped_char  = data.get("equipped_char", "default")
        self.equipped_bg    = data.get("equipped_bg",   "default")

    def _save(self):
        self.save_sys.save_shop_data({
            "unlocked_chars": list(self.unlocked_chars),
            "unlocked_bgs":   list(self.unlocked_bgs),
            "equipped_char":  self.equipped_char,
            "equipped_bg":    self.equipped_bg,
        })

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #
    def is_char_unlocked(self, char_id: str) -> bool:
        return char_id in self.unlocked_chars

    def is_bg_unlocked(self, bg_id: str) -> bool:
        return bg_id in self.unlocked_bgs

    def buy_char(self, char_id: str, scoring) -> bool:
        """
        Attempt to purchase a character.
        Deducts coins from *scoring* on success.
        Returns True if purchased (or already owned).
        """
        if char_id in self.unlocked_chars:
            return True  # already owned — just equip
        item = next((c for c in SHOP_CHARACTERS if c["id"] == char_id), None)
        if item is None:
            return False
        if scoring.coins < item["price"]:
            return False  # not enough coins
        scoring.coins -= item["price"]           # ← deduct coins
        self.save_sys.save_coins(scoring.coins)  # persist new coin total
        self.unlocked_chars.add(char_id)
        self._save()
        return True

    def buy_bg(self, bg_id: str, scoring) -> bool:
        """
        Attempt to purchase a background.
        Deducts coins from *scoring* on success.
        Returns True if purchased (or already owned).
        """
        if bg_id in self.unlocked_bgs:
            return True  # already owned — just equip
        item = next((b for b in SHOP_BACKGROUNDS if b["id"] == bg_id), None)
        if item is None:
            return False
        if scoring.coins < item["price"]:
            return False  # not enough coins
        scoring.coins -= item["price"]           # ← deduct coins
        self.save_sys.save_coins(scoring.coins)  # persist new coin total
        self.unlocked_bgs.add(bg_id)
        self._save()
        return True

    def equip_char(self, char_id: str):
        if char_id in self.unlocked_chars:
            self.equipped_char = char_id
            self._save()

    def equip_bg(self, bg_id: str):
        if bg_id in self.unlocked_bgs:
            self.equipped_bg = bg_id
            self._save()

    # ------------------------------------------------------------------ #
    #  Convenience getters — return the full item dict                     #
    # ------------------------------------------------------------------ #
    def get_equipped_char(self) -> dict:
        return next(
            (c for c in SHOP_CHARACTERS if c["id"] == self.equipped_char),
            SHOP_CHARACTERS[0],
        )

    def get_equipped_bg(self) -> dict:
        return next(
            (b for b in SHOP_BACKGROUNDS if b["id"] == self.equipped_bg),
            SHOP_BACKGROUNDS[0],
        )