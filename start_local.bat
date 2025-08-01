@echo off
echo Iniciando sistema ML local...

echo 1. Activando entorno virtual...
call venv\Scripts\activate

echo 2. Iniciando Ray head node...
start "Ray Head" cmd /k "venv\Scripts\activate && ray start --head --port=6379 --dashboard-port=8265 --dashboard-host=0.0.0.0"

echo 3. Esperando que Ray inicie...
timeout /t 5

echo 4. Iniciando API backend...
start "API Backend" cmd /k "venv\Scripts\activate && cd microservices\api && python main.py"

echo 5. Esperando que API inicie...
timeout /t 5

echo 6. Iniciando Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo Sistema iniciado! Abre http://localhost:3000 en tu navegador
echo.
echo Servicios disponibles:
echo - Frontend: http://localhost:3000
echo - API Backend: http://localhost:8000
echo - Ray Dashboard: http://localhost:8265
echo.
pause 