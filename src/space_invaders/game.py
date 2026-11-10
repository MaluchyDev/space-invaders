"""Gestiona el bucle principal y coordina los sistemas de Space Invaders."""

import pygame

import space_invaders.settings as cfg
from space_invaders.enemy_fleet import EnemyFleet
from space_invaders.player import Player
from space_invaders.projectile import Projectile
from space_invaders.type_aliases import HorizontalDirection, Position2D


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

        # === PROYECTIL ===
        self._projectile: Projectile | None = None
        self._shot_cooldown_remaining: float = 0.0

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
        self._update_projectile(dt=dt)

    def _render_world(self) -> None:
        """Renderiza el mundo."""
        self._player.draw(surface=self._screen, color=cfg.PLAYER_COLOR)
        self._enemy_fleet.draw(surface=self._screen)

        if self._projectile is not None:
            self._projectile.draw(surface=self._screen)

    def _try_shoot(self) -> None:
        """Intenta crear un proyectil si el disparo está autorizado."""
        if not self._can_shoot():
            return

        # Calcular la posición inicial del proyectil.
        spawn_position_x: int = self._player.midtop[0] - cfg.PROJECTILE_WIDTH // 2
        spawn_position_y: int = self._player.midtop[1] - cfg.PROJECTILE_HEIGHT
        spawn_position: Position2D = (spawn_position_x, spawn_position_y)

        self._projectile = Projectile(
            spawn_position=spawn_position,
            vertical_speed=cfg.PLAYER_PROJECTILE_VERTICAL_SPEED,
            color=cfg.PLAYER_PROJECTILE_COLOR,
        )

        self._shot_cooldown_remaining = cfg.PLAYER_SHOT_COOLDOWN

    def _can_shoot(self) -> bool:
        """Indica si el jugador solicita un disparo y puede realizarlo."""
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        return keys[pygame.K_SPACE] and (
            self._projectile is None and self._shot_cooldown_remaining == 0.0
        )

    def _update_projectile(self, *, dt: float) -> None:
        """Gestiona el disparo y el ciclo de vida del proyectil del jugador."""
        # Actualiza el cooldown y procesa la solicitud de disparo.
        self._shot_cooldown_remaining = max(0.0, self._shot_cooldown_remaining - dt)
        self._try_shoot()

        if self._projectile is None:
            return

        # Actualiza y elimina el proyectil cuando abandona la pantalla.
        self._projectile.update(dt=dt)
        if self._projectile.bottom <= 0:
            self._projectile = None
