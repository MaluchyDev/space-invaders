"""Define la configuración estable de Space Invaders."""

from typing import Final

from space_invaders.type_aliases import ColorRGB, Position2D, Size

# === SCREEN ===
WINDOW_WIDTH: Final[int] = 960
WINDOW_HEIGHT: Final[int] = 720
WINDOW_SIZE: Final[Size] = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_TITLE: Final[str] = "Space Invaders"

FPS: Final[int] = 60
BACKGROUND_COLOR: Final[ColorRGB] = (18, 22, 30)

# === JUGADOR ===
PLAYER_WIDTH: Final[int] = 64
PLAYER_HEIGHT: Final[int] = 28
PLAYER_SIZE: Final[Size] = (PLAYER_WIDTH, PLAYER_HEIGHT)

PLAYER_BOTTOM_MARGIN: Final[int] = 48
PLAYER_START_MIDBOTTOM: Final[Position2D] = (
    WINDOW_WIDTH // 2,
    WINDOW_HEIGHT - PLAYER_BOTTOM_MARGIN,
)

PLAYER_COLOR: Final[ColorRGB] = (80, 200, 220)
PLAYER_MOVE_SPEED: Final[float] = 320.0

# === ENEMIGO ===
ENEMY_WIDTH: Final[int] = 40
ENEMY_HEIGHT: Final[int] = 28
ENEMY_SIZE: Final[Size] = (ENEMY_WIDTH, ENEMY_HEIGHT)

# === FLOTA ENEMIGA ===
FLEET_HORIZONTAL_GAP: Final[int] = 16
FLEET_VERTICAL_GAP: Final[int] = 18
FLEET_TOP_MARGIN: Final[int] = 90
FLEET_DROP_DISTANCE: Final[int] = 20

FLEET_HORIZONTAL_SPEED: Final[float] = 90.0

FLEET_ROW_COUNT: Final[int] = 3
FLEET_COLUMN_COUNT: Final[int] = 8
FLEET_WIDTH: Final[int] = (
    FLEET_COLUMN_COUNT * ENEMY_WIDTH + (FLEET_COLUMN_COUNT - 1) * FLEET_HORIZONTAL_GAP
)

FLEET_INITIAL_X: Final[int] = (WINDOW_WIDTH - FLEET_WIDTH) // 2
FLEET_INITIAL_Y: Final[int] = FLEET_TOP_MARGIN

# Colores de las filas enemigas
FLEET_ROW_COLORS: Final[tuple[ColorRGB, ...]] = (
    (225, 105, 120),  # Fila 0: coral
    (230, 185, 85),  # Fila 1: dorado
    (160, 135, 220),  # Fila 2: violeta
)
