"""Define el proyectil y su comportamiento dentro de Space Invaders."""

import pygame

import space_invaders.settings as cfg
from space_invaders.type_aliases import ColorRGB, Position2D, Position2DFloat


class Projectile:
    """Gestiona la posición, el movimiento y la representación de un proyectil."""

    def __init__(
        self,
        *,
        spawn_position: Position2D,
        vertical_speed: float,
        color: ColorRGB,
    ) -> None:
        """Inicializa la geometría y el estado de un proyectil."""
        # Geometría del proyectil.
        self._rect: pygame.Rect = pygame.Rect((0, 0), cfg.PROJECTILE_SIZE)
        self._rect.topleft = spawn_position

        # Posición lógica del proyectil.
        self._logical_position: Position2DFloat = (
            float(self._rect.x),
            float(self._rect.y),
        )

        self._vertical_speed: float = vertical_speed
        self._color: ColorRGB = color

    @property
    def rect(self) -> pygame.Rect:
        """Devuelve el rectángulo del proyectil."""
        return self._rect.copy()

    @property
    def bottom(self) -> int:
        """Devuelve el borde inferior del proyectil."""
        return self._rect.bottom

    @property
    def top(self) -> int:
        """Devuelve el borde superior del proyectil."""
        return self._rect.top

    def update(self, *, dt: float) -> None:
        """Actualiza la posición vertical del proyectil."""
        x: float = self._logical_position[0]
        new_y: float = self._logical_position[1] + self._vertical_speed * dt
        self._logical_position = (x, new_y)

        # Actualiza la posición geométrica respecto a la posición lógica
        self._rect.topleft = (round(x), round(new_y))

    def draw(self, *, surface: pygame.Surface) -> None:
        """Dibuja el proyectil en la superficie indicada."""
        pygame.draw.rect(surface, self._color, self._rect)
