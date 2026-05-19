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
from datetime import timedelta
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db import transaction
from articulos.models import Articulos
from django.db.models import Case, Value, When
from django.core.paginator import Paginator
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
    """Genera múltiples cuotas de interés según el tipo de contrato."""
    monto = empeno.monto_prestado
    interes_mensual = round(monto * empeno.tasa_interes / 100, 2)
    
    # 1. Definimos la duración según el tipo de contrato del contrato vinculado
    # Accedemos a través de empeno.id_contrato que creaste en la vista 'crear_empeno'
    tipo = empeno.id_contrato.tipo_contrato
    
    mapa_meses = {
        'Normal': 3,             # 3 Meses
        'Plazo Maximo': 4,       # 4 Meses
        'Contrato sobre Oro': 1, # 1 Mes (ajusta según tu necesidad)
    }
    
    # Obtenemos el número de meses, por defecto 3 si hay algún error
    cantidad_cuotas = mapa_meses.get(tipo, 3)
    
    # 2. Bucle para crear cada cuota mensual
    for i in range(1, cantidad_cuotas + 1):
        # Calculamos la fecha programada sumando i meses a la fecha de inicio
        # Si el empeño inició hoy, la cuota 1 vence en 1 mes, la 2 en 2 meses...
        fecha_cuota = empeno.fecha_inicio + relativedelta(months=i)
        
        Cuota.objects.create(
            id_empeno=empeno,
            id_cliente=empeno.id_cliente, # Agregado para integridad
            numero_cuota=i,
            fecha_programada=fecha_cuota,
            capital=Decimal('0.00'),
            interes=interes_mensual,
            mora=Decimal('0.00'),
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

    empenos_por_pagina = 10
    paginator = Paginator(empenos, empenos_por_pagina)
    
    # 2. Capturamos qué página está viendo el usuario desde la URL (ej: ?page=2)
    numero_pagina = request.GET.get('page')
    
    # 3. Extraemos los registros que corresponden únicamente a esa página
    page_obj = paginator.get_page(numero_pagina)
    
    # 🚨 IMPORTANTE: Al HTML ahora le pasamos 'page_obj' en lugar de 'empenos'
    return render(request, 'empenos/listar.html', {'empenos': page_obj, 'form': form})


# Asegúrate de importar tus modelos, formularios y funciones auxiliares (_generar_cuota, etc.)

@transaction.atomic
def crear_empeno(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    if request.method == 'POST':
        data = request.POST.copy()
        
        # 1. Capturamos el artículo seleccionado y el monto desde el POST
        articulo_id = data.get('id_articulo')
        valor_str = data.get('monto_prestado', '0')
        
        # Convertimos el string del monto a Decimal de forma segura
        try:
            valor_prestado = Decimal(valor_str)
        except (ValueError, TypeError, InvalidOperation):
            valor_prestado = Decimal('0')

        # 2. Lógica de automatización de tipo de contrato e interés automático
        if articulo_id and not data.get('tipo_contrato'):
            try:
                # Buscamos el artículo en la base de datos para conocer su precio y categoría
                articulo_obj = Articulos.objects.get(pk=articulo_id)
                precio_sugerido = articulo_obj.precio_sugerido_venta
                categoria_art = articulo_obj.categoria.strip().lower()
                
                # Calculamos los topes dinámicos basados en el 40% y 60%
                tope_40_porc = precio_sugerido * Decimal('0.40')
                tope_60_porc = precio_sugerido * Decimal('0.60')
                
                # Evaluamos las condiciones según las reglas de negocio de Diamante Azul
                if valor_prestado <= tope_40_porc and categoria_art != 'oro':
                    data['tipo_contrato'] = 'Normal'
                elif valor_prestado <= tope_60_porc and categoria_art != 'oro':
                    data['tipo_contrato'] = 'Plazo Maximo'
                elif valor_prestado <= tope_40_porc and categoria_art == 'oro':
                    data['tipo_contrato'] = 'Contrato sobre Oro'
                elif valor_prestado <= tope_60_porc and categoria_art == 'oro':
                    data['tipo_contrato'] = 'Oro Maximo'  # Fuerza interés automático al 60%
                    
            except Articulos.DoesNotExist:
                pass # Si el artículo no existe, el formulario se encargará de gestionarlo

        # Pasamos los datos (ya modificados con el contrato automático) al formulario
        form = EmpenoForm(data)
        
        if form.is_valid():
            # 3. Creamos el objeto en memoria (Aún no se guarda en la base de datos)
            empeno = form.save(commit=False)
            
            # Guardamos el tipo de contrato calculado dentro del objeto empeño antes de guardar
            tipo_elegido = data.get('tipo_contrato', 'Normal')
            empeno.tipo_contrato = tipo_elegido
            
            articulo = empeno.id_articulo

            # 4. VALIDACIÓN DEL TOPE MÁXIMO PERMITIDO (60% del valor sugerido)
            tope_maximo = articulo.precio_sugerido_venta * Decimal('0.60')

            if empeno.monto_prestado > tope_maximo:
                messages.error(
                    request, 
                    f"Error: El préstamo (${empeno.monto_prestado:,.0f}) supera el 60% del valor comercial permitido (${tope_maximo:,.0f})."
                )
                return render(request, 'empenos/crear.html', {'form': form})
            
            # 5. PRIMER Y ÚNICO GUARDADO INICIAL: El empeño ya sabe que tipo de contrato es
            empeno.save() 

            # 6. CREACIÓN DEL CONTRATO ÚNICO ASOCIADO
            nuevo_contrato = Contrato.objects.create(
                id_empeno=empeno,
                id_cliente=empeno.id_cliente,
                id_articulo=empeno.id_articulo,
                fecha_contrato=timezone.now().date(),
                tipo_contrato=tipo_elegido,
                estado_contrato='Disponible'
            )

            # 7. VINCULACIÓN FINAL DEL CONTRATO AL EMPEÑO
            empeno.id_contrato = nuevo_contrato
            empeno.save()
            
            # 8. PROCESOS AUTOMÁTICOS SECUNDARIOS
            _sincronizar_articulo(empeno)  # Cambia estado del artículo a 'Empeñado'
            _generar_cuota(empeno)        # Genera las cuotas leyendo correctamente el nuevo contrato
            
            messages.success(request, f'Empeño #{empeno.id_empeno} registrado con contrato {tipo_elegido}.')
            return redirect('empenos:detalle', empeno.pk)
        
        else:
            # Imprime en la consola del servidor los errores exactos si la validación falla
            print("======= ERRORES FORMULARIO =======", form.errors)
            messages.error(request, 'Por favor corrige los errores del formulario.')
            
    else:
        # Configuración del formulario limpio para peticiones GET
        fecha_vencimiento = timezone.now() + timedelta(days=31)
        form = EmpenoForm(initial={
            'fecha_vencimiento': fecha_vencimiento.date()
        })

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
    verificar_vencidos() # Ejecuta tu rutina normal de revisión

    usuario_rol_id = request.session.get('usuario_rol_id')
    usuario_id = request.session.get('usuario_id')

    form = FiltroCuota(request.GET)
    
    # 🎯 MEJORA: select_related optimizado para traer el artículo y cliente sin matar la BD
    cuotas = Cuota.objects.select_related('id_empeno__id_articulo', 'id_cliente')

    # Filtro para Clientes (Rol 3)
    if usuario_rol_id == 3:
        try:
            from clientes.models import Cliente
            cliente = Cliente.objects.get(id_usuario=usuario_id)
            cuotas = cuotas.filter(id_cliente=cliente)
        except Exception:
            cuotas = cuotas.none()

    # Aplicación de filtros del formulario
    if form.is_valid():
        estado = form.cleaned_data.get('estado')
        q = form.cleaned_data.get('q')
        
        if estado:
            cuotas = cuotas.filter(estado=estado)
        
        if q:
            if q.isdigit():
                cuotas = cuotas.filter(id_empeno__id_empeno=q)
            else:
                cuotas = cuotas.filter(id_cliente__nombre__icontains=q)

    # 🎯 PRIORIZACIÓN INTELIGENTE DE ESTADOS:
    # 1 = Pendiente (Arriba), 2 = Vencida, 3 = Pagada (Abajo)
    cuotas = cuotas.annotate(
        prioridad=Case(
            When(estado='Pendiente', then=Value(1)),
            When(estado='Vencida', then=Value(2)),
            default=Value(3)
        )
    ).order_by('prioridad', 'fecha_programada') # Ordena por prioridad y luego por fecha más vieja

    # 🥞 PAGINACIÓN DE 10 EN 10
    paginator = Paginator(cuotas, 10)
    numero_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_pagina)

    # 🚨 CORRECCIÓN: El return render queda afuera de todos los condicionales, al ras de la función
    return render(request, 'cuotas/listar.html', {
        'cuotas': page_obj, # Enviamos el objeto paginado con el mismo nombre 'cuotas'
        'form': form,
        'total_pendientes': Cuota.objects.filter(estado='Pendiente').count(),
        'total_pagadas': Cuota.objects.filter(estado='Pagada').count(),
        'total_vencidas': Cuota.objects.filter(estado='Vencida').count(),
    })
    
    
def pagar_multiples(request, id_empeno):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        if request.session.get('usuario_rol_id') != 3:
            return redirect('usuarios:login')

    if request.method == 'POST':
        empeno = get_object_or_404(Empeno, pk=id_empeno)
        cuotas_ids = request.POST.getlist('cuotas_seleccionadas')
        cantidad_extra = int(request.POST.get('cantidad_extra', 0))
        
        # 1. Procesar cuotas existentes
        cuotas_seleccionadas = Cuota.objects.filter(id_empeno=empeno, id_cuota__in=cuotas_ids)
        
        # Obtenemos el valor del interés de la primera cuota para las cuotas extra
        primera_cuota = Cuota.objects.filter(id_empeno=empeno).first()
        valor_interes_fijo = primera_cuota.interes if primera_cuota else Decimal('0.00')

        for cuota in cuotas_seleccionadas:
            if cuota.estado != 'Pagada':
                # Sumamos capital, interes y mora para el total del pago
                total_pago = cuota.capital + cuota.interes + cuota.mora
                
                Pago.objects.create(
                    id_cuota=cuota,
                    id_cliente=empeno.id_cliente,
                    monto=total_pago,
                    metodo_pago='Efectivo',
                )
                cuota.estado = 'Pagada'
                cuota.save()

        # 2. Procesar cuotas excedentes (Extra)
        if cantidad_extra > 0:
            for _ in range(cantidad_extra):
                ultima = Cuota.objects.filter(id_empeno=empeno).order_by('-numero_cuota').first()
                nuevo_num = (ultima.numero_cuota + 1) if ultima else 1
                
                # Calculamos la fecha programada (30 días después de la última)
                fecha_base = ultima.fecha_programada if ultima else timezone.now().date()
                nueva_fecha = fecha_base + timedelta(days=30)
                
                nueva_cuota = Cuota.objects.create(
                    id_empeno=empeno,
                    id_cliente=empeno.id_cliente,
                    numero_cuota=nuevo_num,
                    fecha_programada=nueva_fecha,
                    capital=Decimal('0.00'),
                    interes=valor_interes_fijo,
                    mora=Decimal('0.00'),
                    estado='Pagada'
                )
                
                Pago.objects.create(
                    id_cuota=nueva_cuota,
                    id_cliente=empeno.id_cliente,
                    monto=valor_interes_fijo,
                    metodo_pago='Efectivo',
                )

        empeno.estado = 'Activo'
        empeno.save()
        _sincronizar_articulo(empeno)

        messages.success(request, f"Pagos registrados exitosamente.")

    return redirect('cuotas:listar')

def agregar_cuota_manual(request, id_empeno):
    empeno = get_object_or_404(Empeno, pk=id_empeno)
    ultima_cuota = Cuota.objects.filter(id_empeno=empeno).order_by('-numero_cuota').first()
    nuevo_numero = (ultima_cuota.numero_cuota + 1) if ultima_cuota else 1

    Cuota.objects.create(
        id_empeno=empeno,
        numero_cuota=nuevo_numero,
        valor_cuota=empeno.tasa_interes,
        fecha_vencimiento=timezone.now() + timedelta(days=30),
        estado='Pendiente'
    ) # CORRECCIÓN: Falta cerrar paréntesis
    
    return redirect('cuotas:listar')

def ver_cuotas(request, id_empeno):
    # ... tus validaciones de usuario ...
    empeno = get_object_or_404(Empeno, pk=id_empeno)
    cuotas = Cuota.objects.filter(id_empeno=empeno).order_by('numero_cuota')

    # VARIABLE CRUCIAL:
    # Verifica si existe alguna cuota que no esté pagada.
    tiene_pendientes = cuotas.filter(estado='Pendiente').exists()

    return render(request, 'cuotas/detalle.html', {
        'empeno': empeno,
        'cuotas': cuotas,
        'tiene_cuotas_pendientes': tiene_pendientes, # Se envía al HTML
    })
def retirar_empeno(request, empeno_id):
    empeno = get_object_or_404(Empeno, pk=empeno_id)
    
    if request.method == 'POST':
        # Seguridad final: no dejar retirar si hay deuda (aunque el botón se viera verde)
        if Cuota.objects.filter(id_empeno=empeno, estado='Pendiente').exists(): 
            messages.error(request, "Error: Hay deudas pendientes.")
            return redirect('empenos:cuotas', id_empeno=empeno.id_empeno)

        # Actualizamos estados
        empeno.estado = 'Retirado'
        empeno.save()
        
        articulo = empeno.id_articulo
        articulo.estado = 'Retirado'
        articulo.save()
        
        messages.success(request, f"¡Éxito! {articulo.nombre} retirado de bodega.")
        return redirect('empenos:listar')

    return redirect('empenos:cuotas', id_empeno=empeno.id_empeno)