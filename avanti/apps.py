from django.apps import AppConfig


class AvantiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'avanti'

    def ready(self):
        import avanti.signals 