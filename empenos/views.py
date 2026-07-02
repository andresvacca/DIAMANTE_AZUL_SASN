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
from .forms import EmpenoForm, PagoForm, FiltroEmpeno, AbonoForm, EditarEmpenoForm
from factura.views import generar_factura_automatica
from factura.models import Factura
from factura.forms import DetalleFactura
from django.urls import reverse
from usuarios.models import Usuario
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
    # 1. Creamos los filtros base para texto (Cliente y Artículo)
                filtros = Q(id_cliente__nombre__icontains=q) | Q(id_articulo__nombre__icontains=q)
                
                # 2. Si el usuario escribió un número válido, también buscamos coincidencia en el monto prestado
                # Quitamos los puntos o comas por si escriben "12.000" o "12,000"
                q_limpio = q.replace('.', '').replace(',', '')
                
                if q_limpio.isdigit():
                    # Usamos __exact o __gte/__lte según prefieras, __exact es ideal para buscar el monto exacto
                    filtros |= Q(monto_prestado=int(q_limpio))
                
                # 3. Aplicamos todo el bloque de filtros agrupado
                empenos = empenos.filter(filtros)
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
    # 🚨 BLOQUEO ABSOLUTO: Si no es Admin ni Empleado, o si es un Cliente (Rol 3), se le niega el acceso
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        messages.error(request, 'No tienes permisos para realizar cobros en el sistema.')
        return redirect('cuotas:listar')

    cuota = get_object_or_404(Cuota, pk=id_cuota)

    if cuota.estado == 'Pagada':
        messages.info(request, 'Esta cuota ya fue pagada.')
        return redirect('cuotas:listar')

    if request.method == 'POST':
        from decimal import Decimal  # Mantenemos la importación aquí o la subes al inicio del archivo
        
        # 🔥 BLINDAJE: Convertimos explícitamente a Decimal para evitar el TypeError en la suma
        capital_dec = Decimal(str(cuota.capital))
        interes_dec = Decimal(str(cuota.interes))
        monto_total_pago = capital_dec + interes_dec

        # Registramos el objeto Pago de tu app de empeños
        pago_objeto = Pago.objects.create(
            id_cuota   = cuota,
            id_cliente = cuota.id_empeno.id_cliente,
            monto      = monto_total_pago, # Usamos la variable blindada
            metodo_pago = 'Efectivo',
        )
        
        # ⚠️ Nota: Asegúrate de aplicar el cambio de Decimal('0.05') en empenos/models.py (línea 123) 
        # para que esta siguiente línea guarde sin estallar:
        cuota.estado = 'Pagada'
        cuota.save()

        empeno = cuota.id_empeno
        empeno.estado = 'Activo'
        empeno.save()
        _sincronizar_articulo(empeno)

        # Extracción segura del usuario logueado manualmente
        from factura.views import generar_factura_automatica
        from usuarios.models import Usuario
        
        usuario_id_sesion = request.session.get('usuario_id') or request.session.get('user_id')
        
        usuario_operador = None
        if usuario_id_sesion:
            try:
                usuario_operador = Usuario.objects.get(pk=usuario_id_sesion)
            except Usuario.DoesNotExist:
                pass
        
        if not usuario_operador and not request.user.is_anonymous:
            usuario_operador = request.user
        elif not usuario_operador:
            usuario_operador = Usuario.objects.first() 
        
        # Generación de la factura con el monto unificado y limpio
        generar_factura_automatica(
            usuario=usuario_operador, 
            cliente=empeno.id_cliente,
            tipo_movimiento='Cuota', 
            monto=monto_total_pago, # Usamos la variable blindada
            id_empeno=empeno.id_empeno,
            descripcion=f"Pago Interés/Cuota de Empeño #{empeno.id_empeno} - ID Cuota: {cuota.id_cuota}"
        )

        messages.success(request, f'Pago registrado y Comprobante de Caja generado. Empeño #{empeno.id_empeno} actualizado.')
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
    
    # REGLAS 2 y 3: Capturamos los valores originales e inmutables directamente de la Base de Datos
    monto_prestado_original = empeno.monto_prestado
    monto_entregado_original = empeno.monto_entregado
    articulo_original = empeno.id_articulo # Por si acaso se altera el POST

    if request.method == 'POST':
        form = EditarEmpenoForm(request.POST, instance=empeno)
        if form.is_valid():
            # Creamos el objeto en memoria sin impactar la DB todavía
            empeno_editado = form.save(commit=False)
            
            # 🚨 BLINDAJE INMUTABLE: Forzamos la sobreescritura de los datos protegidos
            empeno_editado.monto_prestado = monto_prestado_original
            empeno_editado.monto_entregado = monto_entregado_original
            empeno_editado.tasa_interes = Decimal('10.0') # REGLA 3: Siempre clavada en 10
            
            # REGLA 1: Si no se usó el botón de cambiar artículo, mantiene el original de forma segura
            if not empeno_editado.id_articulo:
                empeno_editado.id_articulo = articulo_original
            
            # Guardado físico en la base de datos
            empeno_editado.save()
            
            # Sincronizamos el estado del artículo asociado
            _sincronizar_articulo(empeno_editado)
            
            messages.success(request, f'Empeño #{empeno_editado.id_empeno} actualizado correctamente.')
            return redirect('empenos:detalle', empeno_editado.id_empeno)
        
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = EditarEmpenoForm(instance=empeno)

    return render(request, 'empenos/editar.html', {'form': form, 'empeno': empeno})


def registrar_abono(request, id_empeno):
    # Validaciones de seguridad (tus funciones de rol)
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        if request.session.get('usuario_role_id') != 3:
            return redirect('usuarios:login')

    empeno = get_object_or_404(Empeno, pk=id_empeno)

    if request.method == 'POST':
        form = AbonoForm(request.POST, saldo_actual=empeno.monto_prestado)
        if form.is_valid():
            monto_abonado = form.cleaned_data['abonoCap']
            tipo_elegido = form.cleaned_data['tipo_contrato']

            try:
                # Envolvemos todo en una transacción atómica para asegurar consistencia
                with transaction.atomic():
                    # 1. Reducir el saldo del empeño
                    empeno.monto_prestado -= monto_abonado

                    # 2. Crear el nuevo contrato asociado al abono
                    nuevo_contrato = Contrato.objects.create(
                        id_empeno=empeno,
                        id_cliente=empeno.id_cliente,
                        id_articulo=empeno.id_articulo,
                        fecha_contrato=timezone.now().date(),
                        tipo_contrato=tipo_elegido,
                        estado_contrato='Disponible'
                    )

                    # 3. Vincular el nuevo contrato al empeño y guardar cambios
                    empeno.id_contrato = nuevo_contrato
                    empeno.save()

                    # 🌟 4. CREAR LA FACTURA DE FORMA SILENCIOSA (SEGUNDO PLANO)
                    usuario_id = request.session.get('usuario_id')
                    usuario_operador = Usuario.objects.filter(pk=usuario_id).first() if usuario_id else Usuario.objects.first()

                    factura = Factura.objects.create(
                        id_cliente=empeno.id_cliente,
                        id_usuario=usuario_operador,
                        total_neto=monto_abonado,
                        monto_pagado=monto_abonado,
                        metodo_pago='Efectivo',
                        tipo_movimiento='Abono',
                        id_empeno_asociado=empeno.id_empeno
                    )

                    # 5. Registrar el desglose del artículo
                    DetalleFactura.objects.create(
                        id_factura=factura,
                        id_articulo=empeno.id_articulo,
                        descripcion_servicio=f"Abono parcial a capital — Contrato #{empeno.id_empeno}",
                        precio_venta=monto_abonado
                    )

                    # 6. Ejecutar tus rutinas automáticas originales
                    _sincronizar_articulo(empeno)
                    _generar_cuota(empeno)

                    # Notificación en pantalla indicando que todo se creó correctamente
                    messages.success(
                        request, 
                        f'Abono de ${monto_abonado} procesado con éxito. Se generó la Factura #{factura.id_factura}.'
                    )
                    
                    # 🚀 REDIRECCIÓN SEGURA A LA LISTA DE EMPEÑOS (Evita el 404 por completo)
                    # Cambia 'empenos:listar' por el nombre exacto de la ruta de tu lista general
                    return redirect(f"/factura/detalle/{factura.id_factura}/")

            except Exception as e:
                messages.error(request, f"Error interno al procesar el abono: {str(e)}")
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
    if request.method == 'POST':
        empeno = get_object_or_404(Empeno, pk=id_empeno)
        cuotas_ids = request.POST.getlist('cuotas_seleccionadas')
        
        # Como descartamos la factura, el "cantidad_extra" (excedente) se omite o se ignora 
        # ya que no genera cuotas físicas en la base de datos de inmediato.
        if not cuotas_ids:
            return JsonResponse({'success': False, 'error': 'No seleccionó ninguna cuota para pagar.'}, status=400)
            
        try:
            with transaction.atomic():
                # 1. Filtrar y traer solo las cuotas seleccionadas que pertenezcan a este empeño
                cuotas_a_pagar = Cuota.objects.filter(pk__in=cuotas_ids, id_empeno=empeno)
                
                # 2. Actualizar el estado de cada una
                for cuota in cuotas_a_pagar:
                    cuota.estado = 'Pagada'
                    cuota.fecha_pago = timezone.now()
                    cuota.save()
                
                # 3. Responder éxito puro al frontend
                return JsonResponse({'success': True})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

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
        # Seguridad final: no dejar retirar si hay deudas (aunque el botón se viera verde)
        if Cuota.objects.filter(id_empeno=empeno, estado='Pendiente').exists(): 
            messages.error(request, "Error: Hay deudas pendientes.")
            return redirect('empenos:cuotas', id_empeno=empeno.id_empeno)

        try:
            with transaction.atomic():
                # 1. Determinar el valor de liquidación (lo que quedaba en monto prestado)
                valor_liquidacion = Decimal(str(empeno.monto_prestado))

                # 2. Actualizamos estados del empeño y del artículo físico
                empeno.estado = 'Retirado'
                empeno.save()
                
                articulo = empeno.id_articulo
                articulo.estado = 'Retirado'
                articulo.save()
                
                # 3. Obtener el operador de la sesión de Diamante Azul de forma segura
                usuario_id = request.session.get('usuario_id')
                usuario_operador = Usuario.objects.filter(pk=usuario_id).first() if usuario_id else Usuario.objects.first()
                
                if not usuario_operador:
                    messages.error(request, "No se encontró un operador válido en el sistema para facturar.")
                    return redirect('empenos:cuotas', id_empeno=empeno.id_empeno)

                # 4. Crear la Factura de Liquidación ('Retiro')
                factura = Factura.objects.create(
                    id_cliente=empeno.id_cliente,
                    id_usuario=usuario_operador,
                    total_neto=valor_liquidacion,
                    monto_pagado=valor_liquidacion,
                    metodo_pago='Efectivo',
                    tipo_movimiento='Retiro',
                    id_empeno_asociado=empeno.id_empeno
                )
                
                # 5. Crear el Detalle desglosado vinculado al artículo
                # Nota: Usamos el campo correcto de tu modelo 'articulo.nombre_articulo' 
                # (o 'articulo.nombre' según como esté mapeado en tu base de datos)
                nombre_art = getattr(articulo, 'nombre_articulo', getattr(articulo, 'nombre', 'Artículo'))
                
                DetalleFactura.objects.create(
                    id_factura=factura,
                    id_articulo=articulo,
                    descripcion_servicio=f"Liquidación final y Retiro de: {nombre_art} (Contrato #{empeno.id_empeno})",
                    precio_venta=valor_liquidacion
                )
                
                messages.success(
                    request, 
                    f"¡Éxito! {nombre_art} retirado de bodega. Se generó la Factura #{factura.id_factura}."
                )
                
                # 🚀 REDIRECCIÓN EXACTA A TU URL (Singular, sin la 'f' interna rota)
                return redirect(f"/factura/detalle/{factura.id_factura}/")

        except Exception as e:
            messages.error(request, f"Error crítico al procesar el retiro y la factura: {str(e)}")
            return redirect('empenos:cuotas', id_empeno=empeno.id_empeno)

    return redirect('empenos:cuotas', id_empeno=empeno.id_empeno)