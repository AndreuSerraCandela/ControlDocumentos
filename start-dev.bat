@echo off
echo Iniciando servidor de desarrollo...
echo.

echo Iniciando API Backend...
start "API Backend" cmd /k "cd . && python main.py"

echo Esperando 3 segundos...
timeout /t 3 /nobreak > nul

echo Iniciando Frontend React...
start "Frontend React" cmd /k "cd frontend && npm start"

echo.
echo Servidores iniciados:
echo - API Backend: http://localhost:8000
echo - Frontend React: http://localhost:3000
echo.
echo Presiona cualquier tecla para cerrar...
pause > nul
