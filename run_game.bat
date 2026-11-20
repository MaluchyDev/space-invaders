@echo off
setlocal
cd /d "%~dp0"

rem Usa el Python del entorno virtual del proyecto.
set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo ERROR: No se encuentra .venv\Scripts\python.exe
    echo Comprueba que el entorno virtual existe junto a este archivo.
    pause
    exit /b 1
)

rem Permite importar space_invaders desde la estructura src/.
set "PYTHONPATH=%~dp0src"

rem Ejecuta el punto de entrada del paquete.
"%PYTHON_EXE%" -m space_invaders

if errorlevel 1 (
    echo.
    echo ERROR: Space Invaders ha terminado con un error.
    pause
    exit /b 1
)

endlocal
