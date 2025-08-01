@echo off
echo ========================================
echo Deteniendo Proyecto ML Local
echo ========================================

echo.
echo Deteniendo procesos de Python (API)...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo.
echo Deteniendo procesos de Node.js (Frontend)...
taskkill /f /im node.exe 2>nul

echo.
echo ========================================
echo Proyecto detenido correctamente!
echo ========================================
echo.
pause 