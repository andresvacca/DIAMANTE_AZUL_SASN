from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Contrato
from .forms import ContratoForm
from .pdf import generar_pdf_contrato
from empenos.models import Empeno
from usuarios.models import Rol


def listar_contratos(request):
    rol_id     = request.session.get('usuario_rol_id')
    usuario_id = request.session.get('usuario_id')

    qs = Contrato.objects.select_related(
        'id_cliente', 'id_articulo', 'id_empeno'
    ).order_by('-fecha_contrato')

    if rol_id in (Rol.ROL_ADMINISTRADOR, Rol.ROL_EMPLEADO):
        contratos = qs
        q      = request.GET.get('q', '').strip()
        estado = request.GET.get('estado', '').strip()
        if q:
            contratos = contratos.filter(id_cliente__nombre__icontains=q)
        if estado:
            contratos = contratos.filter(estado_contrato=estado)
    else:
        contratos = qs.filter(id_cliente__id_usuario=usuario_id)

    return render(request, 'contratos/listar.html', {
        'contratos': contratos,
        'q':         request.GET.get('q', ''),
        'estado':    request.GET.get('estado', ''),
        'estados':   Contrato.ESTADO_CHOICES,
    })

def crear_contrato(request):
    if request.method == 'POST':
        empeno_id   = request.POST.get('id_empeno')
        cliente_id  = request.POST.get('id_cliente')
        articulo_id = request.POST.get('id_articulo')

        if not empeno_id or not cliente_id or not articulo_id:
            messages.error(request, 'Debes seleccionar un cliente y un empeño.')
            form = ContratoForm(request.POST)
            return render(request, 'contratos/crear.html', {'form': form})

        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.id_cliente_id  = cliente_id
            contrato.id_articulo_id = articulo_id
            contrato.id_empeno_id   = empeno_id
            contrato.save()
            buffer = generar_pdf_contrato(contrato)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="contrato_{contrato.id_contrato}.pdf"'
            return response
        messages.error(request, f'Errores: {form.errors}')
    else:
        form = ContratoForm()
    return render(request, 'contratos/crear.html', {'form': form})



def detalle_contrato(request, id_contrato):
    contrato = get_object_or_404(
        Contrato.objects.select_related(
            'id_cliente', 'id_articulo', 'id_empeno', 'id_cuota', 'id_pago', 'id_factura'
        ),
        pk=id_contrato
    )
    return render(request, 'contratos/detalle.html', {'contrato': contrato})


def descargar_pdf_contrato(request, id_contrato):  # ✅ nombre consistente con urls.py
    contrato = get_object_or_404(
        Contrato.objects.select_related(
            'id_cliente', 'id_articulo', 'id_empeno'
        ),
        pk=id_contrato
    )
    buffer = generar_pdf_contrato(contrato)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{contrato.id_contrato}.pdf"'
    return response


def editar_contrato(request, id_contrato):
    contrato = get_object_or_404(Contrato, pk=id_contrato)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato actualizado correctamente.')
            return redirect('contratos:listar')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ContratoForm(instance=contrato)
    return render(request, 'contratos/editar.html', {'form': form, 'contrato': contrato})


def eliminar_contrato(request, id_contrato):
    contrato = get_object_or_404(Contrato, pk=id_contrato)
    if request.method == 'POST':
        contrato.delete()
        messages.success(request, 'Contrato eliminado correctamente.')
        return redirect('contratos:listar')
    return render(request, 'contratos/eliminar.html', {'contrato': contrato})


def get_empeno_detalles(request, pk):
    try:
        empeno = Empeno.objects.select_related('id_cliente', 'id_articulo').get(pk=pk)
        data = {
            'id_cliente': empeno.id_cliente.id_cliente,
            'id_articulo': empeno.id_articulo.id_articulo,
            'descripcion_producto': empeno.id_articulo.descripcion,
            'valor_empenado': float(empeno.valor_empenado),
            'valor_retiro': float(empeno.valor_rescatable),
            'cliente_full': f"{empeno.id_cliente.nombre} {empeno.id_cliente.apellido}"
        }
        return JsonResponse(data)
    except Empeno.DoesNotExist:
        return JsonResponse({'error': 'Empeño no encontrado en Diamante Azul'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def datos_empeno_api(request, id_empeno):
    try:
        empeno = Empeno.objects.select_related(
            'id_cliente', 'id_articulo'
        ).get(pk=id_empeno)
        data = {
            'cliente_id':           empeno.id_cliente.id_cliente,
            'cliente_nombre':       empeno.id_cliente.nombre,
            'articulo_id':          empeno.id_articulo.id_articulo,
            'articulo_nombre':      empeno.id_articulo.nombre,
            'articulo_descripcion': empeno.id_articulo.descripcion or '',
            'monto_prestado':       str(empeno.monto_prestado),
            'precio_retiro':        str(empeno.id_articulo.precio_sugerido_venta),
        }
    except Empeno.DoesNotExist:
        data = {}
    return JsonResponse(data)

def buscar_clientes_api(request):
    from django.http import JsonResponse
    from clientes.models import Cliente
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse([], safe=False)
    clientes = Cliente.objects.filter(nombre__icontains=q)[:10]
    data = [{'id': c.id_cliente, 'nombre': c.nombre, 'documento': c.documento_id} for c in clientes]
    return JsonResponse(data, safe=False)


def empenos_sin_contrato_api(request, id_cliente):
    from django.http import JsonResponse
    from empenos.models import Empeno
    from .models import Contrato
    # IDs de empeños que ya tienen contrato
    empenos_con_contrato = Contrato.objects.filter(
        id_empeno__isnull=False
    ).values_list('id_empeno_id', flat=True)

    empenos = Empeno.objects.filter(
        id_cliente=id_cliente,
        estado='Activo'
    ).exclude(
        id_empeno__in=empenos_con_contrato
    ).select_related('id_articulo')

    data = [{
        'id':               e.id_empeno,
        'articulo_nombre':  e.id_articulo.nombre,
        'articulo_id':      e.id_articulo.id_articulo,
        'articulo_desc':    e.id_articulo.descripcion or '',
        'monto_prestado':   str(e.monto_prestado),
        'precio_retiro':    str(e.id_articulo.precio_sugerido_venta),
    } for e in empenos]
    return JsonResponse(data, safe=False)


