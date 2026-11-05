"""Punto de entrada de la aplicación Space Invaders."""

import pygame

from space_invaders.game import Game


def main() -> None:
    """Inicia la aplicación y garantiza el cierre Pygame."""
    pygame.init()
    try:
        game: Game = Game()
        game.run()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
