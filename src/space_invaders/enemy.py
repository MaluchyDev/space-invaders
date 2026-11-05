"""Define el enemigo y su comportamiento dentro de Space Invaders."""

import pygame

import space_invaders.settings as cfg
from space_invaders.type_aliases import ColorRGB, Position2D, Position2DFloat


class Enemy:
    """Gestiona la posición, el movimiento y la representación de un enemigo."""

    def __init__(
        self,
        *,
        spawn_position: Position2D,
        color: ColorRGB,
    ) -> None:
        """Inicializa la geometría y el estado del enemigo."""
        self._rect: pygame.Rect = pygame.Rect((0, 0), cfg.ENEMY_SIZE)
        self._rect.topleft = spawn_position  # Posición geométrica
        self._logical_position: Position2DFloat = (
            float(self._rect.x),
            float(self._rect.y),
        )  # Posición lógica

        self._color: ColorRGB = color

    @property
    def left(self) -> int:
        """Devuelve el borde izquierdo del enemigo."""
        return self._rect.left

    @property
    def right(self) -> int:
        """Devuelve el borde derecho del enemigo."""
        return self._rect.right

    def move(self, *, dx: float, dy: float) -> None:
        """Desplaza el enemigo y actualiza su geometría."""
        new_x: float = self._logical_position[0] + dx
        new_y: float = self._logical_position[1] + dy
        self._logical_position = (new_x, new_y)

        # Actualiza la posición geométrica respecto a la posición lógica
        self._rect.topleft = (round(new_x), round(new_y))

    def draw(self, *, surface: pygame.Surface) -> None:
        """Dibuja el enemigo en la superficie indicada."""
        pygame.draw.rect(surface, self._color, self._rect)
