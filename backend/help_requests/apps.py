from django.apps import AppConfig


class HelpRequestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'help_requests'
    verbose_name = 'Demandes d\'aide communautaire'
    
    def ready(self):
        """Configuration lors du démarrage de l'application"""
        try:
            import help_requests.signals  # noqa
        except ImportError:
            pass 