# Script de démarrage des serveurs CommuniConnect
# Auteur: CommuniConnect Team
# Date: 2025

Write-Host "🚀 DÉMARRAGE DES SERVEURS COMMUNICONNECT" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Vérifier si Python est installé
try {
    $pythonVersion = python --version
    Write-Host "✅ Python détecté: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Python 3.8+ et réessayer" -ForegroundColor Yellow
    exit 1
}

# Vérifier si les dépendances backend sont installées
if (-not (Test-Path "backend\venv")) {
    Write-Host "📦 Création de l'environnement virtuel backend..." -ForegroundColor Blue
    Set-Location "backend"
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Set-Location ".."
}

# Activer l'environnement virtuel
Write-Host "🔧 Activation de l'environnement virtuel..." -ForegroundColor Blue
Set-Location "backend"
. .\venv\Scripts\Activate.ps1
Set-Location ".."

# Vérifier si les migrations sont à jour
Write-Host "🗄️  Vérification des migrations..." -ForegroundColor Blue
Set-Location "backend"
python manage.py makemigrations
python manage.py migrate
Set-Location ".."

# Vérifier si un processus utilise déjà le port 8000
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000) {
    Write-Host "⚠️  Le port 8000 est déjà utilisé" -ForegroundColor Yellow
    $kill = Read-Host "Voulez-vous arrêter le processus sur le port 8000 ? (y/n)"
    if ($kill -eq "y") {
        Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force
        Start-Sleep -Seconds 2
    }
}

# Vérifier si un processus utilise déjà le port 3000
$port3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($port3000) {
    Write-Host "⚠️  Le port 3000 est déjà utilisé" -ForegroundColor Yellow
    $kill = Read-Host "Voulez-vous arrêter le processus sur le port 3000 ? (y/n)"
    if ($kill -eq "y") {
        Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Stop-Process -Force
        Start-Sleep -Seconds 2
    }
}

# Démarrer le serveur backend Django
Write-Host "🐍 Démarrage du serveur backend Django..." -ForegroundColor Blue
Start-Process -FilePath "python" -ArgumentList "backend\manage.py", "runserver", "8000" -WindowStyle Minimized

# Attendre que le serveur backend soit prêt
Write-Host "⏳ Attente du démarrage du serveur backend..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Vérifier si le serveur backend fonctionne
$maxAttempts = 10
$attempt = 0
do {
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/api/users/" -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Serveur backend démarré avec succès sur http://localhost:8000" -ForegroundColor Green
            break
        }
    }
    catch {
        if ($attempt -eq $maxAttempts) {
            Write-Host "❌ Impossible de démarrer le serveur backend" -ForegroundColor Red
            exit 1
        }
        Write-Host "⏳ Tentative $attempt/$maxAttempts..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
} while ($attempt -lt $maxAttempts)

# Vérifier si Node.js est installé
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js détecté: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Node.js n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "Le serveur frontend ne sera pas démarré" -ForegroundColor Yellow
    exit 1
}

# Vérifier si les dépendances frontend sont installées
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "📦 Installation des dépendances frontend..." -ForegroundColor Blue
    Set-Location "frontend"
    npm install
    Set-Location ".."
}

# Démarrer le serveur frontend React
Write-Host "⚛️  Démarrage du serveur frontend React..." -ForegroundColor Blue
Start-Process -FilePath "npm" -ArgumentList "start" -WorkingDirectory "frontend" -WindowStyle Minimized

# Attendre que le serveur frontend soit prêt
Write-Host "⏳ Attente du démarrage du serveur frontend..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Vérifier si le serveur frontend fonctionne
$maxAttempts = 10
$attempt = 0
do {
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Serveur frontend démarré avec succès sur http://localhost:3000" -ForegroundColor Green
            break
        }
    }
    catch {
        if ($attempt -eq $maxAttempts) {
            Write-Host "❌ Impossible de démarrer le serveur frontend" -ForegroundColor Red
            Write-Host "Le serveur backend fonctionne sur http://localhost:8000" -ForegroundColor Green
            exit 1
        }
        Write-Host "⏳ Tentative $attempt/$maxAttempts..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
} while ($attempt -lt $maxAttempts)

# Afficher les URLs
Write-Host ""
Write-Host "🎉 TOUS LES SERVEURS SONT DÉMARRÉS !" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Frontend React: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend Django: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8000/api/schema/" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Pour arrêter les serveurs, fermez cette fenêtre ou appuyez sur Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Garder la fenêtre ouverte
Read-Host "Appuyez sur Entree pour fermer" 