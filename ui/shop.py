import os
import pygame
from settings import (
    WIDTH, HEIGHT, GOLD, GRAY,
    SHOP_CHARACTERS, SHOP_BACKGROUNDS,
)

# ── palette ──────────────────────────────────────────────────────────────────
_BG_TOP    = (14,  8, 45)
_BG_BOT    = (40, 20, 80)
_CARD_CLR  = (25, 15, 55)
_CARD_SEL  = (50, 30, 100)
_TAB_ACT   = (80,  50, 160)
_TAB_INACT = (30,  20,  60)
_WHITE     = (240, 240, 255)
_DIM       = (130, 120, 160)
_GREEN     = (80,  220, 120)
_RED       = (255,  80,  80)
_GOLD      = GOLD


def _pill(surface, rect, color, alpha=210, r=8):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=r)
    surface.blit(s, rect.topleft)


def _load_font(size, bold=False):
    for name in ("Consolas", "Courier New", "Lucida Console", "monospace"):
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except Exception:
            pass
    return pygame.font.Font(None, size + 8)


def _load_preview(path: str, target_w: int, target_h: int) -> pygame.Surface:
    """Load an image and fit it inside target_w × target_h, keeping aspect."""
    try:
        raw = pygame.image.load(path).convert_alpha()
        rw, rh = raw.get_size()
        scale = min(target_w / rw, target_h / rh)
        nw, nh = max(1, int(rw * scale)), max(1, int(rh * scale))
        return pygame.transform.smoothscale(raw, (nw, nh))
    except Exception:
        # grey placeholder
        surf = pygame.Surface((target_w, target_h), pygame.SRCALPHA)
        surf.fill((80, 80, 100, 200))
        return surf


class ShopScreen:
    # layout constants
    COLS        = 2
    CARD_W      = 160
    CARD_H      = 170
    PREVIEW_W   = 80
    PREVIEW_H   = 80
    TAB_H       = 36
    HEADER_H    = 50
    SCROLL_SPD  = 20

    def __init__(self, screen, shop_sys):
        self.screen   = screen
        self.shop_sys = shop_sys

        self.font_title = _load_font(20, bold=True)
        self.font_tab   = _load_font(14, bold=True)
        self.font_name  = _load_font(13, bold=True)
        self.font_sub   = _load_font(11)
        self.font_badge = _load_font(10, bold=True)
        self.font_coin  = _load_font(13)

        self.tab      = 0          # 0 = characters, 1 = backgrounds
        self.scroll   = 0          # vertical scroll offset (pixels)
        self._scroll_target = 0

        # Pre-load previews so we don't hitch mid-frame
        self._char_previews = [
            _load_preview(c["image"], self.PREVIEW_W, self.PREVIEW_H)
            for c in SHOP_CHARACTERS
        ]
        self._bg_previews = [
            _load_preview(b["image"], self.PREVIEW_W, self.PREVIEW_H)
            for b in SHOP_BACKGROUNDS
        ]

        # message shown briefly after a purchase attempt
        self._msg       = ""
        self._msg_timer = 0

    # ------------------------------------------------------------------ #
    #  Input                                                               #
    # ------------------------------------------------------------------ #
    def handle_key(self, key) -> str:
        """Returns 'close' when the player leaves the shop."""
        if key in (pygame.K_ESCAPE, pygame.K_s):
            self.scroll = 0
            self._scroll_target = 0
            return "close"
        if key == pygame.K_LEFT or key == pygame.K_q:
            self.tab = 0
            self.scroll = self._scroll_target = 0
        if key == pygame.K_RIGHT or key == pygame.K_e:
            self.tab = 1
            self.scroll = self._scroll_target = 0
        if key == pygame.K_UP:
            self._scroll_target = max(0, self._scroll_target - self.SCROLL_SPD * 3)
        if key == pygame.K_DOWN:
            self._scroll_target += self.SCROLL_SPD * 3
        return ""

    def handle_click(self, pos, scoring):
        """Call this with mouse-click pos and the scoring object."""
        mx, my = pos
        items  = SHOP_CHARACTERS if self.tab == 0 else SHOP_BACKGROUNDS

        pad    = (WIDTH - self.COLS * self.CARD_W) // (self.COLS + 1)
        start_y = self.HEADER_H + self.TAB_H + 12 - self.scroll

        for idx, item in enumerate(items):
            col = idx % self.COLS
            row = idx // self.COLS
            cx  = pad + col * (self.CARD_W + pad)
            cy  = start_y + row * (self.CARD_H + 10)
            rect = pygame.Rect(cx, cy, self.CARD_W, self.CARD_H)
            if rect.collidepoint(mx, my):
                self._interact(item, scoring)
                break

    def _interact(self, item, scoring):
        iid = item["id"]
        if self.tab == 0:
            owned = self.shop_sys.is_char_unlocked(iid)
            if owned:
                self.shop_sys.equip_char(iid)
                self._flash(f"Equipped {item['name']}!")
            else:
                ok = self.shop_sys.buy_char(iid, scoring)
                if ok:
                    self.shop_sys.equip_char(iid)
                    self._flash(f"Bought & equipped {item['name']}!")
                else:
                    self._flash("Not enough coins!")
        else:
            owned = self.shop_sys.is_bg_unlocked(iid)
            if owned:
                self.shop_sys.equip_bg(iid)
                self._flash(f"Equipped {item['name']}!")
            else:
                ok = self.shop_sys.buy_bg(iid, scoring)
                if ok:
                    self.shop_sys.equip_bg(iid)
                    self._flash(f"Bought & equipped {item['name']}!")
                else:
                    self._flash("Not enough coins!")

    def _flash(self, msg: str):
        self._msg       = msg
        self._msg_timer = 120  # frames

    # ------------------------------------------------------------------ #
    #  Draw                                                                #
    # ------------------------------------------------------------------ #
    def draw(self, coins: int):
        self._smooth_scroll()
        self._draw_bg()
        self._draw_header(coins)
        self._draw_tabs()
        self._draw_items()
        self._draw_msg()
        self._draw_hints()

    # ── smooth scroll ──
    def _smooth_scroll(self):
        diff = self._scroll_target - self.scroll
        self.scroll += diff * 0.18
        if abs(diff) < 0.5:
            self.scroll = self._scroll_target

    # ── gradient background ──
    def _draw_bg(self):
        for y in range(HEIGHT):
            t = y / HEIGHT
            r = int(_BG_TOP[0] + (_BG_BOT[0] - _BG_TOP[0]) * t)
            g = int(_BG_TOP[1] + (_BG_BOT[1] - _BG_TOP[1]) * t)
            b = int(_BG_TOP[2] + (_BG_BOT[2] - _BG_TOP[2]) * t)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    # ── header ──
    def _draw_header(self, coins: int):
        title = self.font_title.render("SHOP", True, _GOLD)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

        # coin counter top-right
        coin_txt = self.font_coin.render(f"Coins: {coins}", True, _GOLD)
        _pill(self.screen,
              pygame.Rect(WIDTH - coin_txt.get_width() - 20, 8,
                          coin_txt.get_width() + 12, coin_txt.get_height() + 6),
              (60, 40, 0), alpha=200)
        self.screen.blit(coin_txt, (WIDTH - coin_txt.get_width() - 14, 11))

    # ── tabs ──
    def _draw_tabs(self):
        tw = WIDTH // 2
        labels = ["Characters", "Backgrounds"]
        for i, lbl in enumerate(labels):
            rect  = pygame.Rect(i * tw, self.HEADER_H, tw, self.TAB_H)
            color = _TAB_ACT if i == self.tab else _TAB_INACT
            _pill(self.screen, rect, color, alpha=230, r=0)
            txt = self.font_tab.render(lbl, True, _WHITE if i == self.tab else _DIM)
            self.screen.blit(txt,
                (rect.x + rect.w // 2 - txt.get_width() // 2,
                 rect.y + rect.h // 2 - txt.get_height() // 2))
        # bottom border
        pygame.draw.line(self.screen, _TAB_ACT,
                         (0, self.HEADER_H + self.TAB_H),
                         (WIDTH, self.HEADER_H + self.TAB_H), 2)

    # ── item grid ──
    def _draw_items(self):
        items    = SHOP_CHARACTERS if self.tab == 0 else SHOP_BACKGROUNDS
        previews = self._char_previews if self.tab == 0 else self._bg_previews

        pad     = (WIDTH - self.COLS * self.CARD_W) // (self.COLS + 1)
        start_y = self.HEADER_H + self.TAB_H + 12 - int(self.scroll)

        # clipping region so cards don't bleed over header/tabs
        clip = pygame.Rect(0, self.HEADER_H + self.TAB_H + 2, WIDTH,
                           HEIGHT - self.HEADER_H - self.TAB_H - 40)
        self.screen.set_clip(clip)

        for idx, item in enumerate(items):
            col = idx % self.COLS
            row = idx // self.COLS
            cx  = pad + col * (self.CARD_W + pad)
            cy  = start_y + row * (self.CARD_H + 10)
            self._draw_card(item, previews[idx], cx, cy)

        self.screen.set_clip(None)

        # Update scroll max so you can't over-scroll
        rows = (len(items) + self.COLS - 1) // self.COLS
        total_h = rows * (self.CARD_H + 10) + 20
        visible_h = HEIGHT - self.HEADER_H - self.TAB_H - 40
        self._scroll_target = max(
            0, min(self._scroll_target, total_h - visible_h)
        )

    def _draw_card(self, item, preview: pygame.Surface, cx: int, cy: int):
        iid      = item["id"]
        is_char  = self.tab == 0
        owned    = (self.shop_sys.is_char_unlocked(iid) if is_char
                    else self.shop_sys.is_bg_unlocked(iid))
        equipped = (self.shop_sys.equipped_char == iid if is_char
                    else self.shop_sys.equipped_bg == iid)

        border_color = _GREEN if equipped else (_TAB_ACT if owned else _CARD_CLR)
        card_color   = _CARD_SEL if equipped else _CARD_CLR

        # card body
        card_rect = pygame.Rect(cx, cy, self.CARD_W, self.CARD_H)
        _pill(self.screen, card_rect, card_color, alpha=220, r=10)
        # border
        pygame.draw.rect(self.screen, border_color, card_rect,
                         width=2, border_radius=10)

        # preview image — centred in top portion
        prev_x = cx + self.CARD_W // 2 - preview.get_width() // 2
        prev_y = cy + 8
        self.screen.blit(preview, (prev_x, prev_y))

        # item name
        name_surf = self.font_name.render(item["name"], True, _WHITE)
        self.screen.blit(name_surf,
            (cx + self.CARD_W // 2 - name_surf.get_width() // 2,
             cy + self.PREVIEW_H + 12))

        # music label (backgrounds only)
        if not is_char:
            music_path = item.get("music")
            if music_path:
                mname = os.path.splitext(os.path.basename(music_path))[0]
            else:
                mname = "no music"
            m_surf = self.font_sub.render(f"♪ {mname}", True, (170, 140, 255))
            self.screen.blit(m_surf,
                (cx + self.CARD_W // 2 - m_surf.get_width() // 2,
                 cy + self.PREVIEW_H + 28))

        # price / badge row
        badge_y = cy + self.CARD_H - 28
        if equipped:
            badge = self.font_badge.render("EQUIPPED", True, _GREEN)
            _pill(self.screen,
                  pygame.Rect(cx + self.CARD_W // 2 - badge.get_width() // 2 - 4,
                               badge_y - 2, badge.get_width() + 8, badge.get_height() + 4),
                  (0, 80, 30), alpha=200, r=4)
            self.screen.blit(badge,
                (cx + self.CARD_W // 2 - badge.get_width() // 2, badge_y))
        elif owned:
            badge = self.font_badge.render("OWNED", True, (130, 200, 255))
            _pill(self.screen,
                  pygame.Rect(cx + self.CARD_W // 2 - badge.get_width() // 2 - 4,
                               badge_y - 2, badge.get_width() + 8, badge.get_height() + 4),
                  (0, 30, 80), alpha=200, r=4)
            self.screen.blit(badge,
                (cx + self.CARD_W // 2 - badge.get_width() // 2, badge_y))
        else:
            price = item["price"]
            p_surf = self.font_coin.render(f"{price} coins", True, _GOLD)
            self.screen.blit(p_surf,
                (cx + self.CARD_W // 2 - p_surf.get_width() // 2, badge_y))

    # ── flash message ──
    def _draw_msg(self):
        if self._msg_timer > 0:
            self._msg_timer -= 1
            alpha = min(255, self._msg_timer * 5)
            surf  = self.font_name.render(self._msg, True, _WHITE)
            s     = pygame.Surface((surf.get_width() + 20, surf.get_height() + 8),
                                   pygame.SRCALPHA)
            s.fill((0, 0, 0, min(alpha, 180)))
            s.blit(surf, (10, 4))
            self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT - 72))

    # ── bottom hint bar ──
    def _draw_hints(self):
        hints = "Q/← Chars  E/→ Bgs  ↑↓ Scroll  Click=Buy/Equip  ESC=Close"
        h_surf = self.font_sub.render(hints, True, _DIM)
        _pill(self.screen,
              pygame.Rect(0, HEIGHT - 18, WIDTH, 18),
              (0, 0, 0), alpha=160, r=0)
        self.screen.blit(h_surf,
            (WIDTH // 2 - h_surf.get_width() // 2, HEIGHT - 16))