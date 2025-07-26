# Demandes d'Aide Communautaire

## Vue d'ensemble

Cette application gère les demandes d'aide communautaire, inspirée de Nextdoor mais distincte des alertes d'urgence. Elle permet aux utilisateurs de :

- **Demander de l'aide** pour des besoins non urgents (matériel, présence, services, etc.)
- **Offrir de l'aide** à la communauté
- **Localiser** les demandes sur une carte interactive
- **Interagir** avec les demandes via des réponses et messages

## Différence avec les Alertes

| Aspect | Alertes | Demandes d'Aide |
|--------|---------|-----------------|
| **Nature** | Urgences, dangers | Solidarité, entraide |
| **Types** | Incendie, agression, etc. | Matériel, présence, services |
| **Urgence** | Immédiate | Variable (immédiat à continu) |
| **Géolocalisation** | Précise | Précise + zones de proximité |
| **Notifications** | Push, SMS | Email, in-app |

## Modèles de données

### HelpRequest

**Champs principaux :**
- `request_type` : 'request' (demande) ou 'offer' (offre)
- `need_type` : Type de besoin (matériel, présence, service, etc.)
- `for_who` : Destinataire (moi-même, famille, voisin, communauté)
- `duration_type` : Durée estimée (immédiat, cette semaine, etc.)
- `proximity_zone` : Zone de proximité (quartier, ville, région)

**Géolocalisation :**
- `latitude`, `longitude` : Coordonnées GPS
- `address`, `neighborhood`, `city`, `postal_code` : Adresse structurée

**Statut et suivi :**
- `status` : open, in_progress, completed, cancelled
- `responses_count`, `views_count` : Métriques d'engagement

### HelpResponse

**Champs :**
- `response_type` : offer_help, need_help, contact, question
- `message` : Contenu de la réponse
- `is_accepted`, `is_rejected` : Statut de la réponse

## API Endpoints

### Demandes d'aide

```
GET    /help-requests/api/requests/           # Liste des demandes
POST   /help-requests/api/requests/           # Créer une demande
GET    /help-requests/api/requests/{id}/      # Détail d'une demande
PUT    /help-requests/api/requests/{id}/      # Modifier une demande
DELETE /help-requests/api/requests/{id}/      # Supprimer une demande

# Actions spéciales
POST   /help-requests/api/requests/{id}/respond/           # Répondre
POST   /help-requests/api/requests/{id}/accept-response/   # Accepter réponse
POST   /help-requests/api/requests/{id}/reject-response/   # Rejeter réponse
POST   /help-requests/api/requests/{id}/mark-completed/    # Marquer terminée
POST   /help-requests/api/requests/{id}/mark-cancelled/    # Marquer annulée

# Données spéciales
GET    /help-requests/api/requests/map_data/  # Données pour carte
GET    /help-requests/api/requests/stats/     # Statistiques
```

### Réponses

```
GET    /help-requests/api/responses/          # Liste des réponses
POST   /help-requests/api/responses/          # Créer une réponse
GET    /help-requests/api/responses/{id}/     # Détail d'une réponse
PUT    /help-requests/api/responses/{id}/     # Modifier une réponse
DELETE /help-requests/api/responses/{id}/     # Supprimer une réponse

# Actions spéciales
POST   /help-requests/api/responses/{id}/accept/   # Accepter
POST   /help-requests/api/responses/{id}/reject/   # Rejeter
```

### Catégories

```
GET    /help-requests/api/categories/         # Liste des catégories
GET    /help-requests/api/categories/{id}/    # Détail d'une catégorie
```

## Filtres disponibles

### Demandes d'aide
- `request_type` : Type de demande (request/offer)
- `need_type` : Type de besoin
- `status` : Statut de la demande
- `duration_type` : Type de durée
- `proximity_zone` : Zone de proximité
- `is_urgent` : Demande urgente
- `city`, `neighborhood` : Localisation
- `radius`, `latitude`, `longitude` : Filtrage géographique
- `date_from`, `date_to` : Période
- `search` : Recherche textuelle

### Réponses
- `response_type` : Type de réponse
- `is_accepted`, `is_rejected` : Statut
- `help_request` : ID de la demande
- `author` : ID de l'auteur

## Types de besoins

1. **Matériel** (📦) : Prêt ou don de matériel
2. **Présence/Accompagnement** (👥) : Accompagnement ou présence
3. **Service** (🛠️) : Prestation de service
4. **Transport** (🚗) : Transport ou livraison
5. **Courses** (🛒) : Courses ou achats
6. **Aide technique** (🔧) : Assistance technique
7. **Aide éducative** (📚) : Soutien scolaire ou formation
8. **Autre** (🤝) : Autre type d'aide

## Durées estimées

1. **Immédiat** (⚡) : Besoin urgent
2. **Cette semaine** (📅) : Dans les 7 jours
3. **Ce mois** (🗓️) : Dans le mois
4. **Avant une date** (📆) : Date spécifique
5. **En continu** (🔄) : Besoin régulier

## Zones de proximité

1. **Quartier** (🏠) : Zone locale
2. **Ville** (🏙️) : Zone urbaine
3. **Région** (🌍) : Zone étendue

## Signaux automatiques

L'application envoie automatiquement des notifications par email pour :

- **Création de demande** : Confirmation à l'auteur
- **Nouvelle réponse** : Notification à l'auteur de la demande
- **Statut de réponse** : Notification à l'auteur de la réponse
- **Changement de statut** : Notification aux répondants

## Nettoyage automatique

Une fonction `cleanup_expired_requests()` est disponible pour :

- Identifier les demandes expirées
- Les marquer comme 'expired'
- Maintenir la base de données propre

## Permissions

- **Lecture** : Tous les utilisateurs (authentifiés ou non)
- **Création** : Utilisateurs authentifiés
- **Modification/Suppression** : Auteur de la demande/réponse
- **Réponse** : Utilisateurs authentifiés (sauf à sa propre demande)

## Intégration frontend

### Composants React

1. **HelpMap.js** : Vue principale avec carte et liste
2. **HelpRequestForm.js** : Formulaire de création
3. **HelpRequestDetail.js** : Détail d'une demande

### Fonctionnalités

- **Carte interactive** avec marqueurs personnalisés
- **Filtres avancés** par type, durée, zone
- **Formulaire structuré** avec validation
- **Interface responsive** adaptée mobile/desktop
- **Géolocalisation** automatique utilisateur

## Configuration

### Settings Django

```python
# Activer les notifications email (optionnel)
SEND_HELP_REQUEST_NOTIFICATIONS = True
SEND_HELP_RESPONSE_NOTIFICATIONS = True
SEND_HELP_RESPONSE_STATUS_NOTIFICATIONS = True
SEND_HELP_REQUEST_STATUS_NOTIFICATIONS = True
```

### URLs

Ajouter dans `urls.py` principal :

```python
urlpatterns = [
    # ...
    path('help-requests/', include('help_requests.urls')),
]
```

## Tests

L'application inclut des tests complets pour :

- **Modèles** : Validation, propriétés, méthodes
- **Intégration** : Flux complet demande → réponse → acceptation
- **Filtrage** : Tous les types de filtres
- **Permissions** : Accès et restrictions

## Déploiement

1. **Migrations** : `python manage.py migrate`
2. **Collecte statiques** : `python manage.py collectstatic`
3. **Superuser** : `python manage.py createsuperuser`
4. **Tests** : `python manage.py test help_requests`

## Maintenance

- **Nettoyage** : Tâche cron pour `cleanup_expired_requests()`
- **Monitoring** : Surveiller les métriques (vues, réponses)
- **Backup** : Sauvegarde régulière des données
- **Performance** : Index sur les champs de filtrage 