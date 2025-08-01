@echo off
echo ========================================
echo Deteniendo Proyecto ML con Docker
echo ========================================

echo.
echo Deteniendo contenedores...
docker-compose -f docker-compose.simple.yml down

echo.
echo ========================================
echo Proyecto detenido correctamente!
echo ========================================
echo.
pause 