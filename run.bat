@echo off
echo Entrando al entorno virtual
call .venv\Scripts\activate
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio backend
start "Backend" cmd /c python backend\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio Inicio y Registro
start "AuthService" cmd /c python auth_service\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio Ordenes
start "OrdersService" cmd /c python orders_service\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio Tracking
start "TrackingService" cmd /c python tracking_service\app.py
timeout /nobreak /t 2 >nul

echo Ejecutando microservicio Comidas
start "MealService" cmd /c python meals_service\app.py
timeout /nobreak /t 2 >nul

echo Saliendo del entorno virtual
call deactivate
