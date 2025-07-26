from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre aux propriétaires de modifier leurs demandes d'aide
    """
    
    def has_object_permission(self, request, view, obj):
        # Les permissions de lecture sont autorisées pour toute requête
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Les permissions d'écriture sont autorisées uniquement au propriétaire
        return obj.author == request.user


class CanRespondToHelpRequest(permissions.BasePermission):
    """
    Permission pour répondre aux demandes d'aide
    """
    
    def has_permission(self, request, view):
        # Vérifier que l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return False
        
        # Empêcher de répondre à sa propre demande
        if view.action == 'respond':
            help_request_id = view.kwargs.get('pk')
            if help_request_id:
                try:
                    help_request = view.get_queryset().get(id=help_request_id)
                    if help_request.author == request.user:
                        return False
                except:
                    pass
        
        return True


class CanManageHelpResponse(permissions.BasePermission):
    """
    Permission pour gérer les réponses aux demandes d'aide
    """
    
    def has_object_permission(self, request, view, obj):
        # L'auteur de la réponse peut accepter/rejeter sa propre réponse
        if obj.author == request.user:
            return True
        
        # L'auteur de la demande d'aide peut accepter/rejeter les réponses
        if obj.help_request.author == request.user:
            return True
        
        return False 