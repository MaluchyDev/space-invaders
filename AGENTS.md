# Space Invaders — Instrucciones del proyecto

## Contexto técnico

- Python >=3.15.
- Pygame CE >=2.5.8.
- Arquitectura modular con estructura `src/space_invaders/`.
- Ruff y mypy como herramientas de calidad.
- Uso de Git para el control de versiones.

## Metodología del proyecto

- Desarrollo mediante Micro-Labs y criterios de aceptación.
- Cada Micro-Lab debe respetar su contrato y Definition of Done.
- El usuario implementa las soluciones de forma autónoma.
- No anticipes funcionalidades de Micro-Labs posteriores.
- Prioriza la consolidación de conocimientos frente a la complejidad innecesaria.

## Arquitectura y diseño

- `Game` coordina el ciclo principal del juego.
- Las entidades gestionan sus responsabilidades individuales.
- `EnemyFleet` coordina el comportamiento colectivo de los enemigos.
- Utiliza delta time para el movimiento independiente del framerate.
- Mantén separadas las responsabilidades de entrada, actualización y dibujo.
- Respeta las convenciones y los alias de tipos existentes.

## Revisión técnica

- Comprueba que cada implementación respeta su contrato.
- Señala errores funcionales, problemas de diseño y oportunidades de mejora.
- No propongas nuevas abstracciones sin una justificación clara.
- Respeta las decisiones arquitectónicas ya validadas, salvo que exista un problema demostrable.
- Aplica las instrucciones globales de tutoría, calidad y autonomía.
