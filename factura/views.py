from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from .models import Factura, DetalleFactura
from .forms import FacturaForm, FiltroFactura
from django.core.paginator import Paginator
from usuarios.views import _requiere_admin, _requiere_empleado


# ==========================================================================
# 🌟 MOTOR HELPER: GENERACIÓN AUTOMÁTICA DE COMPROBANTES DE CAJA
# ==========================================================================
def generar_factura_automatica(usuario, cliente, tipo_movimiento, monto,
                                id_empeno=None, articulo=None, descripcion=""):
    """
    Registra de forma automatizada cualquier flujo de dinero de Diamante Azul
    en la tabla de auditoría de facturas (Desembolsos, Cuotas, Abonos, Retiros).
    """
    factura = Factura.objects.create(
        id_cliente=cliente,
        id_usuario=usuario,
        total_neto=Decimal(str(monto)),
        monto_pagado=Decimal(str(monto)),
        metodo_pago='Efectivo',
        tipo_movimiento=tipo_movimiento,
        id_empeno_asociado=id_empeno
    )

    DetalleFactura.objects.create(
        id_factura=factura,
        id_articulo=articulo,
        descripcion_servicio=descripcion if not articulo else f"Artículo: {articulo.nombre}",
        precio_venta=Decimal(str(monto))
    )

    return factura


# ==========================================================================
# 📊 VISTAS PRINCIPALES DEL MÓDULO DE FACTURACIÓN
# ==========================================================================

def listar_facturas(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    form = FiltroFactura(request.GET)
    # 💡 Agregamos 'id_usuario__id_rol' en select_related para traer el rol eficientemente
    facturas = Factura.objects.select_related('id_cliente', 'id_usuario__id_rol').order_by('-fecha_venta')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        fecha = form.cleaned_data.get('fecha')  # Campo fecha que añades al formulario
        rol = form.cleaned_data.get('rol')      # Campo rol que añades al formulario

        # 1. Tu filtro actual de Texto / ID (q)
        if q:
            filtro = Q(id_cliente__nombre__icontains=q) | Q(tipo_movimiento__icontains=q)
            try:
                filtro |= Q(id_factura=int(q))
            except ValueError:
                pass
            facturas = facturas.filter(filtro)

        # 2. 🔥 NUEVO: Filtro por Fecha de Creación/Venta
        if fecha:
            # .date asegura buscar solo por el día sin importar la hora exacta en el DateTimeField
            facturas = facturas.filter(fecha_venta__date=fecha)

        # 3. 🔥 NUEVO: Filtro por Rol del Usuario creador de la factura
        if rol:
            facturas = facturas.filter(id_usuario__id_rol__id_rol=rol)

    # Paginación (Se mantiene intacta)
    paginator = Paginator(facturas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'factura/listar.html', {'facturas': page_obj, 'form': form})


def crear_factura(request):
    """Maneja la venta directa tradicional de artículos en vitrina."""
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            articulos_ids = request.POST.getlist('articulo[]')
            precios = request.POST.getlist('precio[]')

            if not articulos_ids:
                messages.error(request, 'Debes agregar al menos un artículo a la factura.')
                return render(request, 'factura/crear.html', {'form': form})

            factura = form.save(commit=False)
            factura.tipo_movimiento = 'Venta'
            factura.save()

            total = Decimal('0.00')
            from articulos.models import Articulos  # Import local para evitar importación cíclica

            for art_id, precio_v in zip(articulos_ids, precios):
                if art_id and precio_v:
                    articulo = get_object_or_404(Articulos, pk=art_id)
                    precio_dec = Decimal(precio_v)
                    DetalleFactura.objects.create(
                        id_factura=factura,
                        id_articulo=articulo,
                        descripcion_servicio=f"Venta Directa: {articulo.nombre}",
                        precio_venta=precio_dec
                    )
                    total += precio_dec

            factura.total_neto = total
            factura.save()

            messages.success(request, f'Factura de Venta #{factura.id_factura} generada con éxito.')
            return redirect('factura:listar')
    else:
        form = FacturaForm()

    return render(request, 'factura/crear.html', {'form': form})


def detalle_factura(request, id_factura):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    factura = get_object_or_404(Factura, pk=id_factura)
    detalles = DetalleFactura.objects.filter(id_factura=factura).select_related('id_articulo')

    return render(request, 'factura/detalle.html', {
        'factura': factura,
        'detalles': detalles
    })