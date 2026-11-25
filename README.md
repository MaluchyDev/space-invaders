# Space Invaders — Vertical Slice

Un pequeño videojuego arcade desarrollado en **Python y Pygame CE** como proyecto de consolidación de conocimientos de programación y desarrollo de videojuegos.

Esta versión didáctica, no oficial, reproduce las mecánicas esenciales de un juego de invasores espaciales: controlar una nave, disparar a una formación enemiga y sobrevivir a sus ataques. El proyecto prioriza un código claro, modular y mantenible frente a la incorporación de funcionalidades adicionales.

## Características

- Movimiento horizontal del jugador con límites de pantalla.
- Formación de **24 enemigos** distribuida en 3 filas y 8 columnas, con desplazamiento lateral, rebote y descenso.
- Disparos del jugador y de los enemigos, con límites de proyectiles y tiempos de espera (*cooldowns*).
- Detección de colisiones, puntuación y sistema de vidas.
- Invulnerabilidad temporal tras recibir daño, indicada mediante parpadeo.
- Estados de partida: `RUNNING`, `PAUSED`, `VICTORY` y `GAME_OVER`.
- HUD con puntuación, vidas y mensajes de estado.
- Reinicio de partida sin cerrar la aplicación.
- Cuatro efectos de sonido: disparo del jugador, disparo enemigo, destrucción de enemigos y daño al jugador.

## Requisitos

- **Python 3.15 o superior**, de acuerdo con `pyproject.toml`.
- **Pygame CE 2.5.8 o superior**.
- Windows para utilizar el lanzador `run_game.bat` (el código Python no depende de ese archivo).

## Instalación

Desde la **raíz del proyecto**, donde se encuentra `pyproject.toml`, crea un entorno virtual e instala el paquete en modo editable.

En Windows, desde una terminal:

```powershell
py -3.15 -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
```

El comando de instalación también instala la dependencia `pygame-ce` declarada en `pyproject.toml`.

## Ejecución

### Lanzador de Windows

Ejecuta `run_game.bat` desde la raíz del proyecto (por ejemplo, con doble clic). El lanzador utiliza el intérprete de `.venv`, configura la ruta `src/` y ejecuta el paquete como módulo.

> El lanzador requiere que el entorno virtual `.venv` ya exista y tenga instaladas las dependencias.

### Desde una terminal

Con el entorno creado y el paquete instalado:

```powershell
.venv\Scripts\python.exe -m space_invaders
```

En PyCharm también puedes utilizar una configuración de ejecución de tipo **Module name** con el valor `space_invaders`, seleccionando el intérprete del entorno virtual del proyecto.

## Controles

| Tecla | Acción |
| --- | --- |
| `←` / `→` o `A` / `D` | Mover la nave a izquierda o derecha |
| `Espacio` | Disparar |
| `P` | Pausar o reanudar la partida |
| `R` | Iniciar una nueva partida tras `VICTORY` o `GAME_OVER` |
| `Esc` | Salir del juego |

También puedes cerrar la aplicación mediante el botón de cierre de la ventana.

## Reglas del juego

- La partida comienza con **3 vidas** y **0 puntos**.
- Cada enemigo destruido suma **10 puntos**.
- El jugador dispone de **un único proyectil activo** a la vez.
- Los enemigos pueden mantener hasta **dos proyectiles activos** simultáneamente.
- Tras recibir daño, la nave dispone de **1,5 segundos de invulnerabilidad**.
- Se consigue la **victoria** al eliminar todos los enemigos.
- La partida termina en **derrota** si se agotan las vidas o la formación alcanza la línea defensiva del jugador.
- La pausa detiene la simulación y sus temporizadores. El reinicio restablece los elementos de una nueva partida, pero mantiene abierta la aplicación.

## Organización del proyecto

```text
space-invaders/
├── src/
│   └── space_invaders/
│       ├── __init__.py
│       ├── __main__.py          # Punto de entrada
│       ├── game.py              # Game loop y coordinación
│       ├── game_state.py        # Estados de partida
│       ├── player.py            # Nave del jugador
│       ├── enemy.py             # Enemigo individual
│       ├── enemy_fleet.py       # Formación y comportamiento colectivo
│       ├── projectile.py        # Proyectiles
│       ├── hud.py               # Puntuación, vidas y mensajes
│       ├── sound_effects.py     # Carga y reproducción de sonidos
│       ├── settings.py          # Constantes y configuración
│       ├── type_aliases.py      # Alias de tipos compartidos
│       └── assets/
│           └── sfx/             # Archivos WAV
├── pyproject.toml
├── .gitignore
├── run_game.bat
└── README.md
```

La clase `Game` coordina los sistemas; las entidades administran su movimiento y representación; `HUD` se ocupa de la información en pantalla, y `SoundEffects` encapsula el audio. El movimiento utiliza **delta time** para evitar depender directamente de los FPS.

## Comprobaciones de calidad

Durante el desarrollo se utilizan **Ruff** y **mypy**. Una vez instaladas estas herramientas en el entorno de desarrollo, las comprobaciones habituales son:

```powershell
.venv\Scripts\python.exe -m ruff check src
.venv\Scripts\python.exe -m ruff format --check src
.venv\Scripts\python.exe -m mypy
```

La configuración de las herramientas y las dependencias de desarrollo están definidas en `pyproject.toml`.

## Alcance del proyecto

Este repositorio contiene un **vertical slice educativo**, no una recreación comercial completa. Su objetivo ha sido consolidar el bucle de juego, las entidades, la gestión del tiempo, las colisiones, los estados, el feedback y la organización modular del código.

Las posibles mejoras —niveles, dificultad progresiva, sprites, animaciones o partículas— quedan fuera del alcance de esta versión y podrían estudiarse en una evolución futura.

## Recursos y atribuciones

Los efectos de sonido utilizados por el juego se encuentran en `src/space_invaders/assets/sfx/`. Antes de redistribuir o publicar los archivos de audio, deben comprobarse sus condiciones de uso y añadirse los créditos o licencias correspondientes cuando proceda.
