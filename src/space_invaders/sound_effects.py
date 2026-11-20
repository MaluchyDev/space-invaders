"""Proporciona los efectos de sonido del juego."""

import pygame

import space_invaders.settings as cfg


class SoundEffects:
    """Carga, configura y reproduce los efectos de sonido del juego."""

    def __init__(self) -> None:
        """Carga y configura los efectos de sonido del juego."""
        # === CARGA DE EFECTOS DE SONIDO ===
        self._player_shot_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            file=cfg.SFX_PLAYER_SHOT_PATH
        )
        self._player_hit_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            file=cfg.SFX_PLAYER_HIT_PATH
        )
        self._enemy_shot_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            file=cfg.SFX_ENEMY_SHOT_PATH
        )
        self._enemy_destroyed_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            file=cfg.SFX_ENEMY_DESTROYED_PATH
        )

        # === CONFIGURACIÓN DE VOLÚMENES ===
        self._player_shot_sound.set_volume(cfg.SFX_PLAYER_SHOT_VOLUME)
        self._player_hit_sound.set_volume(cfg.SFX_PLAYER_HIT_VOLUME)
        self._enemy_shot_sound.set_volume(cfg.SFX_ENEMY_SHOT_VOLUME)
        self._enemy_destroyed_sound.set_volume(cfg.SFX_ENEMY_DESTROYED_VOLUME)

    def play_player_shot(self) -> None:
        """Reproduce el sonido del disparo del jugador."""
        self._player_shot_sound.play()

    def play_player_hit(self) -> None:
        """Reproduce el sonido de daño al jugador."""
        self._player_hit_sound.play()

    def play_enemy_shot(self) -> None:
        """Reproduce el sonido del disparo del enemigo."""
        self._enemy_shot_sound.play()

    def play_enemy_destroyed(self) -> None:
        """Reproduce el sonido de un enemigo destruido."""
        self._enemy_destroyed_sound.play()
