from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction, IntegrityError
from .models import Compra, VentaArticulo
from .forms import CompraForm, VentaForm
from factura.models import Factura, DetalleFactura
from usuarios.models import Rol, Usuario

# --- Funciones Auxiliares ---
def _es_admin_o_empleado(request):
    rol_id = request.session.get('usuario_rol_id')
    return rol_id in (Rol.ROL_ADMINISTRADOR, Rol.ROL_EMPLEADO)

# --- Vistas de Compra ---

def listar_compras(request):
    if not _es_admin_o_empleado(request):
        return redirect('usuarios:login')
    
    compras = Compra.objects.select_related(
        'id_cliente', 'id_articulo', 'id_factura_compra', 'id_factura_venta'
    ).order_by('-fecha_compra')
    return render(request, 'compras/listar.html', {'compras': compras})

@transaction.atomic
def crear_compra(request):
    if not _es_admin_o_empleado(request):
        return redirect('usuarios:login')
        
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            usuario_id = request.session.get('usuario_id')
            usuario = get_object_or_404(Usuario, pk=usuario_id)

            # 1. Crear factura de compra
            factura = Factura.objects.create(
                id_cliente=data['id_cliente'],
                id_usuario=usuario,
                total_neto=data['precio_pagado'],
                monto_pagado=data['precio_pagado'],
                metodo_pago=data['forma_pago'],
            )
            
            # 2. Detalle de la factura
            DetalleFactura.objects.create(
                id_factura=factura,
                id_articulo=data['id_articulo'],
                precio_venta=data['precio_pagado'],
            )
            
            # 3. Crear la compra vinculada
            Compra.objects.create(
                id_cliente=data['id_cliente'],
                id_articulo=data['id_articulo'],
                precio_pagado=data['precio_pagado'],
                precio_reventa=data['precio_reventa'],
                id_factura_compra=factura,
                estado='En Venta'
            )
            
            messages.success(request, 'Compra registrada y factura generada correctamente.')
            return redirect('compras:listar')
    else:
        form = CompraForm()
    return render(request, 'compras/crear.html', {'form': form})

# --- Vistas de Venta ---


def registrar_venta(request, id_compra):
    if not _es_admin_o_empleado(request):
        return redirect('usuarios:login')

    compra = get_object_or_404(Compra, pk=id_compra)
    
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            # EL TRY DEBE ENVOLVER AL TRANSACTION.ATOMIC
            try:
                with transaction.atomic():
                    usuario_id = request.session.get('usuario_id')
                    usuario = get_object_or_404(Usuario, pk=usuario_id)

                    # 1. Crear Factura
                    factura_venta = Factura.objects.create(
                        id_cliente=form.cleaned_data['id_cliente'],
                        id_usuario=usuario,
                        total_neto=form.cleaned_data['valor_total'],
                        monto_pagado=form.cleaned_data['valor_total'],
                        metodo_pago=form.cleaned_data['forma_pago']
                    )

                    # 2. Crear Detalle
                    DetalleFactura.objects.create(
                        id_factura=factura_venta,
                        id_articulo=compra.id_articulo,
                        precio_venta=form.cleaned_data['valor_total'],
                    )
                    
                    # 3. Crear VentaArticulo
                    VentaArticulo.objects.create(
                        id_compra=compra,
                        id_factura=factura_venta,
                        precio_venta_final=form.cleaned_data['valor_total']
                    )
                    
                    # 4. Actualizar Compra
                    compra.estado = 'Vendido'
                    compra.save()
                
                # SI LLEGAMOS AQUÍ, LA TRANSACCIÓN TERMINÓ BIEN
                messages.success(request, "Venta registrada exitosamente.")
                return redirect('compras:listar')

            except IntegrityError as e:
                # El error de "Duplicate Entry" cae aquí. 
                # Al estar fuera del 'with atomic', la transacción ya se revirtió
                # y la base de datos vuelve a estar "sana" para recibir consultas.
                messages.error(request, f"Error de base de datos: El artículo ya tiene una venta o factura asociada ({e})")
            except Exception as e:
                messages.error(request, f"Ocurrió un error: {e}")
    else:
        form = VentaForm(initial={'valor_total': compra.precio_reventa})

    return render(request, 'compras/venta.html', {'form': form, 'compra': compra})
# --- Otras Vistas ---

def detalle_compra(request, id_compra):
    if not _es_admin_o_empleado(request):
        return redirect('usuarios:login')
    compra = get_object_or_404(
        Compra.objects.select_related(
            'id_cliente', 'id_articulo', 'id_factura_compra', 'id_factura_venta'
        ),
        pk=id_compra
    )
    return render(request, 'compras/detalle.html', {'compra': compra})

def eliminar_compra(request, id_compra):
    if not _es_admin_o_empleado(request):
        return redirect('usuarios:login')
    compra = get_object_or_404(Compra, pk=id_compra)
    if request.method == 'POST':
        compra.delete()
        messages.success(request, 'Compra eliminada correctamente.')
        return redirect('compras:listar')
    return render(request, 'compras/eliminar.html', {'compra': compra})