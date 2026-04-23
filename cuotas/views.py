from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.shortcuts import render
from empenos.models import Cuota, Empeno
from empenos.views import verificar_vencidos
from usuarios.views import _requiere_admin, _requiere_empleado
from .forms import FiltroCuota

from usuarios.views import _requiere_admin, _requiere_empleado

"""def listar_cuotas(request):
    
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
    
def detalle_cuota(request, id_cuota, id_empeno):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        usuario_rol_id = request.session.get('usuario_rol_id')
        if usuario_rol_id != 3:
            return redirect('usuarios:login')

    verificar_vencidos()
    empeno = get_object_or_404(Empeno, pk=id_empeno)
    cuotas = Cuota.objects.filter(id_empeno=empeno).order_by('numero_cuota')

    return render(request, 'empenos/cuotas.html', {'empeno': empeno, 'cuotas': cuotas})"""