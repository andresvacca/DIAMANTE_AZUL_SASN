from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Notificacion
from usuarios.views import _requiere_admin, _requiere_empleado


def listar_notificaciones(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('usuarios:login')

    # Ver las globales y las del usuario logueado
    notificaciones = Notificacion.objects.filter(
        usuario_id__in=[None, usuario_id]
    ).order_by('-fecha')[:100]

    # Marcar todas como leídas al entrar
    Notificacion.objects.filter(
        usuario_id__in=[None, usuario_id],
        leida=False
    ).update(leida=True)

    return render(request, 'notificaciones/listar.html', {
        'notificaciones': notificaciones
    })


def marcar_leida(request, id_notificacion):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        Notificacion.objects.filter(
            pk=id_notificacion,
            usuario_id__in=[None, usuario_id]
        ).update(leida=True)
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})


def conteo_no_leidas(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return JsonResponse({'count': 0})
    count = Notificacion.objects.filter(
        usuario_id__in=[None, usuario_id],
        leida=False
    ).count()
    return JsonResponse({'count': count})