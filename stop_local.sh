#!/bin/bash
echo "Deteniendo sistema ML local..."

echo "1. Deteniendo Ray..."
ray stop

echo "2. Deteniendo procesos Node.js..."
pkill -f "npm start" 2>/dev/null
pkill -f "node" 2>/dev/null

echo "3. Deteniendo procesos Python..."
pkill -f "python main.py" 2>/dev/null

echo "Sistema detenido" 