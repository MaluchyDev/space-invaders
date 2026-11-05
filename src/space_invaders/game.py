"""Gestiona el bucle principal y coordina los sistemas de Space Invaders."""

import pygame

import space_invaders.settings as cfg
from space_invaders.enemy_fleet import EnemyFleet
from space_invaders.player import Player
from space_invaders.type_aliases import HorizontalDirection


class Game:
    """Coordina el ciclo de vida y el bucle principal del juego."""

    def __init__(self) -> None:
        """Inicializa los recursos y el estado inicial del juego."""
        # === RECURSOS BASE DE PYGAME ===
        self._screen: pygame.Surface = pygame.display.set_mode(cfg.WINDOW_SIZE)
        pygame.display.set_caption(cfg.WINDOW_TITLE)
        self._clock: pygame.time.Clock = pygame.time.Clock()

        # === CONTROL DE EJECUCIÓN ===
        self._is_running: bool = True

        # === JUGADOR ===
        self._player: Player = Player()

        # === FLOTA ENEMIGA ===
        self._enemy_fleet: EnemyFleet = EnemyFleet()

    def run(self) -> None:
        """Ejecuta el bucle principal hasta finalizar la aplicación."""
        while self._is_running:
            # === EVENTOS ===
            self._handle_events()
            if not self._is_running:
                break

            # === TIEMPO ===
            dt: float = self._clock.tick(cfg.FPS) / 1000.0

            # === UPDATE ===
            self._update_world(dt=dt)

            # === RENDER ===
            self._screen.fill(cfg.BACKGROUND_COLOR)

            self._render_world()

            # === PRESENTACIÓN ===
            pygame.display.flip()

    def _handle_events(self) -> None:
        """Procesa los eventos relevantes para el control de la aplicación."""
        for event in pygame.event.get():
            # === CONTROL DE EJECUCIÓN ===
            if event.type == pygame.QUIT:
                self._is_running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._is_running = False

    def _get_movement_direction(self) -> HorizontalDirection:
        """Obtiene la dirección horizontal a partir del input continuo."""
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        move_left: bool = keys[pygame.K_LEFT] or keys[pygame.K_a]
        move_right: bool = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if move_right == move_left:
            return 0

        if move_right:
            return 1

        return -1

    def _update_world(self, *, dt: float) -> None:
        """Actualiza el mundo."""
        direction: HorizontalDirection = self._get_movement_direction()
        self._player.update(direction=direction, dt=dt)
        self._enemy_fleet.update(dt=dt)

    def _render_world(self) -> None:
        """Renderiza el mundo."""
        self._player.draw(surface=self._screen, color=cfg.PLAYER_COLOR)
        self._enemy_fleet.draw(surface=self._screen)
