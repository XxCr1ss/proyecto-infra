#!/bin/bash
echo "Iniciando sistema ML local..."

echo "1. Activando entorno virtual..."
source venv/bin/activate

echo "2. Iniciando Ray head node..."
ray start --head --port=6379 --dashboard-port=8265 --dashboard-host=0.0.0.0 &
RAY_PID=$!

echo "3. Esperando que Ray inicie..."
sleep 5

echo "4. Iniciando API backend..."
cd microservices/api
python main.py &
API_PID=$!

echo "5. Esperando que API inicie..."
sleep 5

echo "6. Iniciando Frontend..."
cd ../../frontend
npm start &
FRONTEND_PID=$!

echo "Sistema iniciado! Abre http://localhost:3000 en tu navegador"
echo ""
echo "Servicios disponibles:"
echo "- Frontend: http://localhost:3000"
echo "- API Backend: http://localhost:8000"
echo "- Ray Dashboard: http://localhost:8265"
echo ""
echo "Para detener: kill $RAY_PID $API_PID $FRONTEND_PID"

# Mantener script ejecutándose
wait 