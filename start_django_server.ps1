# Script PowerShell pour démarrer le serveur Django CommuniConnect
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEMARRAGE SERVEUR DJANGO COMMUNICONNECT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Aller dans le répertoire backend
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $scriptPath "backend"
Set-Location $backendPath

Write-Host "Répertoire actuel: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# Vérification de l'environnement Django
Write-Host "Vérification de l'environnement Django..." -ForegroundColor Green
try {
    python manage.py check
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Django n'est pas configuré correctement" -ForegroundColor Red
        Read-Host "Appuyez sur Entrée pour continuer"
        exit 1
    }
} catch {
    Write-Host "ERREUR: Impossible d'exécuter Django" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour continuer"
    exit 1
}

Write-Host ""
Write-Host "Démarrage du serveur Django..." -ForegroundColor Green
Write-Host "URL: http://127.0.0.1:8000/" -ForegroundColor Yellow
Write-Host "Pour arrêter: CTRL+C" -ForegroundColor Yellow
Write-Host ""

# Démarrer le serveur
python manage.py runserver 127.0.0.1:8000 