@echo off
echo Entrando al entorno virtual
call .venv\Scripts\activate
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio backend en el puerto 5000
start "Backend" cmd /c python backend\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio Inicio y Registro en el puerto 5001
start "AuthService" cmd /c python auth_service\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio Ordenes en el puerto 5002
start "OrdersService" cmd /c python orders_service\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio Tracking en el puerto 5004
start "TrackingService" cmd /c python tracking_service\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio Comidas en el puerto 5006
start "MealService" cmd /c python tracking_service\app.py
timeout /nobreak /t 2 >nul

echo Saliendo del entorno virtual
call deactivate
