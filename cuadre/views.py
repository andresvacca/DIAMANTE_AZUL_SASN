import datetime
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from django.utils.timezone import make_aware

# Importaciones de modelos (es mejor tenerlas arriba si es posible)
from empenos.models import Pago, Empeno
from factura.models import Factura

def cuadre_caja(request):
    # Verificación de permisos
    from usuarios.views import _requiere_admin, _requiere_empleado
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    # 1. Obtener fechas del GET o usar hoy por defecto
    hoy = timezone.now().date()
    fecha_inicio_str = request.GET.get('fecha_inicio', str(hoy))
    fecha_fin_str    = request.GET.get('fecha_fin',    str(hoy))

    try:
        fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        fecha_fin_obj    = datetime.datetime.strptime(fecha_fin_str,    '%Y-%m-%d').date()
    except ValueError:
        fecha_inicio_obj = fecha_fin_obj = hoy

    # 2. Convertir fechas a Datetime "Aware" (con zona horaria)
    # Esto asegura que capturemos desde las 00:00:00 del inicio hasta las 23:59:59 del fin
    d_inicio = make_aware(datetime.datetime.combine(fecha_inicio_obj, datetime.time.min))
    d_final  = make_aware(datetime.datetime.combine(fecha_fin_obj, datetime.time.max))

    # 3. Consultas usando __range para evitar errores de zona horaria
    
    # Pagos recibidos (Entradas)
    pagos = Pago.objects.filter(fecha_pago__range=(d_inicio, d_final))
    total_pagos = pagos.aggregate(t=Sum('monto'))['t'] or 0
    cantidad_pagos = pagos.count()

    # Préstamos entregados (Salidas)
    empenos_rango = Empeno.objects.filter(fecha_inicio__range=(d_inicio, d_final))
    total_prestamos = empenos_rango.aggregate(t=Sum('monto_prestado'))['t'] or 0
    cantidad_empenos = empenos_rango.count()

    # Facturas / Ventas de artículos (Entradas)
    facturas_rango = Factura.objects.filter(fecha_venta__range=(d_inicio, d_final))
    total_facturas = facturas_rango.aggregate(t=Sum('total_neto'))['t'] or 0
    cantidad_facturas = facturas_rango.count()

    # 4. Cálculos de Balance
    # Convertimos a float para asegurar que la operación matemática sea correcta
    entradas = float(total_pagos) + float(total_facturas)
    salidas  = float(total_prestamos)
    balance  = entradas - salidas

    # 5. Detalle para la tabla inferior
    detalle_pagos = pagos.select_related('id_cliente', 'id_cuota__id_empeno').order_by('-fecha_pago')[:50]

    # 6. Renderizado
    return render(request, 'cuadre/index.html', {
        # Enviamos las fechas formateadas para que los <input type="date"> las reconozcan
        'fecha_inicio':     fecha_inicio_obj.strftime('%Y-%m-%d'),
        'fecha_fin':        fecha_fin_obj.strftime('%Y-%m-%d'),
        
        'total_pagos':      total_pagos,
        'cantidad_pagos':   cantidad_pagos,
        'total_prestamos':  total_prestamos,
        'cantidad_empenos': cantidad_empenos,
        'total_facturas':   total_facturas,
        'cantidad_facturas':cantidad_facturas,
        
        'entradas':         entradas,
        'salidas':          salidas,
        'balance':          balance,
        'detalle_pagos':    detalle_pagos,
    })