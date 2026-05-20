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
    # ── Add your own characters below ──────────────────────────────────────
    # {
    #     "id":    "ninja",
    #     "name":  "Ninja",
    #     "image": "assets/ninja.png",
    #     "price": 300,
    #     "scale": 0.20,
    # },
    # {
    #     "id":    "robot",
    #     "name":  "Robot",
    #     "image": "assets/robot.png",
    #     "price": 500,
    #     "scale": 0.18,
    # },
]

# ========================
# SHOP — BACKGROUNDS
# Each entry:
#   id        : unique string key
#   name      : display name
#   image     : path to PNG in assets/
#   price     : coin cost  (0 = free / default)
#   music     : path to music file in sounds/ (None = no music / silence)
#               Supported formats: .ogg  .mp3  .wav
# ========================
SHOP_BACKGROUNDS = [
    {
        "id":    "default",
        "name":  "Sky",
        "image": "assets/background.png",
        "price": 0,
        "music": None,          # put e.g. "sounds/music_sky.ogg" here
    },
    # ── Add your own backgrounds below ─────────────────────────────────────
    # {
    #     "id":    "space",
    #     "name":  "Space",
    #     "image": "assets/bg_space.png",
    #     "price": 200,
    #     "music": "sounds/music_space.ogg",
    # },
    # {
    #     "id":    "forest",
    #     "name":  "Forest",
    #     "image": "assets/bg_forest.png",
    #     "price": 400,
    #     "music": "sounds/music_forest.ogg",
    # },
]