# 🧪 GUIDE DE TEST MANUEL - COMMUNICONNECT

## 📋 **PLAN DE TEST COMPLET**

### **🎯 Objectif**
Tester manuellement toutes les fonctionnalités de CommuniConnect pour s'assurer qu'elles fonctionnent correctement.

---

## 🚀 **ÉTAPE 1: DÉMARRAGE DES SERVEURS**

### **Backend (Django)**
```bash
cd backend
python manage.py runserver
```
**Vérification** : http://127.0.0.1:8000/admin/ accessible

### **Frontend (React)**
```bash
cd frontend
npm start
```
**Vérification** : http://localhost:3002 accessible

---

## 🔐 **ÉTAPE 2: TEST AUTHENTIFICATION**

### **2.1 Page d'Accueil**
- [ ] **URL** : http://localhost:3002
- [ ] **Vérifications** :
  - Page se charge correctement
  - Logo CommuniConnect visible
  - Boutons "Connexion" et "Inscription" présents
  - Design responsive

### **2.2 Inscription**
- [ ] **URL** : http://localhost:3002/register
- [ ] **Tests** :
  - Remplir le formulaire d'inscription
  - Sélectionner un quartier (obligatoire)
  - Valider l'inscription
  - Vérifier la redirection vers le dashboard

**Données de test** :
```
Nom d'utilisateur: test_user_123
Email: test123@test.gn
Mot de passe: test123456
Prénom: Test
Nom: User
Quartier: Boké Centre
```

### **2.3 Connexion**
- [ ] **URL** : http://localhost:3002/login
- [ ] **Tests** :
  - Se connecter avec un compte existant
  - Vérifier la redirection vers le dashboard
  - Tester la déconnexion

**Compte de test** :
```
Email: mariam.diallo@test.gn
Mot de passe: test123456
```

---

## 🏠 **ÉTAPE 3: TEST DASHBOARD**

### **3.1 Page Dashboard**
- [ ] **URL** : http://localhost:3002/dashboard
- [ ] **Vérifications** :
  - Navigation visible (Dashboard, Posts, Utilisateurs, Profil)
  - Posts récents affichés
  - Informations utilisateur visibles
  - Bouton "Nouveau Post" présent

### **3.2 Navigation**
- [ ] **Tests** :
  - Cliquer sur "Posts" → Vérifier la page
  - Cliquer sur "Utilisateurs" → Vérifier la page
  - Cliquer sur "Profil" → Vérifier la page
  - Retourner au Dashboard

---

## 📝 **ÉTAPE 4: TEST POSTS**

### **4.1 Création de Post**
- [ ] **Action** : Cliquer sur "Nouveau Post"
- [ ] **Tests** :
  - Remplir le contenu du post
  - Choisir la visibilité (Public/Privé)
  - Publier le post
  - Vérifier l'apparition dans la liste

### **4.2 Interaction avec les Posts**
- [ ] **Like/Unlike** :
  - Cliquer sur le bouton "Like"
  - Vérifier l'augmentation du compteur
  - Cliquer à nouveau pour "Unlike"
  - Vérifier la diminution du compteur

- [ ] **Commentaires** :
  - Cliquer sur "Commenter"
  - Écrire un commentaire
  - Publier le commentaire
  - Vérifier l'affichage

### **4.3 Filtrage des Posts**
- [ ] **Tests** :
  - Filtrer par "Tous les posts"
  - Filtrer par "Mes posts"
  - Filtrer par localisation
  - Vérifier les résultats

---

## 👥 **ÉTAPE 5: TEST UTILISATEURS**

### **5.1 Page Utilisateurs**
- [ ] **URL** : http://localhost:3002/users
- [ ] **Vérifications** :
  - Liste des utilisateurs affichée
  - Informations de base visibles (nom, quartier)
  - Boutons d'action présents

### **5.2 Recherche d'Utilisateurs**
- [ ] **Tests** :
  - Utiliser la barre de recherche
  - Rechercher par nom
  - Rechercher par quartier
  - Vérifier les résultats

### **5.3 Profil Utilisateur**
- [ ] **Tests** :
  - Cliquer sur un utilisateur
  - Voir son profil détaillé
  - Vérifier les informations géographiques
  - Voir ses posts

---

## 👤 **ÉTAPE 6: TEST PROFIL**

### **6.1 Page Profil**
- [ ] **URL** : http://localhost:3002/profile
- [ ] **Vérifications** :
  - Informations personnelles affichées
  - Photo de profil visible
  - Quartier et localisation corrects
  - Statistiques utilisateur

### **6.2 Modification du Profil**
- [ ] **Tests** :
  - Modifier la bio
  - Changer la photo de profil
  - Modifier les informations personnelles
  - Sauvegarder les modifications
  - Vérifier les changements

---

## 🗺️ **ÉTAPE 7: TEST GÉOGRAPHIE**

### **7.1 Sélecteur Géographique**
- [ ] **Tests** :
  - Ouvrir le sélecteur de quartier
  - Sélectionner une région
  - Sélectionner une préfecture
  - Sélectionner une commune
  - Sélectionner un quartier
  - Vérifier la sélection

### **7.2 Filtrage Géographique**
- [ ] **Tests** :
  - Filtrer les posts par quartier
  - Filtrer les utilisateurs par région
  - Vérifier la pertinence des résultats

---

## 🔔 **ÉTAPE 8: TEST NOTIFICATIONS**

### **8.1 Notifications**
- [ ] **Tests** :
  - Vérifier l'icône de notifications
  - Cliquer pour voir les notifications
  - Marquer comme lues
  - Vérifier les différents types

---

## 📱 **ÉTAPE 9: TEST RESPONSIVE**

### **9.1 Mobile**
- [ ] **Tests** :
  - Ouvrir sur mobile (F12 → Device toolbar)
  - Vérifier la navigation mobile
  - Tester les formulaires
  - Vérifier l'affichage des posts

### **9.2 Tablette**
- [ ] **Tests** :
  - Tester sur tablette
  - Vérifier l'adaptation du layout
  - Tester la navigation

---

## 🔧 **ÉTAPE 10: TEST PERFORMANCE**

### **10.1 Temps de Chargement**
- [ ] **Tests** :
  - Mesurer le temps de chargement des pages
  - Vérifier la vitesse de l'API
  - Tester avec plusieurs posts

### **10.2 Gestion des Erreurs**
- [ ] **Tests** :
  - Tester avec une connexion lente
  - Vérifier les messages d'erreur
  - Tester la récupération après erreur

---

## ✅ **CHECKLIST FINALE**

### **Fonctionnalités Principales**
- [ ] Authentification (Inscription/Connexion)
- [ ] Dashboard
- [ ] Création et gestion des posts
- [ ] Like/Commentaire
- [ ] Gestion des utilisateurs
- [ ] Profil utilisateur
- [ ] Géographie
- [ ] Notifications

### **Interface Utilisateur**
- [ ] Design responsive
- [ ] Navigation intuitive
- [ ] Messages d'erreur clairs
- [ ] Feedback utilisateur
- [ ] Accessibilité

### **Performance**
- [ ] Temps de chargement acceptable
- [ ] Pas de bugs visuels
- [ ] Fonctionnement fluide
- [ ] Gestion des erreurs

---

## 🐛 **PROBLÈMES COURANTS À VÉRIFIER**

### **Authentification**
- [ ] Token expiré
- [ ] Erreurs de validation
- [ ] Redirection incorrecte

### **Posts**
- [ ] Posts qui ne se chargent pas
- [ ] Likes qui ne fonctionnent pas
- [ ] Commentaires qui ne s'affichent pas

### **Géographie**
- [ ] Sélecteur qui ne fonctionne pas
- [ ] Données géographiques manquantes
- [ ] Filtrage incorrect

### **Interface**
- [ ] Problèmes d'affichage mobile
- [ ] Navigation cassée
- [ ] Formulaires non fonctionnels

---

## 📊 **RAPPORT DE TEST**

Après chaque test, noter :
- ✅ **Réussi**
- ❌ **Échoué**
- ⚠️ **Problème mineur**
- 🔧 **Nécessite correction**

**Date du test** : _______________
**Testeur** : _______________
**Version** : _______________

---

## 🎯 **OBJECTIFS DE QUALITÉ**

- **100% des fonctionnalités principales** doivent fonctionner
- **Interface responsive** sur tous les appareils
- **Performance optimale** (< 3s de chargement)
- **Expérience utilisateur fluide** sans bugs majeurs
- **Sécurité** des données utilisateur

**CommuniConnect doit offrir une expérience utilisateur exceptionnelle !** 🚀 