# Script PowerShell pour CommuniConnect
# Gestion automatique de l'environnement virtuel et des serveurs

param(
    [switch]$Force,
    [switch]$TestOnly,
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   COMMUNICONNECT - START SERVER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Fonction pour arrêter les processus
function Stop-CommuniConnectProcesses {
    Write-Host "Arret des processus existants..." -ForegroundColor Yellow
    
    # Arrêter les processus Python
    Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
    Get-Process -Name "python.exe" -ErrorAction SilentlyContinue | Stop-Process -Force
    
    # Arrêter les processus Node.js
    Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force
    Get-Process -Name "node.exe" -ErrorAction SilentlyContinue | Stop-Process -Force
    
    Start-Sleep -Seconds 2
    Write-Host "Processus arretes" -ForegroundColor Green
}

# Fonction pour vérifier les prérequis
function Test-Prerequisites {
    Write-Host "Verification des prerequis..." -ForegroundColor Blue
    
    # Vérifier Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "Python detecte: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "Python non trouve. Veuillez installer Python 3.8+" -ForegroundColor Red
        return $false
    }
    
    # Vérifier Node.js
    try {
        $nodeVersion = node --version
        Write-Host "Node.js detecte: $nodeVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "Node.js non trouve. Veuillez installer Node.js" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Fonction pour configurer le backend
function Setup-Backend {
    Write-Host "Configuration du backend Django..." -ForegroundColor Blue
    
    Set-Location "backend"
    
    # Créer l'environnement virtuel s'il n'existe pas
    if (-not (Test-Path "venv")) {
        Write-Host "Creation de l'environnement virtuel..." -ForegroundColor Yellow
        python -m venv venv
    }
    
    # Activer l'environnement virtuel
    Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    
    # Installer les dépendances
    Write-Host "Installation des dependances Python..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    # Exécuter les migrations
    Write-Host "Execution des migrations..." -ForegroundColor Yellow
    python manage.py makemigrations
    python manage.py migrate
    
    Set-Location ".."
    Write-Host "Backend configure" -ForegroundColor Green
}

# Fonction pour configurer le frontend
function Setup-Frontend {
    Write-Host "Configuration du frontend React..." -ForegroundColor Blue
    
    Set-Location "frontend"
    
    # Installer les dépendances si nécessaire
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installation des dependances Node.js..." -ForegroundColor Yellow
        npm install
    }
    
    Set-Location ".."
    Write-Host "Frontend configure" -ForegroundColor Green
}

# Fonction pour démarrer les serveurs
function Start-Servers {
    Write-Host "Demarrage des serveurs..." -ForegroundColor Blue
    
    if (-not $BackendOnly) {
        # Démarrer le backend
        Write-Host "Demarrage du serveur Django..." -ForegroundColor Yellow
        Start-Process -FilePath "cmd" -ArgumentList "/c", "cd backend && call venv\Scripts\activate.bat && python manage.py runserver 8000" -WindowStyle Minimized
        Start-Sleep -Seconds 5
    }
    
    if (-not $FrontendOnly) {
        # Démarrer le frontend
        Write-Host "Demarrage du serveur React..." -ForegroundColor Yellow
        Start-Process -FilePath "cmd" -ArgumentList "/c", "cd frontend && npm start" -WindowStyle Minimized
        Start-Sleep -Seconds 10
    }
    
    Write-Host "Serveurs demarres" -ForegroundColor Green
}

# Fonction pour tester les serveurs
function Test-Servers {
    Write-Host "Test des serveurs..." -ForegroundColor Blue
    
    $maxAttempts = 10
    $attempt = 0
    
    # Test du backend
    if (-not $FrontendOnly) {
        do {
            $attempt++
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health/" -TimeoutSec 5
                if ($response.StatusCode -eq 200) {
                    Write-Host "Backend fonctionne sur http://localhost:8000" -ForegroundColor Green
                    break
                }
            }
            catch {
                if ($attempt -eq $maxAttempts) {
                    Write-Host "Backend non accessible" -ForegroundColor Red
                    return $false
                }
                Write-Host "Tentative $attempt/$maxAttempts pour le backend..." -ForegroundColor Yellow
                Start-Sleep -Seconds 2
            }
        } while ($attempt -lt $maxAttempts)
    }
    
    # Test du frontend
    if (-not $BackendOnly) {
        $attempt = 0
        do {
            $attempt++
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5
                if ($response.StatusCode -eq 200) {
                    Write-Host "Frontend fonctionne sur http://localhost:3000" -ForegroundColor Green
                    break
                }
            }
            catch {
                if ($attempt -eq $maxAttempts) {
                    Write-Host "Frontend non accessible" -ForegroundColor Red
                    return $false
                }
                Write-Host "Tentative $attempt/$maxAttempts pour le frontend..." -ForegroundColor Yellow
                Start-Sleep -Seconds 2
            }
        } while ($attempt -lt $maxAttempts)
    }
    
    return $true
}

# Fonction principale
function Main {
    # Arrêter les processus existants si demandé
    if ($Force) {
        Stop-CommuniConnectProcesses
    }
    
    # Vérifier les prérequis
    if (-not (Test-Prerequisites)) {
        Write-Host "Prerequis non satisfaits. Arret." -ForegroundColor Red
        return
    }
    
    # Configuration
    if (-not $FrontendOnly) {
        Setup-Backend
    }
    
    if (-not $BackendOnly) {
        Setup-Frontend
    }
    
    # Démarrer les serveurs
    Start-Servers
    
    # Tester les serveurs
    if ($TestOnly -or (Test-Servers)) {
        Write-Host ""
        Write-Host "COMMUNICONNECT DEMARRE AVEC SUCCES !" -ForegroundColor Green
        Write-Host ""
        Write-Host "Frontend React: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "Backend Django: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API Documentation: http://localhost:8000/api/schema/" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Pour arreter les serveurs, fermez les fenetres ou utilisez Ctrl+C" -ForegroundColor Yellow
        Write-Host ""
        
        if ($TestOnly) {
            Write-Host "Mode test active - Arret apres verification" -ForegroundColor Yellow
        } else {
            Write-Host "Appuyez sur Entree pour fermer..." -ForegroundColor Gray
            Read-Host
        }
    } else {
        Write-Host "Echec du demarrage des serveurs" -ForegroundColor Red
    }
}

# Exécution du script
Main 