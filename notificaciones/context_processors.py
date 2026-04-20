def notificaciones_context(request):
    """Inyecta el conteo de notificaciones no leídas en todos los templates."""
    count = 0
    if request.session.get('usuario_id'):
        try:
            from notificaciones.models import Notificacion
            usuario_id = request.session.get('usuario_id')
            count = Notificacion.objects.filter(
                usuario_id__in=[None, usuario_id],
                leida=False
            ).count()
        except Exception:
            pass
    return {'notif_count': count}