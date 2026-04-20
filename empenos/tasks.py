from celery import shared_task
from django.utils import timezone
from .models import Empeno, Cuota


@shared_task
def generar_cuotas_mensuales():
    hoy = timezone.now().date()

    empenos_activos = Empeno.objects.filter(
        estado='Activo'
    ).select_related('id_articulo')

    for empeno in empenos_activos:
        # Verificar si ya existe una cuota este mes
        ya_existe = Cuota.objects.filter(
            id_empeno=empeno,
            fecha_programada__year=hoy.year,
            fecha_programada__month=hoy.month,
        ).exists()

        if ya_existe:
            continue

        # Obtener el tipo de contrato
        tipo = 'Normal'
        if empeno.id_contrato_id:
            from contratos.models import Contrato
            try:
                contrato = Contrato.objects.get(pk=empeno.id_contrato_id)
                tipo = contrato.tipo_contrato
            except Contrato.DoesNotExist:
                tipo = 'Normal'

        # Obtener el máximo de meses según tipo de contrato
        meses_max = {
            'Normal':               3,
            'Plazo Maximo':         1,
            'Contrato sobre Oro':   4,
            'Contrato Maximo Oro':  2,
        }.get(tipo, 3)

        # Contar cuotas sin pagar
        cuotas_sin_pagar = Cuota.objects.filter(
            id_empeno=empeno,
            estado__in=['Pendiente', 'Vencida']
        ).count()

        if cuotas_sin_pagar >= meses_max:
            # Vencer el empeño y el artículo
            Cuota.objects.filter(
                id_empeno=empeno, estado='Pendiente'
            ).update(estado='Vencida')
            empeno.estado = 'Vencido'
            empeno.save(update_fields=['estado'])
            articulo = empeno.id_articulo
            articulo.estado = 'Vencido'
            articulo.save(update_fields=['estado'])
        else:
            # Crear nueva cuota mensual
            capital = empeno.monto_prestado
            interes = round(capital * empeno.tasa_interes / 100, 2)
            numero  = Cuota.objects.filter(id_empeno=empeno).count() + 1
            Cuota.objects.create(
                id_empeno        = empeno,
                numero_cuota     = numero,
                fecha_programada = hoy,
                capital          = capital,
                interes          = interes,
                mora             = 0,
                estado           = 'Pendiente',
            )

    return f"Cuotas generadas: {hoy}"