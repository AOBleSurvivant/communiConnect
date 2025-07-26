@echo off
echo ========================================
echo   DEMARRAGE SERVEUR DJANGO COMMUNICONNECT
echo ========================================
echo.

cd /d "%~dp0backend"
echo Repertoire actuel: %CD%
echo.

echo Verification de l'environnement Django...
python manage.py check
if %errorlevel% neq 0 (
    echo ERREUR: Django n'est pas configure correctement
    pause
    exit /b 1
)

echo.
echo Demarrage du serveur Django...
echo URL: http://127.0.0.1:8000/
echo Pour arreter: CTRL+C
echo.

python manage.py runserver 127.0.0.1:8000

pause 