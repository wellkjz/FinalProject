# ========================
# WINDOW
# ========================
WIDTH  = 400
HEIGHT = 600
FPS    = 60

# ========================
# PHYSICS
# ========================
GRAVITY      = 0.5
JUMP_FORCE   = -12
PLAYER_SPEED = 5
BOOST_VEL    = -25

# ========================
# PLATFORM
# ========================
PLATFORM_W = 80
PLATFORM_H = 12
GAP_Y      = 90
LEFT_X     = 50
RIGHT_X    = WIDTH - 130  # 270

# ========================
# COLORS
# ========================
GREEN      = (70,  200, 120)
DARK_GREEN = (40,  120,  70)
BLUE       = (80,  140, 255)
PURPLE     = (180,  70, 255)
GOLD       = (255, 215,   0)
RED        = (220,  70,  70)
DARK_RED   = (160,  30,  30)
SKY        = (135, 206, 235)
BLACK      = (0,     0,   0)
WHITE      = (240, 240, 240)
BROWN      = (120,  70,  30)
GRAY       = (180, 180, 180)
YELLOW     = (255, 220,  90)
BRICK_COLOR = (70, 37, 125)

# ========================
# ENEMY
# ========================
ENEMY_SCORE_THRESHOLD    = 2000
ENEMY_SPAWN_INTERVAL_MIN = 120   # frames
ENEMY_SPAWN_INTERVAL_MAX = 300   # frames
INVINCIBILITY_FRAMES     = 90    # ~1.5 sec

# ========================
# SCORE VALUES
# ========================
COIN_GOLD_VALUE   = 1000
COIN_BLUE_PENALTY = 200
COIN_VALUE = 5

# ========================
# SOUND PATHS
# ========================
SOUND_JUMP  = "sounds/jump.wav"
SOUND_COIN  = "sounds/coin.wav"
SOUND_BAD   = "sounds/bad.wav"
SOUND_BOOST = "sounds/boost.wav"

# ========================
# SAVE
# ========================
HIGHSCORE_FILE = "data/highscore.json"

# ========================
# SHOP — CHARACTERS
# Each entry:
#   id        : unique string key (used in save file)
#   name      : display name
#   image     : path to PNG in assets/  (used as preview AND in-game skin)
#   price     : coin cost  (0 = free / default)
#   scale     : draw scale applied to the PNG (same as Player.SCALE)
# ========================
SHOP_CHARACTERS = [
    {
        "id":    "default",
        "name":  "Default",
        "image": "assets/player.png",
        "price": 0,
        "scale": 0.20,
    },
    {
        "id": "pixel_eren",
        "name": "Eren Yeager",
        "price": 2000,
        "image": "assets/eren.PNG",
        "scale": 0.20,
    },
    {
        "id": "pixel_mikasa",
        "name": "Mikasa Ackerman",
        "price": 2700,
        "image": "assets/mikasa.PNG",
        "scale": 0.20,
    },
    {
        "id": "pixel_armin",
        "name": "Armin Arlert",
        "price": 2700,
        "image": "assets/armin.PNG",
        "scale": 0.20,
    },
    {
        "id":    "pusheen",
        "name":  "Harry Potter pusheen",
        "image": "assets/pusheen.png",
        "price": 3000,
        "scale": 0.20,
    },
{
        "id":    "ablay",
        "name":  "Abilaykhan",
        "image": "assets/ablay.png",
        "price": 2500,
        "scale": 0.20,
    }
]

SHOP_BACKGROUNDS = [
    {
        "id":    "default",
        "name":  "Sky",
        "image": "assets/background.png",
        "price": 0,
        "music": "sounds/default_sound.mp3"
    },
    {
        "id": "aot_bg",
        "name": "Attack on Titan",
        "price": 2500,
        "image": "assets/aot_bg_png.JPG",
        "music": "sounds/AOT_music.ogg",
    },
{
        "id": "hp_bg",
        "name": "Harry Potter",
        "price": 3000,
        "image": "assets/hastle.JPG",
        "music": "sounds/harry_potter_music.mp3",
    }
]