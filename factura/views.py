from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from .models import Factura, DetalleFactura
from .forms import FacturaForm, DetalleFacturaForm, FiltroFactura
from django.core.paginator import Paginator
from usuarios.views import _requiere_admin, _requiere_empleado

# ==========================================================================
# 🌟 MOTOR HELPER: GENERACIÓN AUTOMÁTICA DE COMPROBANTES DE CAJA
# ==========================================================================
def generar_factura_automatica(usuario, cliente, tipo_movimiento, monto, id_empeno=None, articulo=None, descripcion=""):
    """
    Registra de forma automatizada cualquier flujo de dinero de Diamante Azul
    en la tabla de auditoría de facturas (Desembolsos, Cuotas, Abonos, Retiros).
    """
    # 1. Creamos la cabecera del movimiento
    factura = Factura.objects.create(
        id_cliente=cliente,
        id_usuario=usuario,
        total_neto=Decimal(str(monto)),
        monto_pagado=Decimal(str(monto)),
        metodo_pago='Efectivo',  # Por defecto caja general maneja efectivo, se puede cambiar
        tipo_movimiento=tipo_movimiento,
        id_empeno_asociado=id_empeno
    )
    
    # 2. Creamos el detalle descriptivo del servicio o bien
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
    facturas = Factura.objects.select_related('id_cliente', 'id_usuario').order_by('-fecha_venta')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            filtro = Q(id_cliente__nombre__icontains=q) | Q(tipo_movimiento__icontains=q)
            try:
                filtro |= Q(id_factura=int(q))
            except ValueError:
                pass
            facturas = facturas.filter(filtro)

    # 🌟 CONTROL DE PAGINACIÓN AUTOMÁTICA
    facturas_por_pagina = 10
    paginator = Paginator(facturas, facturas_por_pagina)
    
    numero_pagina = request.GET.get('page')
    page_obj = paginator.get_page(numero_pagina)

    # Enviamos 'page_obj' mapeado bajo la clave 'facturas' para que no tengas que renombrar variables en tu bucle HTML
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

            # Guardamos la cabecera como 'Venta Directa'
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


def editar_factura(request, id_factura):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    factura = get_object_or_404(Factura, pk=id_factura)
    detalles = DetalleFactura.objects.filter(id_factura=factura)

    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            messages.success(request, 'Factura actualizada correctamente.')
            return redirect('factura:detalle', factura.id_factura)
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FacturaForm(instance=factura)

    return render(request, 'factura/editar.html', {
        'form': form, 'factura': factura, 'detalles': detalles
    })


def eliminar_detalle(request, id_detalle):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    detalle = get_object_or_404(DetalleFactura, pk=id_detalle)
    factura = detalle.id_factura
    factura_id = factura.id_factura

    if request.method == 'POST':
        detalle.delete()
        total = sum(d.precio_venta for d in DetalleFactura.objects.filter(id_factura=factura))
        factura.total_neto = total
        factura.save()
        messages.success(request, 'Artículo eliminado de la factura.')

    return redirect('factura:editar', factura_id)


def eliminar_factura(request, id_factura):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    factura = get_object_or_404(Factura, pk=id_factura)
    if request.method == 'POST':
        factura.delete()
        messages.success(request, 'Factura eliminada correctamente de los registros.')
    
    return redirect('factura:listar')