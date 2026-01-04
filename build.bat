@echo off
title Stealth Storage - Quintero Dev Studio
cls

echo ===================================================
echo           COMPILADOR DE STEALTH STORAGE
echo ===================================================

:: 1. Intentar activar el entorno virtual
if exist venv\Scripts\activate (
    echo [+] Activando entorno virtual...
    call venv\Scripts\activate
) else (
    echo [!] AVISO: No se encontro la carpeta 'venv'. Se usara el Python global.
)

:: 2. Limpiar carpetas de compilacion previas
echo [+] Limpiando archivos temporales...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

:: 3. Lanzar la compilacion
echo [+] Iniciando PyInstaller...
echo [!] Esto puede tardar un par de minutos...
python -m PyInstaller --name "StealthStorage" ^
--onefile ^
--noconsole ^
--clean ^
--collect-all customtkinter ^
--add-data "src;src" ^
app.py

echo.
echo ===================================================
echo    PROCESO FINALIZADO. REVISA LA CARPETA 'DIST'
echo ===================================================
pause