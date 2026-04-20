from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Factura, DetalleFactura
from .forms import FacturaForm, DetalleFacturaForm, FiltroFactura
from usuarios.views import _requiere_admin, _requiere_empleado


def listar_facturas(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    form = FiltroFactura(request.GET)
    facturas = Factura.objects.select_related('id_cliente', 'id_usuario').order_by('-fecha_venta')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            filtro = Q(id_cliente__nombre__icontains=q)
            try:
                filtro |= Q(id_factura=int(q))
            except ValueError:
                pass
            facturas = facturas.filter(filtro)

    return render(request, 'factura/listar.html', {'facturas': facturas, 'form': form})


def crear_factura(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            articulos_ids = request.POST.getlist('articulo[]')
            precios       = request.POST.getlist('precio[]')
            pares = [(a, p) for a, p in zip(articulos_ids, precios) if a and p]

            if not pares:
                messages.error(request, 'Debes agregar al menos un artículo a la factura.')
                return render(request, 'factura/crear.html', {'form': form})

            factura = form.save(commit=False)
            factura.total_neto = 0
            factura.save()

            total = 0
            for art_id, precio in pares:
                try:
                    d = DetalleFactura.objects.create(
                        id_factura=factura,
                        id_articulo_id=int(art_id),
                        precio_venta=float(precio),
                    )
                    total += d.precio_venta
                except Exception:
                    pass

            factura.total_neto = total
            factura.save()
            messages.success(request, f'Factura #{factura.id_factura} creada correctamente.')
            return redirect('factura:detalle', factura.id_factura)

        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FacturaForm()

    # Pre-seleccionar al usuario logueado como vendedor
    usuario_id = request.session.get('usuario_id')

    from articulos.models import Articulos
    articulos = Articulos.objects.all()
    return render(request, 'factura/crear.html', {
        'form': form,
        'articulos': articulos,
        'usuario_id': usuario_id,
    })


def detalle_factura(request, id_factura):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    factura  = get_object_or_404(
        Factura.objects.select_related('id_cliente', 'id_usuario'), pk=id_factura
    )
    detalles = DetalleFactura.objects.filter(id_factura=factura).select_related('id_articulo')
    return render(request, 'factura/detalle.html', {'factura': factura, 'detalles': detalles})


def editar_factura(request, id_factura):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    factura  = get_object_or_404(Factura, pk=id_factura)
    detalles = DetalleFactura.objects.filter(id_factura=factura).select_related('id_articulo')

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

    detalle    = get_object_or_404(DetalleFactura, pk=id_detalle)
    factura    = detalle.id_factura
    factura_id = factura.id_factura

    if request.method == 'POST':
        detalle.delete()
        total = sum(
            d.precio_venta for d in DetalleFactura.objects.filter(id_factura=factura)
        )
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
        messages.success(request, 'Factura eliminada correctamente.')
        return redirect('factura:listar')

    return render(request, 'factura/eliminar.html', {'factura': factura})