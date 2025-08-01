@echo off
echo ========================================
echo Iniciando Proyecto ML Local
echo ========================================

echo.
echo 1. Iniciando API en puerto 8001...
start "API Server" cmd /k "python api_simple.py"

echo.
echo 2. Esperando 5 segundos para que la API se inicie...
timeout /t 5 /nobreak > nul

echo.
echo 3. Iniciando Frontend en puerto 3000...
cd frontend
start "Frontend" cmd /k "npm start"

echo.
echo ========================================
echo Proyecto iniciado correctamente!
echo ========================================
echo.
echo API: http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause > nul 