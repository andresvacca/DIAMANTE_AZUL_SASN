from django.apps import AppConfig


class NotificacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notificaciones'

    """def ready(self):
        from . import signals
        signals.conectar_empenos()
        signals.conectar_clientes()
        signals.conectar_contratos()
        signals.conectar_facturas()"""
    
    def ready(self):
        import notificaciones.signals  # noqa