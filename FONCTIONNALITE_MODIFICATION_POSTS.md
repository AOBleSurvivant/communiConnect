# 🔧 Fonctionnalité de Modification des Posts

## 📋 Vue d'ensemble

La fonctionnalité de modification des posts permet aux utilisateurs de modifier leurs publications **pendant les 30 premières minutes** après leur création.

## ⏰ Limite de temps

- **Durée** : 30 minutes après la création du post
- **Raison** : Éviter les abus et maintenir l'intégrité des discussions
- **Message d'erreur** : "Vous ne pouvez plus modifier ce post. La limite de 30 minutes est dépassée."

## 🔐 Sécurité

### Vérifications effectuées :
1. **Authentification** : L'utilisateur doit être connecté
2. **Autorisation** : Seul l'auteur du post peut le modifier
3. **Limite de temps** : Maximum 30 minutes après création
4. **Validation** : Le contenu ne peut pas être vide

## 🛠️ Implémentation Technique

### Backend (Django)

#### Modèle Post
```python
class Post(models.Model):
    # ... autres champs ...
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Vue de modification
```python
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    def perform_update(self, serializer):
        # Vérifier l'auteur
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("Vous ne pouvez modifier que vos propres posts")
        
        # Vérifier la limite de temps (30 minutes)
        from django.utils import timezone
        from datetime import timedelta
        
        time_limit = serializer.instance.created_at + timedelta(minutes=30)
        if timezone.now() > time_limit:
            raise permissions.PermissionDenied(
                "Vous ne pouvez plus modifier ce post. La limite de 30 minutes est dépassée."
            )
        
        serializer.save()
```

### Frontend (React)

#### Composant EditPostModal
- Interface utilisateur pour la modification
- Validation côté client
- Gestion des erreurs
- Feedback utilisateur

#### Intégration dans PostCard
- Bouton "Modifier" visible seulement pour l'auteur
- Vérification de la limite de temps côté client
- Modal de modification

## 🎯 Fonctionnalités

### ✅ Ce qui peut être modifié :
- **Contenu** : Le texte principal du post
- **Titre** : Le titre optionnel du post
- **Type de post** : info, event, help, announcement, discussion

### ❌ Ce qui ne peut pas être modifié :
- **Auteur** : Impossible de changer l'auteur
- **Date de création** : Reste inchangée
- **Médias** : Les fichiers médias ne peuvent pas être modifiés
- **Métadonnées** : Likes, commentaires, etc.

## 🔄 API Endpoints

### Modification d'un post
```
PUT /api/posts/{id}/
```

**Corps de la requête :**
```json
{
  "content": "Nouveau contenu du post",
  "title": "Nouveau titre (optionnel)",
  "post_type": "info"
}
```

**Réponse de succès (200) :**
```json
{
  "id": 1,
  "content": "Nouveau contenu du post",
  "title": "Nouveau titre",
  "post_type": "info",
  "author": {...},
  "created_at": "2025-07-19T10:00:00Z",
  "updated_at": "2025-07-19T10:15:00Z"
}
```

**Réponse d'erreur (403) :**
```json
{
  "detail": "Vous ne pouvez plus modifier ce post. La limite de 30 minutes est dépassée."
}
```

## 🧪 Tests

### Script de test automatique
```bash
python test_post_editing.py
```

**Tests effectués :**
1. ✅ Création de post
2. ✅ Modification dans les 30 minutes
3. ✅ Vérification de la modification
4. ✅ Limite de temps (30 minutes)
5. ✅ Gestion des erreurs

## 🎨 Interface Utilisateur

### Bouton de modification
- Visible seulement pour l'auteur du post
- Apparaît seulement dans les 30 premières minutes
- Style : Bouton bleu avec icône d'édition

### Modal de modification
- Formulaire complet avec tous les champs modifiables
- Validation en temps réel
- Message d'information sur la limite de temps
- Boutons "Annuler" et "Modifier"

## 📱 Utilisation

### Pour modifier un post :

1. **Identifier** : Le bouton "Modifier" apparaît sur vos posts récents
2. **Cliquer** : Ouvrir le modal de modification
3. **Modifier** : Changer le contenu, titre ou type
4. **Sauvegarder** : Cliquer sur "Modifier" pour confirmer
5. **Confirmation** : Message de succès affiché

### Messages d'information :
- ⏰ "Vous pouvez modifier votre post pendant les 30 premières minutes après sa publication."
- ✅ "Post modifié avec succès !"
- ❌ "Vous ne pouvez plus modifier ce post. La limite de 30 minutes est dépassée."

## 🔧 Configuration

### Limite de temps
Pour modifier la limite de 30 minutes, changer dans `backend/posts/views.py` :
```python
time_limit = serializer.instance.created_at + timedelta(minutes=30)  # Changer 30
```

### Messages d'erreur
Personnaliser les messages dans `backend/posts/views.py` :
```python
raise permissions.PermissionDenied("Votre message personnalisé")
```

## 🚀 Déploiement

### Backend
1. Les migrations sont déjà appliquées
2. La vue `PostDetailView` est déjà configurée
3. Les URLs sont déjà définies

### Frontend
1. Le composant `EditPostModal` est créé
2. L'intégration dans `PostCard` est prête
3. L'API `updatePost` est disponible

## 📊 Statistiques

### Métriques à surveiller :
- Nombre de modifications par jour
- Taux de succès des modifications
- Erreurs de limite de temps
- Temps moyen entre création et modification

## 🔮 Évolutions futures

### Fonctionnalités possibles :
- **Historique des modifications** : Garder un log des changements
- **Limite configurable** : Permettre à l'admin de changer la limite
- **Notifications** : Informer les abonnés des modifications
- **Versioning** : Permettre de revenir à une version précédente

---

**Status** : ✅ **IMPLÉMENTÉ ET OPÉRATIONNEL**

**Dernière mise à jour** : 19 juillet 2025 