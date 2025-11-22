from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        # Importar signals para que se registren cuando la app arranque
        try:
            import core.signals  # noqa: F401
        except Exception:
            pass
