"""Define la flota enemiga dentro de Space Invaders."""

from random import choice

import pygame

import space_invaders.settings as cfg
from space_invaders.enemy import Enemy
from space_invaders.type_aliases import ColorRGB, HorizontalDirection, Position2D


class EnemyFleet:
    """
    Administra un conjunto de enemigos, determina cómo se distribuyen y coordina su movimiento.
    """

    def __init__(self) -> None:
        """Inicializa el conjunto de enemigos."""
        self._enemies: list[Enemy] = self._create_enemies()
        self._horizontal_direction: HorizontalDirection = 1

    @property
    def has_enemies(self) -> bool:
        """Indica si la formación contiene enemigos."""
        return bool(self._enemies)

    def update(self, *, dt: float) -> None:
        """Actualiza el movimiento coordinado de la formación."""
        if not self._enemies:
            return

        # Desplazamiento previsto y extremos de la formación.
        dx: float = self._horizontal_direction * cfg.FLEET_HORIZONTAL_SPEED * dt
        dy: float = 0.0

        leftmost: int = min(enemy.left for enemy in self._enemies)
        rightmost: int = max(enemy.right for enemy in self._enemies)

        # Ajusta el movimiento al alcanzar un límite horizontal.
        if self._horizontal_direction == 1 and rightmost + dx >= cfg.WINDOW_WIDTH:
            dx = cfg.WINDOW_WIDTH - rightmost
            dy = cfg.FLEET_DROP_DISTANCE
            self._horizontal_direction = -1

        elif self._horizontal_direction == -1 and leftmost + dx <= 0:
            dx = -leftmost
            dy = cfg.FLEET_DROP_DISTANCE
            self._horizontal_direction = 1

        # Aplica el movimiento a toda la formación.
        for enemy in self._enemies:
            enemy.move(dx=dx, dy=dy)

    def draw(self, *, surface: pygame.Surface) -> None:
        """Dibuja todos los enemigos de la formación."""
        for enemy in self._enemies:
            enemy.draw(surface=surface)

    def get_random_shot_origin(self) -> Position2D | None:
        """Devuelve un origen de disparo aleatorio o None si no hay enemigos."""
        if not self._enemies:
            return None

        selected_enemy: Enemy = choice(self._enemies)

        return selected_enemy.midbottom

    def remove_hit_enemy(self, *, projectile_rect: pygame.Rect) -> bool:
        """Elimina el primer enemigo alcanzado y confirma si hubo impacto."""
        for index, enemy in enumerate(self._enemies):
            if projectile_rect.colliderect(enemy.rect):
                self._enemies.pop(index)
                return True

        return False

    def reached_defense_line(self, *, defense_y: int) -> bool:
        """Indica si algún enemigo ha alcanzado la línea defensiva."""
        return any(enemy.bottom >= defense_y for enemy in self._enemies)

    def _create_enemies(self) -> list[Enemy]:
        """Crea y devuelve los enemigos distribuidos en filas y columnas."""
        enemies: list[Enemy] = []

        for row in range(cfg.FLEET_ROW_COUNT):
            enemy_color: ColorRGB = cfg.FLEET_ROW_COLORS[row]
            y: int = cfg.FLEET_INITIAL_Y + (cfg.ENEMY_HEIGHT + cfg.FLEET_VERTICAL_GAP) * row
            for column in range(cfg.FLEET_COLUMN_COUNT):
                x: int = cfg.FLEET_INITIAL_X + (cfg.ENEMY_WIDTH + cfg.FLEET_HORIZONTAL_GAP) * column
                enemy: Enemy = Enemy(spawn_position=(x, y), color=enemy_color)
                enemies.append(enemy)

        return enemies
