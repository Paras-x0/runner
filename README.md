# runner
# Runner — Pygame Endless Runner

A small endless runner game built with Pygame. The player can jump (double-jump) to avoid obstacles (snails and flies) while the score increases. This repo contains the core game code (`runner.py`) and expects a `graphics/`, `music/`, and `font/` folder with assets.

---

## Features

* Smooth player animation (walk & jump)
* Double jump mechanic
* Randomly spawning obstacles (snail, fly)
* Score tracking
* Background music and jump sound effect
* Intro screen with restart on spacebar

---

## Requirements

* Python 3.8+ (works on 3.8, 3.9, 3.10+)
* [pygame](https://www.pygame.org/) (tested with pygame 2.x)

Install dependencies with pip:

```bash
pip install pygame
```

---

## File structure (expected)

```
├── runner.py
├── graphics/
│   ├── Sky.png
│   ├── ground.png
│   ├── player/
│   │   ├── player_walk_1.png
│   │   ├── player_walk_2.png
│   │   ├── player_jump.png
│   │   └── player_stand.png
│   ├── snail/
│   │   ├── snail1.png
│   │   └── snail2.png
│   └── fly/
│       ├── Fly1.png
│       └── Fly2.png
├── music/
│   ├── music.wav
│   └── jump.mp3
└── font/
    └── Pixeltype.ttf
```
> Make sure the directory structure and file names match exactly — the game loads assets using relative paths.
---

## How to run

From the repo root (where `runner.py` lives) run:

```bash
python runner.py
```

Controls:

* `SPACE` — jump / double-jump / start the game
* Close the window or press the window manager quit button to exit

---

## Game logic notes

* The game uses a `Player` sprite (handles animation, gravity, double jump, and jump sound).
* Obstacles are instances of `Obstacle` (two types): `snail` and `fly`.
* An event timer (`obstacle_timer`) spawns obstacles at ~1.5s intervals.
* Score increases when the player jumps (the example adds 100 per jump to `initial_score`) — you may want to change scoring to be time/distance-based.
* Collision detection uses `pygame.sprite.spritecollide`.
