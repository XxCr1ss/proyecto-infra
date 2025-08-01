@echo off
echo Deteniendo sistema ML local...

echo 1. Deteniendo Ray...
ray stop

echo 2. Deteniendo procesos Node.js...
taskkill /f /im node.exe 2>nul

echo 3. Deteniendo procesos Python...
taskkill /f /im python.exe 2>nul

echo Sistema detenido
pause 