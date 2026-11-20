"""Gestiona el bucle principal y coordina los sistemas de Space Invaders."""

import pygame

import space_invaders.settings as cfg
from space_invaders.enemy_fleet import EnemyFleet
from space_invaders.game_state import GameState
from space_invaders.hud import HUD
from space_invaders.player import Player
from space_invaders.projectile import Projectile
from space_invaders.sound_effects import SoundEffects
from space_invaders.type_aliases import HorizontalDirection, Position2D


class Game:
    """Coordina el ciclo de vida y el bucle principal del juego."""

    def __init__(self) -> None:
        """Inicializa los recursos de la aplicación y prepara la primera partida."""
        # === RECURSOS DE LA APLICACIÓN ===
        # Recursos base de Pygame.
        self._screen: pygame.Surface = pygame.display.set_mode(cfg.WINDOW_SIZE)
        pygame.display.set_caption(cfg.WINDOW_TITLE)
        self._clock: pygame.time.Clock = pygame.time.Clock()

        # Recursos de audio.
        self._sound_effects: SoundEffects = SoundEffects()

        # Control de ejecución.
        self._is_running: bool = True

        # === ATRIBUTOS DE LA PARTIDA ===
        # Jugador.
        self._player: Player
        self._invulnerability_remaining: float

        # Formación enemiga.
        self._enemy_fleet: EnemyFleet

        # Proyectiles.
        # Disparo del jugador.
        self._player_projectile: Projectile | None
        self._player_shot_cooldown_remaining: float

        # Disparo de los enemigos.
        self._enemy_projectiles: list[Projectile]
        self._enemy_shot_cooldown_remaining: float

        # Estado de la partida.
        self._game_state: GameState
        self._score: int
        self._player_lives: int

        self._start_new_game()

        # === PRESENTACIÓN DEL HUD ===
        self._hud: HUD = HUD(
            config=cfg.HUD_CONFIG,
            initial_score=self._score,
            initial_lives=self._player_lives,
        )

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
            if self._game_state == GameState.RUNNING:
                defense_line_reached: bool = self._update_world(dt=dt)
                self._check_end_conditions(defense_line_reached=defense_line_reached)

            # Actualiza la presentación del HUD, incluso al finalizar la partida.
            self._hud.update(
                game_state=self._game_state,
                score=self._score,
                lives=self._player_lives,
            )

            # === RENDER ===
            self._screen.fill(cfg.BACKGROUND_COLOR)
            self._render_world()
            self._hud.draw(surface=self._screen)

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

            # === ESTADO DEL JUEGO ===
            if event.type == pygame.KEYDOWN:
                # Pausa.
                if event.key == pygame.K_p:
                    self._toggle_pause()

                # Reinicio.
                elif event.key == pygame.K_r and self._game_state in (
                    GameState.VICTORY,
                    GameState.GAME_OVER,
                ):
                    self._start_new_game()

    def _toggle_pause(self) -> None:
        """Alterna la partida entre los estados de ejecución y pausa."""
        if self._game_state is GameState.RUNNING:
            self._game_state = GameState.PAUSED

        elif self._game_state is GameState.PAUSED:
            self._game_state = GameState.RUNNING

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

    def _update_world(self, *, dt: float) -> bool:
        """Actualiza el mundo e indica si se alcanzó la línea defensiva."""
        direction: HorizontalDirection = self._get_movement_direction()

        # Actualiza el temporizador de invulnerabilidad del jugador.
        self._invulnerability_remaining = max(0.0, self._invulnerability_remaining - dt)

        # Actualiza las entidades.
        self._player.update(direction=direction, dt=dt)
        self._enemy_fleet.update(dt=dt)

        # Comprueba si la formación enemiga alcanzó la línea defensiva.
        defense_line_reached: bool = self._enemy_fleet.reached_defense_line(
            defense_y=self._player.top
        )

        # Actualiza los proyectiles.
        self._update_player_projectile(dt=dt)
        self._update_enemy_projectiles(dt=dt)

        # Resuelve las colisiones.
        self._resolve_player_projectile_collision()
        self._resolve_enemy_projectile_collisions()

        return defense_line_reached

    def _render_world(self) -> None:
        """Renderiza el mundo."""
        # Dibuja al jugador cuando corresponde y la flota enemiga.
        if self._should_draw_player():
            self._player.draw(surface=self._screen, color=cfg.PLAYER_COLOR)

        self._enemy_fleet.draw(surface=self._screen)

        # Dibuja los proyectiles del jugador y de la flota enemiga.
        if self._player_projectile is not None:
            self._player_projectile.draw(surface=self._screen)

        for enemy_projectile in self._enemy_projectiles:
            enemy_projectile.draw(surface=self._screen)

    def _try_player_shoot(self) -> None:
        """Intenta crear un proyectil si el disparo está autorizado."""
        if not self._player_can_shoot():
            return

        # Calcular la posición inicial del proyectil.
        spawn_position_x: int = self._player.midtop[0] - cfg.PROJECTILE_WIDTH // 2
        spawn_position_y: int = self._player.midtop[1] - cfg.PROJECTILE_HEIGHT
        spawn_position: Position2D = (spawn_position_x, spawn_position_y)

        self._player_projectile = Projectile(
            spawn_position=spawn_position,
            vertical_speed=cfg.PLAYER_PROJECTILE_VERTICAL_SPEED,
            color=cfg.PLAYER_PROJECTILE_COLOR,
        )

        self._sound_effects.play_player_shot()

        # Reinicia el cooldown.
        self._player_shot_cooldown_remaining = cfg.PLAYER_SHOT_COOLDOWN

    def _player_can_shoot(self) -> bool:
        """Indica si el jugador solicita un disparo y puede realizarlo."""
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        return (
            keys[pygame.K_SPACE]
            and self._player_projectile is None
            and self._player_shot_cooldown_remaining == 0.0
        )

    def _try_enemy_shoot(self) -> None:
        """Intenta crear un proyectil enemigo si se cumplen las condiciones."""
        if not self._enemy_can_shoot():
            return

        enemy_shot_origin: Position2D | None = self._enemy_fleet.get_random_shot_origin()

        if enemy_shot_origin is None:
            return

        # Calcular la posición inicial del proyectil
        projectile_spawn_position_x: int = enemy_shot_origin[0] - cfg.PROJECTILE_WIDTH // 2
        projectile_spawn_position_y: int = enemy_shot_origin[1]
        projectile_spawn_position: Position2D = (
            projectile_spawn_position_x,
            projectile_spawn_position_y,
        )

        projectile: Projectile = Projectile(
            spawn_position=projectile_spawn_position,
            vertical_speed=cfg.ENEMY_PROJECTILE_VERTICAL_SPEED,
            color=cfg.ENEMY_PROJECTILE_COLOR,
        )

        # Registra el proyectil y reinicia el cooldown.
        self._enemy_projectiles.append(projectile)
        self._enemy_shot_cooldown_remaining = cfg.ENEMY_SHOT_COOLDOWN

        # Reproduce el sonido del disparo confirmado.
        self._sound_effects.play_enemy_shot()

    def _enemy_can_shoot(self) -> bool:
        """Indica si puede generarse un nuevo proyectil enemigo."""
        return (
            self._enemy_fleet.has_enemies
            and len(self._enemy_projectiles) < cfg.MAX_ENEMY_PROJECTILES
            and self._enemy_shot_cooldown_remaining == 0.0
        )

    def _update_player_projectile(self, *, dt: float) -> None:
        """Gestiona el disparo y el ciclo de vida del proyectil del jugador."""
        # Actualiza el cooldown y procesa la solicitud de disparo.
        self._player_shot_cooldown_remaining = max(0.0, self._player_shot_cooldown_remaining - dt)
        self._try_player_shoot()

        if self._player_projectile is None:
            return

        # Actualiza y elimina el proyectil cuando abandona la pantalla.
        self._player_projectile.update(dt=dt)
        if self._player_projectile.bottom <= 0:
            self._player_projectile = None

    def _update_enemy_projectiles(self, *, dt: float) -> None:
        """Gestiona los disparos enemigos y el ciclo de vida de sus proyectiles."""
        # Actualiza el cooldown y procesa la solicitud de disparo.
        self._enemy_shot_cooldown_remaining = max(0.0, self._enemy_shot_cooldown_remaining - dt)
        self._try_enemy_shoot()

        # Actualiza los proyectiles y conserva los que siguen en pantalla.
        new_enemy_projectiles: list[Projectile] = []

        for enemy_projectile in self._enemy_projectiles:
            enemy_projectile.update(dt=dt)
            if enemy_projectile.top < cfg.WINDOW_HEIGHT:
                new_enemy_projectiles.append(enemy_projectile)

        self._enemy_projectiles = new_enemy_projectiles

    def _resolve_player_projectile_collision(self) -> None:
        """Resuelve el impacto del proyectil del jugador contra la formación enemiga."""
        if self._player_projectile is None:
            return

        if self._enemy_fleet.remove_hit_enemy(projectile_rect=self._player_projectile.rect):
            self._player_projectile = None
            self._score += cfg.ENEMY_SCORE

            self._sound_effects.play_enemy_destroyed()

    def _resolve_enemy_projectile_collisions(self) -> None:
        """Resuelve los impactos de los proyectiles enemigos contra el jugador."""
        remaining_enemy_projectiles: list[Projectile] = []
        player_rect: pygame.Rect = self._player.rect

        for enemy_projectile in self._enemy_projectiles:
            if enemy_projectile.rect.colliderect(player_rect):
                # Aplica daño únicamente si el jugador es vulnerable y tiene vidas.
                if self._player_lives > 0 and self._invulnerability_remaining == 0.0:
                    self._player_lives = max(0, self._player_lives - 1)
                    self._invulnerability_remaining = cfg.PLAYER_INVULNERABILITY_DURATION

                    self._sound_effects.play_player_hit()

            else:
                # Conserva los proyectiles que no han impactado.
                remaining_enemy_projectiles.append(enemy_projectile)

        self._enemy_projectiles = remaining_enemy_projectiles

    def _should_draw_player(self) -> bool:
        """Indica si debe dibujarse el jugador según el estado y su invulnerabilidad."""
        if self._game_state in (GameState.VICTORY, GameState.GAME_OVER):
            return True

        if self._invulnerability_remaining == 0.0:
            return True

        invulnerability_elapsed: float = (
            cfg.PLAYER_INVULNERABILITY_DURATION - self._invulnerability_remaining
        )
        blink_phase: int = int(invulnerability_elapsed / cfg.PLAYER_BLINK_INTERVAL)

        return blink_phase % 2 == 0

    def _check_end_conditions(self, *, defense_line_reached: bool) -> None:
        """Comprueba las condiciones de victoria y derrota."""
        if self._player_lives == 0 or defense_line_reached:
            self._game_state = GameState.GAME_OVER
            return

        if not self._enemy_fleet.has_enemies:
            self._game_state = GameState.VICTORY
            return

    def _start_new_game(self) -> None:
        """Inicializa las entidades y el estado de una nueva partida."""
        # === JUGADOR ===
        self._player = Player()
        self._invulnerability_remaining = 0.0

        # === FORMACIÓN ENEMIGA ===
        self._enemy_fleet = EnemyFleet()

        # === PROYECTILES ===
        # Disparo del jugador.
        self._player_projectile = None
        self._player_shot_cooldown_remaining = 0.0

        # Disparo de los enemigos.
        self._enemy_projectiles = []
        self._enemy_shot_cooldown_remaining = 0.0

        # === ESTADOS DE LA PARTIDA ===
        self._game_state = GameState.RUNNING
        self._score = 0
        self._player_lives = cfg.PLAYER_INITIAL_LIVES
