@echo off
echo Entrando al entorno virtual
call .venv\Scripts\activate
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio backend en el puerto 5000
start "Backend" cmd /c python backend\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio en el puerto 5001
start "AuthService" cmd /c python auth_service\app.py
timeout /nobreak /t 2 >nul

echo Saliendo del entorno virtual
call deactivate
