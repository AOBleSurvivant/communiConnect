# Script PowerShell pour démarrer les serveurs CommuniConnect
# CommuniConnect - Démarrage Automatique

Write-Host "🚀 DÉMARRAGE COMMUNICONNECT" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Vérifier si on est dans le bon répertoire
if (-not (Test-Path "backend")) {
    Write-Host "❌ Erreur: Répertoire 'backend' non trouvé" -ForegroundColor Red
    Write-Host "💡 Assurez-vous d'être dans le répertoire racine de CommuniConnect" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path "frontend")) {
    Write-Host "❌ Erreur: Répertoire 'frontend' non trouvé" -ForegroundColor Red
    Write-Host "💡 Assurez-vous d'être dans le répertoire racine de CommuniConnect" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Répertoires vérifiés" -ForegroundColor Green

# Démarrer le backend Django
Write-Host "`n🐍 Démarrage du Backend Django..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python manage.py runserver" -WindowStyle Normal

# Attendre un peu que le backend démarre
Write-Host "⏳ Attente du démarrage du backend..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Démarrer le frontend React
Write-Host "⚛️ Démarrage du Frontend React..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start" -WindowStyle Normal

# Attendre un peu que le frontend démarre
Write-Host "⏳ Attente du démarrage du frontend..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`n🎉 SERVEURS DÉMARRÉS !" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "🌐 Backend: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "🌐 Frontend: http://localhost:3002" -ForegroundColor White
Write-Host "📊 Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "`n💡 Les fenêtres PowerShell restent ouvertes pour surveiller les serveurs" -ForegroundColor Yellow
Write-Host "💡 Fermez les fenêtres pour arrêter les serveurs" -ForegroundColor Yellow

# Attendre que l'utilisateur appuie sur une touche
Write-Host "`n⏸️ Appuyez sur une touche pour continuer..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "`n🧪 Lancement du test automatique..." -ForegroundColor Cyan
python test_complet_site.py

Write-Host "`n✅ Test terminé !" -ForegroundColor Green
Write-Host "📋 Consultez le rapport de test pour plus de détails" -ForegroundColor Yellow 