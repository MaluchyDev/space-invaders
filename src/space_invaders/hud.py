"""Define la configuración y la representación visual del HUD."""

from dataclasses import dataclass

import pygame

from space_invaders.game_state import GameState
from space_invaders.type_aliases import ColorRGB, Size


@dataclass(frozen=True, slots=True, kw_only=True)
class HUDConfig:
    """Define la configuración estable del HUD."""

    info_font_size: int
    status_font_size: int
    info_text_color: ColorRGB
    status_text_color: ColorRGB
    margin: int
    layout_size: Size
    paused_message: str
    victory_message: str
    game_over_message: str


class HUD:
    """Gestiona la representación visual de la información de la partida."""

    def __init__(
        self,
        *,
        config: HUDConfig,
        initial_score: int,
        initial_lives: int,
    ) -> None:
        """Inicializa la configuración, los recursos y el estado de presentación del HUD."""
        # === CONFIGURACIÓN ESTABLE ===
        self._config: HUDConfig = config

        # === RECURSOS DERIVADOS ===
        self._info_font: pygame.font.Font = pygame.font.Font(
            None,
            self._config.info_font_size,
        )
        self._status_font: pygame.font.Font = pygame.font.Font(
            None,
            self._config.status_font_size,
        )

        # === ESTADO DE PRESENTACIÓN DE SCORE ===
        self._last_score: int = initial_score
        self._score_text: pygame.Surface = self._info_font.render(
            f"Score: {self._last_score}",
            True,
            self._config.info_text_color,
        )

        # === ESTADO DE PRESENTACIÓN DE LIVES ===
        self._last_lives: int = initial_lives
        self._lives_text: pygame.Surface = self._info_font.render(
            f"Lives: {self._last_lives}",
            True,
            self._config.info_text_color,
        )
        self._lives_rect: pygame.Rect = self._lives_text.get_rect(
            topright=(
                self._config.layout_size[0] - self._config.margin,
                self._config.margin,
            )
        )

        # === ESTADO DE PRESENTACIÓN DEL MENSAJE DE ESTADO ===
        self._status_text: pygame.Surface | None = None
        self._status_rect: pygame.Rect | None = None
        self._last_game_state: GameState | None = None

    def update(self, *, game_state: GameState, score: int, lives: int) -> None:
        """Actualiza la representación del HUD cuando cambian los datos de la partida."""
        self._update_status(game_state=game_state)

        if score != self._last_score:
            self._last_score = score
            self._score_text = self._info_font.render(
                f"Score: {self._last_score}",
                True,
                self._config.info_text_color,
            )

        if lives != self._last_lives:
            self._last_lives = lives
            self._lives_text = self._info_font.render(
                f"Lives: {self._last_lives}",
                True,
                self._config.info_text_color,
            )
            self._lives_rect = self._lives_text.get_rect(
                topright=(
                    self._config.layout_size[0] - self._config.margin,
                    self._config.margin,
                )
            )

    def draw(self, *, surface: pygame.Surface) -> None:
        """Dibuja el HUD sobre la superficie indicada."""
        surface.blit(self._score_text, (self._config.margin, self._config.margin))
        surface.blit(self._lives_text, self._lives_rect)

        if self._status_text is not None and self._status_rect is not None:
            surface.blit(self._status_text, self._status_rect)

    def _update_status(self, *, game_state: GameState) -> None:
        """Actualiza la representación visual del estado del juego cuando cambia."""
        if game_state is self._last_game_state:
            return

        status_message: str

        match game_state:
            case GameState.RUNNING:
                self._status_text = None
                self._status_rect = None
                self._last_game_state = game_state

                return

            case GameState.PAUSED:
                status_message = self._config.paused_message

            case GameState.VICTORY:
                status_message = self._config.victory_message

            case GameState.GAME_OVER:
                status_message = self._config.game_over_message

        status_text: pygame.Surface = self._status_font.render(
            status_message,
            True,
            self._config.status_text_color,
        )
        self._status_text = status_text

        self._status_rect = status_text.get_rect(
            center=(self._config.layout_size[0] // 2, self._config.layout_size[1] // 2),
        )

        self._last_game_state = game_state
