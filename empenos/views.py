from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Empeno, Cuota, Pago
from .forms import EmpenoForm, PagoForm, FiltroEmpeno, AbonoForm
from usuarios.views import _requiere_admin, _requiere_empleado
from django.http import JsonResponse
from django.db.models import Sum
from contratos.models import Contrato
from django.db.models import Q, Sum
from cuotas.forms import FiltroCuota

# ── Helpers ──────────────────────────────────────────────────────────────────

def _sincronizar_articulo(empeno):
    """Sincroniza el estado del artículo según el estado del empeño."""
    articulo = empeno.id_articulo
    mapa_estados = {
        'Activo':   'Empeñado',
        'Retirado': 'En venta',
        'Vencido':  'Vencido',
        'En venta': 'En venta',
        'Vendido':  'Vendido',
    }
    articulo.estado = mapa_estados.get(empeno.estado, articulo.estado)
    articulo.precio_sugerido_venta = empeno.monto_prestado + (
        empeno.monto_prestado * empeno.tasa_interes / 100
    )
    articulo.save()


def _generar_cuota(empeno):
    """Crea automáticamente la cuota única de solo interés."""
    monto = empeno.monto_prestado
    interes = round(monto * empeno.tasa_interes / 100, 2)

    Cuota.objects.create(
        id_empeno=empeno,
        numero_cuota=1,
        fecha_programada=empeno.fecha_vencimiento,
        capital=0,  # <--- Cambiado de 'monto' a 0
        interes=interes,
        mora=0,
        estado='Pendiente',
    )


def verificar_vencidos():
    """
    Revisa todos los empeños Activos cuya fecha de vencimiento ya pasó.
    Marca la cuota como Vencida, el empeño como Vencido y el artículo como Vencido.
    """
    hoy = timezone.now().date()
    vencidos = Empeno.objects.filter(
        estado='Activo',
        fecha_vencimiento__lt=hoy
    ).select_related('id_articulo')

    for empeno in vencidos:
        # Marcar cuotas pendientes como vencidas
        Cuota.objects.filter(
            id_empeno=empeno, estado='Pendiente'
        ).update(estado='Vencida')

        # Marcar empeño
        empeno.estado = 'Vencido'
        empeno.save(update_fields=['estado'])

        # Marcar artículo
        articulo = empeno.id_articulo
        articulo.estado = 'Vencido'
        articulo.save(update_fields=['estado'])


# ── Vistas CRUD ───────────────────────────────────────────────────────────────

def listar_empenos(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        usuario_rol_id = request.session.get('usuario_rol_id')
        if usuario_rol_id != 3:
            return redirect('usuarios:login')

    verificar_vencidos()

    usuario_rol_id = request.session.get('usuario_rol_id')
    usuario_id     = request.session.get('usuario_id')

    empenos = Empeno.objects.select_related('id_cliente', 'id_articulo').order_by('-fecha_inicio')

    if usuario_rol_id == 3:
        try:
            from clientes.models import Cliente
            cliente = Cliente.objects.get(id_usuario=usuario_id)
            empenos = empenos.filter(id_cliente=cliente)
        except Exception:
            empenos = empenos.none()

    form = FiltroEmpeno(request.GET)
    if form.is_valid():
        q      = form.cleaned_data.get('q')
        estado = form.cleaned_data.get('estado')
        if q and usuario_rol_id != 3:
            empenos = empenos.filter(id_cliente__nombre__icontains=q)
        if estado:
            empenos = empenos.filter(estado=estado)

    # Anotar cada empeño con su cuota pendiente (si existe)
    empenos_list = list(empenos)
    cuotas_pendientes = {}
    if empenos_list:
        ids = [e.id_empeno for e in empenos_list]
        cuotas = Cuota.objects.filter(
            id_empeno__in=ids,
            estado='Pendiente'
        ).order_by('fecha_programada')
        for c in cuotas:
            if c.id_empeno_id not in cuotas_pendientes:
                cuotas_pendientes[c.id_empeno_id] = c

    for empeno in empenos_list:
        empeno.cuota_pendiente = cuotas_pendientes.get(empeno.id_empeno)

    return render(request, 'empenos/listar.html', {
        'empenos': empenos_list,
        'form': form
    })


def crear_empeno(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    if request.method == 'POST':
        form = EmpenoForm(request.POST)
        if form.is_valid():
            empeno = form.save()
            tipo_elegido = form.cleaned_data.get('tipo_contrato', 'Normal   ')
            nuevo_contrato = Contrato.objects.create(
                id_empeno=empeno,
                id_cliente=empeno.id_cliente,
                id_articulo=empeno.id_articulo,
                fecha_contrato=timezone.now().date(),
                tipo_contrato=tipo_elegido,
                estado_contrato='Disponible'
            )
            empeno.id_contrato = nuevo_contrato
            empeno.save()
            _sincronizar_articulo(empeno)
            _generar_cuota(empeno)          # ← genera cuota automáticamente
            messages.success(request, f'Empeño #{empeno.id_empeno} registrado. Cuota generada automáticamente.')
            return redirect('empenos:detalle', empeno.id_empeno)
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = EmpenoForm()

    return render(request, 'empenos/crear.html', {'form': form})


def eliminar_empeno(request, id_empeno):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    empeno = get_object_or_404(Empeno, pk=id_empeno)
    if request.method == 'POST':
        empeno.delete()
        messages.success(request, 'Empeño eliminado correctamente.')
        return redirect('empenos:listar')

    return render(request, 'empenos/eliminar.html', {'empeno': empeno})


def detalle_empeno(request, id_empeno):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        usuario_rol_id = request.session.get('usuario_rol_id')
        if usuario_rol_id != 3:
            return redirect('usuarios:login')

    verificar_vencidos()
    empeno = get_object_or_404(Empeno, pk=id_empeno)
    cuotas = Cuota.objects.filter(id_empeno=empeno).order_by('numero_cuota')
    pagos  = Pago.objects.filter(id_cuota__id_empeno=empeno).order_by('fecha_pago')

    return render(request, 'empenos/detalle.html', {
        'empeno': empeno,
        'cuotas': cuotas,
        'pagos':  pagos,
    })


def ver_cuotas(request, id_empeno):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        usuario_rol_id = request.session.get('usuario_rol_id')
        if usuario_rol_id != 3:
            return redirect('usuarios:login')

    verificar_vencidos()
    empeno = get_object_or_404(Empeno, pk=id_empeno)
    cuotas = Cuota.objects.filter(id_empeno=empeno).order_by('numero_cuota')

    return render(request, 'cuotas/detalle.html', {'empeno': empeno, 'cuotas': cuotas})


def registrar_pago(request, id_cuota):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        usuario_rol_id = request.session.get('usuario_rol_id')
        if usuario_rol_id != 3:
            return redirect('usuarios:login')

    cuota = get_object_or_404(Cuota, pk=id_cuota)

    if cuota.estado == 'Pagada':
        messages.info(request, 'Esta cuota ya fue pagada.')
        return redirect('cuotas:listar')

    if request.method == 'POST':
        from decimal import Decimal
        Pago.objects.create(
            id_cuota   = cuota,
            id_cliente = cuota.id_empeno.id_cliente,
            monto      = cuota.capital + cuota.interes,
            metodo_pago = 'Efectivo',
        )
        cuota.estado = 'Pagada'
        cuota.save()

        empeno = cuota.id_empeno
        empeno.estado = 'Activo'
        empeno.save()
        _sincronizar_articulo(empeno)

        messages.success(request, f'Pago registrado. Empeño #{empeno.id_empeno} finalizado.')
        return redirect('cuotas:listar')

    return redirect('cuotas:listar')


def api_reporte_empenos(request):
    # 1. Seguridad: Solo permitimos a los Admin (rol_id 1)
    #if not request.session.get('rol_id') == 1:
    #   return JsonResponse({'error': 'No autorizado'}, status=403)

    # 2. Consulta: Sumamos montos agrupando por el nombre del tipo de contrato
    # Nota: Si tu campo en el modelo Empeno se llama 'contrato', cámbialo aquí
    query = Empeno.objects.values('id_contrato__tipo_contrato').annotate(
        total=Sum('monto_prestado')
    ).order_by('-total')

    labels = []
    for item in query:
        # Si el valor es None (null), le ponemos un nombre por defecto
        nombre = item['id_contrato__tipo_contrato']
        labels.append(nombre if nombre else "Contrato No Definido")

    data = {
        'labels': labels,
        'values': [float(item['total']) for item in query],
    }
    
    return JsonResponse(data)

def pagina_reportes(request):
    # 1. Seguridad: Solo Admin o Empleado
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    # 2. Capturar los filtros desde la URL (Método GET)
    f_inicio = request.GET.get('fecha_inicio')
    f_fin    = request.GET.get('fecha_fin')
    tipo_c   = request.GET.get('tipo_contrato')
    cliente  = request.GET.get('cliente_nombre')

    # 3. Construir la consulta dinámica
    filtros = Q()

    if f_inicio and f_fin:
        filtros &= Q(fecha_contrato__range=[f_inicio, f_fin])
    
    if tipo_c:
        filtros &= Q(tipo_contrato=tipo_c)
        
    if cliente:
        filtros &= (Q(id_cliente__nombre__icontains=cliente) | 
                    Q(id_cliente__apellido__icontains=cliente))

    # 4. Obtener los datos agrupados para la gráfica
    # Usamos el modelo Contrato porque ya tiene el 'tipo_contrato' y está vinculado al Empeño
    datos_query = Contrato.objects.filter(filtros).values('tipo_contrato').annotate(
        total_monto=Sum('id_empeno__monto_prestado')
    ).order_by('-total_monto')

    # 5. Formatear datos para Chart.js (Listas de Python)
    labels = [item['tipo_contrato'] for item in datos_query]
    valores = [float(item['total_monto'] or 0) for item in datos_query]

    # 6. Contexto para el HTML
    context = {
        'labels': labels,
        'valores': valores,
        'filtros_previos': request.GET, # Mantiene lo que el usuario escribió
        'tipos_contrato': Contrato.TIPO_CHOICES, # Para llenar el select
    }

    return render(request, 'empenos/reportes.html', context)

def editar_empeno(request, id_empeno):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    empeno = get_object_or_404(Empeno, pk=id_empeno)
    if request.method == 'POST':
        form = EmpenoForm(request.POST, instance=empeno)
        if form.is_valid():
            empeno = form.save()
            _sincronizar_articulo(empeno)
            messages.success(request, 'Empeño actualizado correctamente.')
            return redirect('empenos:detalle', empeno.id_empeno)
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = EmpenoForm(instance=empeno)

    return render(request, 'empenos/editar.html', {'form': form, 'empeno': empeno})


def registrar_abono(request, id_empeno):
    # Validaciones de seguridad (tus funciones de rol)
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        if request.session.get('usuario_rol_id') != 3:
            return redirect('usuarios:login')

    empeno = get_object_or_404(Empeno, pk=id_empeno)

    if request.method == 'POST':
        form = AbonoForm(request.POST, saldo_actual=empeno.monto_prestado)
        if form.is_valid():
            monto_abonado = form.cleaned_data['abonoCap']
            tipo_elegido = form.cleaned_data['tipo_contrato']

            # Ejecutar la resta y guardar
            empeno.monto_prestado -= monto_abonado

            # Crear el nuevo contrato asociado
            nuevo_contrato = Contrato.objects.create(
                id_empeno=empeno,
                id_cliente=empeno.id_cliente,
                id_articulo=empeno.id_articulo,
                fecha_contrato=timezone.now().date(),
                tipo_contrato=tipo_elegido,
                estado_contrato='Disponible'
            )

            # Actualizar el empeño con el nuevo contrato y guardar todo
            empeno.id_contrato = nuevo_contrato
            empeno.save()

            # Tus funciones automáticas
            _sincronizar_articulo(empeno)
            _generar_cuota(empeno)

            messages.success(request, f'Abono de ${monto_abonado} procesado correctamente.')
            return redirect('empenos:detalle', id_empeno=empeno.id_empeno)
    else:
        form = AbonoForm(saldo_actual=empeno.monto_prestado)

    return render(request, 'empenos/abono_empeno.html', {
        'form': form,
        'empeno': empeno
    })
    
    
#CUOTAS
def listar_cuotas(request):
    
    verificar_vencidos()

    usuario_rol_id = request.session.get('usuario_rol_id')
    usuario_id     = request.session.get('usuario_id')

    form   = FiltroCuota(request.GET)
    cuotas = Cuota.objects.select_related(
        'id_empeno', 'id_empeno__id_cliente', 'id_empeno__id_articulo'
    ).order_by('estado', 'fecha_programada')


    if usuario_rol_id == 3:
        try:
            from clientes.models import Cliente
            cliente = Cliente.objects.get(id_usuario=usuario_id)
            cuotas = cuotas.filter(id_cliente=cliente)
        except Exception:
            cuotas = cuotas.none()


    if form.is_valid():
        estado = form.cleaned_data.get('estado')
        q      = form.cleaned_data.get('q')
        if estado:
            cuotas = cuotas.filter(estado=estado)
        if q:
            cuotas = cuotas.filter(id_empeno__id_cliente__nombre__icontains=q)

    return render(request, 'cuotas/listar.html', {
        'cuotas':           cuotas,
        'form':             form,
        'total_pendientes': Cuota.objects.filter(estado='Pendiente').count(),
        'total_pagadas':    Cuota.objects.filter(estado='Pagada').count(),
        'total_vencidas':   Cuota.objects.filter(estado='Vencida').count(),
    })
    