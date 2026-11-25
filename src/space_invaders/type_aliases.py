"""Define los tipos compartidos utilizados por Space Invaders."""

from typing import Literal

# === GEOMETRÍA ===
type Size = tuple[int, int]
type Position2D = tuple[int, int]
type Position2DFloat = tuple[float, float]

# Desplazamiento visual continuo; se discretiza al llegar al render.
type Offset2D = tuple[float, float] # Partículas

# === PRESENTACIÓN ===
type ColorRGB = tuple[int, int, int]

# === INPUT ===
type HorizontalDirection = Literal[-1, 0, 1]
