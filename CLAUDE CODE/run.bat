@echo off
chcp 65001 >nul
title Operador de Residuos S.A.C. — Servidor Web

echo.
echo  ============================================
echo   Operador de Residuos S.A.C. - Sitio Web
echo  ============================================
echo.

:: Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python no encontrado.
    echo  Descarga Python 3.13 desde: https://www.python.org/downloads/
    echo  Asegurate de marcar "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

echo  [1/3] Python encontrado. Verificando entorno virtual...

:: Crear entorno virtual si no existe
if not exist ".venv" (
    echo  [2/3] Creando entorno virtual...
    python -m venv .venv
) else (
    echo  [2/3] Entorno virtual existente. OK.
)

:: Activar entorno virtual e instalar dependencias
echo  [3/3] Instalando dependencias...
call .venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

echo.
echo  ============================================
echo   Servidor iniciado: http://127.0.0.1:5000
echo   Presiona Ctrl+C para detener
echo  ============================================
echo.

:: Abrir el navegador automaticamente
start "" "http://127.0.0.1:5000"

:: Iniciar Flask
python app.py

pause
