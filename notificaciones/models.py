from django.db import models


class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('info',    'Información'),
        ('success', 'Éxito'),
        ('warning', 'Advertencia'),
        ('error',   'Error'),
    ]

    titulo    = models.CharField(max_length=200)
    mensaje   = models.TextField()
    tipo      = models.CharField(max_length=10, choices=TIPO_CHOICES, default='info')
    leida     = models.BooleanField(default=False)
    fecha     = models.DateTimeField(auto_now_add=True)
    url       = models.CharField(max_length=300, null=True, blank=True)
    usuario_id = models.IntegerField(null=True, blank=True)  # None = global (todos la ven)

    class Meta:
        db_table = 'notificaciones'
        ordering = ['-fecha']

    def __str__(self):
        return self.titulo


def crear_notificacion(titulo, mensaje, tipo='info', url=None, usuario_id=None):
    """Helper para crear notificaciones desde cualquier parte del proyecto."""
    Notificacion.objects.create(
        titulo=titulo,
        mensaje=mensaje,
        tipo=tipo,
        url=url,
        usuario_id=usuario_id,
    )