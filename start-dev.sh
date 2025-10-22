#!/bin/bash

echo "Iniciando servidor de desarrollo..."
echo

echo "Iniciando API Backend..."
python main.py &
BACKEND_PID=$!

echo "Esperando 3 segundos..."
sleep 3

echo "Iniciando Frontend React..."
cd frontend
npm start &
FRONTEND_PID=$!

echo
echo "Servidores iniciados:"
echo "- API Backend: http://localhost:8000"
echo "- Frontend React: http://localhost:3000"
echo
echo "Presiona Ctrl+C para detener todos los servidores..."

# Función para limpiar procesos al salir
cleanup() {
    echo "Deteniendo servidores..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Esperar indefinidamente
wait
