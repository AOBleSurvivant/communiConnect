@echo off
chcp 65001 >nul
title CommuniConnect - Démarrage des Serveurs

echo.
echo 🚀 DÉMARRAGE DES SERVEURS COMMUNICONNECT
echo ==========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python 3.8+ et réessayer
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Vérifier si Node.js est installé
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js n'est pas installé ou pas dans le PATH
    echo Le serveur frontend ne sera pas démarré
    pause
    exit /b 1
)

echo ✅ Node.js détecté
echo.

REM Vérifier si les dépendances backend sont installées
if not exist "backend\venv" (
    echo 📦 Création de l'environnement virtuel backend...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
cd backend
call venv\Scripts\activate.bat
cd ..

REM Vérifier si les migrations sont à jour
echo 🗄️  Vérification des migrations...
cd backend
python manage.py makemigrations
python manage.py migrate
cd ..

REM Vérifier si les dépendances frontend sont installées
if not exist "frontend\node_modules" (
    echo 📦 Installation des dépendances frontend...
    cd frontend
    npm install
    cd ..
)

echo.
echo 🐍 Démarrage du serveur backend Django...
start "Backend Django" cmd /k "cd backend && call venv\Scripts\activate.bat && python manage.py runserver 8000"

echo ⏳ Attente du démarrage du serveur backend...
timeout /t 5 /nobreak >nul

echo.
echo ⚛️  Démarrage du serveur frontend React...
start "Frontend React" cmd /k "cd frontend && npm start"

echo ⏳ Attente du démarrage du serveur frontend...
timeout /t 10 /nobreak >nul

echo.
echo 🎉 TOUS LES SERVEURS SONT DÉMARRÉS !
echo.
echo 📱 Frontend React: http://localhost:3000
echo 🔧 Backend Django: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/api/schema/
echo.
echo 💡 Pour arrêter les serveurs, fermez les fenêtres ou appuyez sur Ctrl+C
echo.

pause 