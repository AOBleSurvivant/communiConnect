# 🚀 GUIDE DE DÉMARRAGE RAPIDE - COMMUNICONNECT

## 📋 **PROBLÈMES FRÉQUENTS ET SOLUTIONS**

### **❌ Problème 1: "manage.py not found"**
**Cause:** Mauvais répertoire de travail
**Solution:**
```bash
# Assurez-vous d'être dans le répertoire racine
cd C:\Users\DELL\Desktop\communiConnect\communiConnect
```

### **❌ Problème 2: PowerShell ne reconnaît pas `&&`**
**Cause:** PowerShell utilise `;` au lieu de `&&`
**Solution:**
```powershell
# Au lieu de: cd backend && python manage.py runserver
# Utilisez:
cd backend; python manage.py runserver
```

### **❌ Problème 3: Ports déjà utilisés**
**Cause:** Autres processus utilisent les ports 8000/3000
**Solution:**
```powershell
# Arrêter les processus Python
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force

# Arrêter les processus Node.js
Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Stop-Process -Force
```

---

## 🎯 **SOLUTIONS DÉFINITIVES**

### **Option 1: Script PowerShell Automatique (RECOMMANDÉ)**
```powershell
# Exécuter le script PowerShell
.\demarrer_serveurs.ps1
```

### **Option 2: Script Batch Simple**
```cmd
# Exécuter le script batch
demarrer_serveurs.bat
```

### **Option 3: Démarrage Manuel**
```powershell
# Terminal 1 - Backend
cd backend
python manage.py runserver 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## 🔧 **VÉRIFICATIONS PRÉALABLES**

### **1. Vérifier la structure des répertoires**
```
communiConnect/
├── backend/
│   ├── manage.py          ✅ Doit exister
│   └── communiconnect/
├── frontend/
│   ├── package.json       ✅ Doit exister
│   └── src/
└── demarrer_serveurs.ps1  ✅ Script de démarrage
```

### **2. Vérifier les dépendances**
```powershell
# Vérifier Python
python --version

# Vérifier Node.js
node --version

# Vérifier npm
npm --version
```

### **3. Installer les dépendances si nécessaire**
```powershell
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## 🚀 **DÉMARRAGE EN 3 ÉTAPES**

### **Étape 1: Préparation**
```powershell
# Aller dans le répertoire racine
cd C:\Users\DELL\Desktop\communiConnect\communiConnect

# Vérifier la structure
dir backend\manage.py
dir frontend\package.json
```

### **Étape 2: Démarrage automatique**
```powershell
# Option A: PowerShell (recommandé)
.\demarrer_serveurs.ps1

# Option B: Batch
demarrer_serveurs.bat
```

### **Étape 3: Vérification**
```powershell
# Tester le backend
curl http://localhost:8000/api/users/

# Tester le frontend
curl http://localhost:3000
```

---

## 📊 **URLS IMPORTANTES**

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Interface utilisateur |
| **Backend** | http://localhost:8000 | API Django |
| **Admin** | http://localhost:8000/admin/ | Interface d'administration |
| **API Docs** | http://localhost:8000/api/schema/ | Documentation API |

---

## 🛠️ **DÉPANNAGE RAPIDE**

### **Problème: "Port 8000 already in use"**
```powershell
# Solution 1: Arrêter les processus
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Solution 2: Utiliser un autre port
python backend\manage.py runserver 8001
```

### **Problème: "Module not found"**
```powershell
# Réinstaller les dépendances
cd backend
pip install -r requirements.txt
```

### **Problème: "npm start failed"**
```powershell
# Réinstaller les dépendances frontend
cd frontend
npm install
npm start
```

---

## 📝 **COMMANDES UTILES**

### **Arrêter tous les serveurs**
```powershell
# Arrêter Python
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force

# Arrêter Node.js
Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Stop-Process -Force
```

### **Redémarrer les serveurs**
```powershell
# Arrêter puis redémarrer
.\demarrer_serveurs.ps1
```

### **Vérifier les processus**
```powershell
# Voir tous les processus Python
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Voir tous les processus Node.js
Get-Process | Where-Object {$_.ProcessName -like "*node*"}
```

---

## ✅ **CHECKLIST DE DÉMARRAGE**

- [ ] Être dans le répertoire racine `communiConnect/`
- [ ] Vérifier que `backend/manage.py` existe
- [ ] Vérifier que `frontend/package.json` existe
- [ ] Vérifier que Python est installé
- [ ] Vérifier que Node.js est installé
- [ ] Exécuter `.\demarrer_serveurs.ps1`
- [ ] Vérifier que http://localhost:8000 répond
- [ ] Vérifier que http://localhost:3000 répond

---

## 🎉 **RÉSULTAT ATTENDU**

Après un démarrage réussi, vous devriez voir :

```
🎉 TOUS LES SERVEURS SONT DÉMARRÉS !

📱 Frontend React: http://localhost:3000
🔧 Backend Django: http://localhost:8000
📚 API Documentation: http://localhost:8000/api/schema/
```

**CommuniConnect est maintenant prêt à être utilisé !** 🚀 