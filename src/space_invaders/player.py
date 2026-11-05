"""Define el jugador y su comportamiento dentro de Space Invaders."""

import pygame

import space_invaders.settings as cfg
from space_invaders.type_aliases import ColorRGB, HorizontalDirection


class Player:
    """Gestiona el movimiento horizontal y la representación del jugador."""

    def __init__(self) -> None:
        """Inicializa la geometría y el estado de movimiento del jugador."""
        self._rect: pygame.Rect = pygame.Rect((0, 0), cfg.PLAYER_SIZE)
        self._rect.midbottom = cfg.PLAYER_START_MIDBOTTOM
        self._x: float = float(self._rect.centerx)  # Posición lógica

        # === LÍMITES DE MOVIMIENTO ===
        half_width: float = self._rect.width / 2
        self._min_center_x: float = half_width
        self._max_center_x: float = cfg.WINDOW_WIDTH - half_width

    def update(self, *, direction: HorizontalDirection, dt: float) -> None:
        """Actualiza el movimiento horizontal."""
        self._x += direction * cfg.PLAYER_MOVE_SPEED * dt

        # Límites horizontales
        self._x = min(max(self._x, self._min_center_x), self._max_center_x)

        # Actualización de la posición geométrica desde la posición lógica
        self._rect.centerx = round(self._x)

    def draw(self, *, surface: pygame.Surface, color: ColorRGB) -> None:
        """Renderiza el jugador sobre la superficie indicada."""
        pygame.draw.rect(surface, color, self._rect)
