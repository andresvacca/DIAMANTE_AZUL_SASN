from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import crear_notificacion


# ── Empeños ──────────────────────────────────────────────────────────────────
from empenos.models import Empeno, Cuota

@receiver(post_save, sender=Empeno)
def notif_empeno(sender, instance, created, **kwargs):
    if created:
        crear_notificacion(
            titulo=f'Empeño #{instance.id_empeno} creado',
            mensaje=f'Cliente: {instance.id_cliente}. Monto: ${instance.monto_prestado}.',
            tipo='success',
            url=f'/empenos/detalle/{instance.id_empeno}/',
        )
    elif instance.estado == 'Vencido':
        crear_notificacion(
            titulo=f'Empeño #{instance.id_empeno} vencido',
            mensaje=f'El empeño de {instance.id_cliente} ha vencido.',
            tipo='warning',
            url=f'/empenos/detalle/{instance.id_empeno}/',
        )

@receiver(post_save, sender=Cuota)
def notif_cuota(sender, instance, created, **kwargs):
    if not created and instance.estado == 'Pagada':
        crear_notificacion(
            titulo=f'Cuota pagada — Empeño #{instance.id_empeno_id}',
            mensaje=f'Cuota #{instance.numero_cuota} pagada. Capital: ${instance.capital} + Interés: ${instance.interes}.',
            tipo='success',
            url=f'/empenos/detalle/{instance.id_empeno_id}/',
        )
    elif not created and instance.estado == 'Vencida':
        crear_notificacion(
            titulo=f'Cuota vencida — Empeño #{instance.id_empeno_id}',
            mensaje=f'La cuota #{instance.numero_cuota} ha vencido sin pago.',
            tipo='error',
            url=f'/cuotas/',
        )


# ── Clientes ──────────────────────────────────────────────────────────────────
from clientes.models import Cliente

@receiver(post_save, sender=Cliente)
def notif_cliente(sender, instance, created, **kwargs):
    if created:
        crear_notificacion(
            titulo='Nuevo cliente registrado',
            mensaje=f'{instance.nombre} (Doc: {instance.documento_id}) fue registrado.',
            tipo='info',
            url='/clientes/',
        )

@receiver(post_delete, sender=Cliente)
def notif_cliente_eliminado(sender, instance, **kwargs):
    crear_notificacion(
        titulo='Cliente eliminado',
        mensaje=f'{instance.nombre} fue eliminado del sistema.',
        tipo='warning',
    )


# ── Contratos ─────────────────────────────────────────────────────────────────
from contratos.models import Contrato

@receiver(post_save, sender=Contrato)
def notif_contrato(sender, instance, created, **kwargs):
    if created:
        crear_notificacion(
            titulo=f'Contrato #{instance.id_contrato} creado',
            mensaje=f'Tipo: {instance.tipo_contrato}. Cliente: {instance.id_cliente}.',
            tipo='success',
            url=f'/contratos/detalle/{instance.id_contrato}/',
        )


# ── Facturas ──────────────────────────────────────────────────────────────────
from factura.models import Factura

@receiver(post_save, sender=Factura)
def notif_factura(sender, instance, created, **kwargs):
    if created:
        crear_notificacion(
            titulo=f'Factura #{instance.id_factura} generada',
            mensaje=f'Cliente: {instance.id_cliente}. Total: ${instance.total_neto}.',
            tipo='info',
            url=f'/factura/detalle/{instance.id_factura}/',
        )