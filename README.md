# Jump Game 🎮
A 2D endless vertical platformer built with Python and Pygame, developed as a team project for the Introduction to Programming 2 course at Astana IT University.

Project Description
Jump Game is an arcade-style game where the player bounces upward on auto-scrolling platforms, collects coins and stars, avoids enemy birds, and tries to reach the highest score possible. The game features a coin-based shop system where players can unlock custom character skins and backgrounds with matching background music.

Features

Endless vertical platformer with procedurally generated platforms
3 lives system with invincibility frames after taking damage
Collectibles:

🟡 Gold star — +1,000 points
🔴 Red star — −200 points (penalty)
⬆️ Green arrow booster — instant upward boost
🪙 Coin — +5 coins (shop currency)


Enemy birds that fly across the screen (spawn after 2,000 score)
Shop system with 5 character skins and 5 backgrounds, each backed by PNG assets
Per-background music — equipping a background switches the music automatically
Persistent save system — best score, coin total, and shop purchases saved to JSON files
Polished UI — animated menu, game-over screen with new-best detection, in-game HUD with pill-shaped overlays


Technologies Used
TechnologyPurposePython 3.12Core languagePygame 2.6Game engine (rendering, input, audio)JSONSave data persistence (data/highscore.json, data/shop_data.json)unittestAutomated testing

# OOP Concepts Used

This project demonstrates several Object-Oriented Programming principles:

## Encapsulation
Game entities manage their own data and behavior inside classes.

Example:
- `Player`
- `Enemy`
- `Platform`

---

## Inheritance
Game objects can inherit shared behavior from common base structures.

---

## Polymorphism
Different objects implement common methods like:
update()
draw()

Project Structure
FinalProject_team/
├── main.py                  # Entry point
├── game.py                  # Main game loop and state machine
├── settings.py              # All constants (window, physics, colors, paths)
├── requirements.txt
├── assets/
│   ├── background.png       # Default background (id="default")
│   ├── background_sunset.png  # Optional extra backgrounds
│   ├── player.png           # Default player skin (id="default")
│   ├── player_fire.png      # Optional extra skins
│   ├── platform.png
│   └── bird_sheet.png       # Animated enemy sprite sheet
├── sounds/
│   ├── jump.wav
│   ├── coin.wav
│   ├── bad.wav
│   ├── boost.wav
│   └── music_default.ogg    # Per-background music files
├── data/
│   ├── highscore.json       # Auto-created on first run
│   └── shop_data.json       # Auto-created on first run
├── entities/
│   ├── player.py            # Player class (movement, lives, skins)
│   ├── enemy.py             # Bird enemy (animated sprite sheet)
│   └── platform.py          # Platform tile
├── systems/
│   ├── level_generator.py   # Procedural platform + collectible generation
│   ├── scoring.py           # Score and coin tracking
│   ├── save_system.py       # JSON persistence (score, coins, shop)
│   └── shop_system.py       # Purchase/equip logic with coin deduction
├── ui/
│   ├── hud.py               # In-game overlay (score, lives, coins)
│   ├── menu.py              # Animated main menu
│   ├── game_over.py         # Game over screen
│   └── shop.py              # Shop screen (skins + backgrounds)
└── tests/
    └── test_*.py            # Unit tests

Installation
Requirements: Python 3.10+ and pip.
bash
1) Clone the repository
git clone https://github.com/wellkjz/FinalProject.git
cd FinalProject
2) Create a virtual environment
python -m venv venv
Windows:
venv\Scripts\activate
macOS / Linux:
source venv/bin/activate
3) Install dependencies
pip install -r requirements.txt

requirements.txt contents:
pygame>=2.6.0

How to Run
bashpython main.py

Controls
KeyAction
← / → Move left / right
SPACE Start game / confirm in shop
S Open shop (from main menu)
TAB Switch tab in shop (Skins / Backgrounds)
← / → Navigate shop items
E Equip an owned item
ESC / BACKSPACE Close shop
ENTER Return to menu (from game over)
BACKSPACE Clear best score (from game over)

Adding Custom Skins and Backgrounds
Skin: drop a PNG into assets/ named player_YOURID.png, then add an entry to SKINS in ui/shop.py:
python{"id": "YOURID", "name": "My Skin", "price": 100, "preview_color": (200, 100, 50)},
Background: drop assets/background_YOURID.png and (optionally) sounds/music_YOURID.ogg, then add to BACKGROUNDS in ui/shop.py:
python{"id": "YOURID", "name": "My BG", "price": 80, "preview_sky": (100,150,200), "preview_ground": (60,100,60)},

Running Tests
bashpython -m unittest discover -s tests -v

Screenshots

Main Menu:
<img width="502" height="790" alt="image" src="https://github.com/user-attachments/assets/abd525c4-ce2d-474d-a62d-e5bf943c9741" />

In Game:
<img width="502" height="790" alt="image" src="https://github.com/user-attachments/assets/a5d4f27c-2901-46d8-af37-a69a062583f1" />


Shop:
<img width="502" height="790" alt="image" src="https://github.com/user-attachments/assets/3615fad1-e22a-4505-8d8f-2870913ee35a" />



Game Over:
<img width="502" height="790" alt="Game Over" src="https://github.com/user-attachments/assets/a2fc8ce7-9296-4c35-ac8a-93b1ba209517" />



Team Member Roles
1) Gaipova Farangiz
Game logic, physics, level generation (game.py, systems/)
2) Sarsenbekova Safiyat
Shop system, save system, entities, documentation (ui/shop.py, systems/shop_system.py, entities/, README.md)
3) Akzholtay Tomiris
UI design and screens, Testing, assets (ui/hud.py, ui/menu.py, ui/game_over.py, tests/)

License
This project was created for educational purposes as part of the SE coursework at Astana IT University.
