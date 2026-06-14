# config.py
from typing import Tuple

# Configurações de Tela e Grade
WIDTH: int = 800
HEIGHT: int = 600
TILE_SIZE: int = 20
GRID_W: int = WIDTH // TILE_SIZE
GRID_H: int = HEIGHT // TILE_SIZE
FPS: int = 60

# Cores Principais (RGB)
BG_COLOR: Tuple[int, int, int] = (15, 20, 25)
SNAKE_COLOR: Tuple[int, int, int] = (46, 204, 113)
APPLE_COLOR: Tuple[int, int, int] = (231, 76, 60)
BOSS_COLOR: Tuple[int, int, int] = (142, 68, 173)
ENEMY_COLOR: Tuple[int, int, int] = (211, 84, 0)
POWERUP_COLOR: Tuple[int, int, int] = (52, 152, 219)
TEXT_COLOR: Tuple[int, int, int] = (236, 240, 241)
WEAK_POINT_COLOR: Tuple[int, int, int] = (241, 196, 15)

# Balanceamento
INITIAL_SPEED: int = 120  # ms por movimento
DASH_MULT: float = 2.5
DASH_DUR: int = 500       # ms
DASH_CD: int = 3000       # ms