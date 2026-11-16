"""Estados de la partida."""

from enum import Enum, auto


class GameState(Enum):
    """Representa los estados posibles de la partida."""

    RUNNING = auto()
    PAUSED = auto()
    VICTORY = auto()
    GAME_OVER = auto()
