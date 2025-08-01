@echo off
echo ========================================
echo Iniciando Proyecto ML con Docker
echo ========================================

echo.
echo 1. Deteniendo contenedores existentes...
docker-compose -f docker-compose.simple.yml down

echo.
echo 2. Construyendo y ejecutando contenedores...
docker-compose -f docker-compose.simple.yml up --build

echo.
echo ========================================
echo Proyecto iniciado con Docker!
echo ========================================
echo.
echo API: http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo Para detener: docker-compose -f docker-compose.simple.yml down
echo.
pause 