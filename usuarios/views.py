from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario, Rol
from contratos.models import Contrato
from .forms import UsuarioForm, RegistroForm, LoginForm, FiltroUsuarios



# ─── Gestión CRUD de usuarios (panel admin) ───────────────────────────────────

def listar_usuarios(request):
    if not _requiere_admin(request) or _requiere_empleado(request):
        return redirect('usuarios:login')
    
    form = FiltroUsuarios(request.GET)
    usuarios = Usuario.objects.select_related('id_rol').order_by('nombre')
    
    if form.is_valid():
        query = form.cleaned_data.get('q')
        if query:
            usuarios = usuarios.filter(nombre__icontains=query)
    
    return render(request, 'usuarios/listar.html', {
        'usuarios': usuarios,
        'form': form
    })


def crear_usuario(request):
    if not _requiere_admin(request):
        return redirect('usuarios:login')
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('usuarios:listar')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear.html', {'form': form})


def editar_usuario(request, id_usuario):
    if not _requiere_admin(request):
        return redirect('usuarios:login')
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios:listar')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar.html', {'form': form, 'usuario': usuario})


def eliminar_usuario(request, id_usuario):
    if not _requiere_admin(request):
        return redirect('usuarios:login')
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('usuarios:listar')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

def listar_contratos(request):
    rol_id = request.session.get('usuario_rol_id')
    usuario_id = request.session.get('usuario_id')

    if rol_id in (Rol.ROL_ADMINISTRADOR, Rol.ROL_EMPLEADO):
        # Admin y empleado ven todos
        contratos = Contrato.objects.select_related(
            'id_cliente', 'id_articulo', 'id_empeno'
        ).order_by('-fecha_contrato')
    else:
        # Cliente solo ve los suyos
        contratos = Contrato.objects.select_related(
            'id_cliente', 'id_articulo', 'id_empeno'
        ).filter(id_cliente=usuario_id).order_by('-fecha_contrato')

    return render(request, 'contratos/listar.html', {'contratos': contratos})


# ─── Autenticación ────────────────────────────────────────────────────────────

def login_view(request):
    if request.session.get('usuario_id'):
        return redirect(_dashboard_por_rol(request))

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            usuario = Usuario.objects.select_related('id_rol').get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'home/auth/login.html', {'form': form})

        if check_password(password, usuario.password_hash):
            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_nombre'] = usuario.nombre
            request.session['usuario_rol'] = usuario.id_rol.nombre if usuario.id_rol else ''
            request.session['usuario_rol_id'] = usuario.id_rol_id
            messages.success(request, f'Bienvenido/a, {usuario.nombre}!')
            return redirect(_dashboard_por_rol(request))
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'home/auth/login.html', {'form': form})


def registro_view(request):
    if request.session.get('usuario_id'):
        return redirect(_dashboard_por_rol(request))

    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        request.session['usuario_id'] = usuario.id_usuario
        request.session['usuario_nombre'] = usuario.nombre
        request.session['usuario_rol'] = usuario.id_rol.nombre if usuario.id_rol else ''
        request.session['usuario_rol_id'] = usuario.id_rol_id
        messages.success(request, f'¡Registro exitoso! Bienvenido/a, {usuario.nombre}.')
        return redirect('home')

    return render(request, 'home/auth/register.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('home')


def dashboard_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('usuarios:login')
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    return render(request, 'home/auth/dashboard.html', {'usuario': usuario})


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _requiere_admin(request):
    return request.session.get('usuario_rol_id') == Rol.ROL_ADMINISTRADOR

def _requiere_empleado(request):
    return request.session.get('usuario_rol_id') == Rol.ROL_EMPLEADO


def _dashboard_por_rol(request):
    rol_id = request.session.get('usuario_rol_id')
    if rol_id == Rol.ROL_ADMINISTRADOR:
        return 'usuarios:dashboard'
    elif rol_id == Rol.ROL_EMPLEADO:
        return 'usuarios:dashboard'
    else:
        return 'home'

def perfil_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('usuarios:login')

    usuario = get_object_or_404(Usuario.objects.select_related('id_rol'), pk=usuario_id)

    cliente = None
    empenos = []

    if usuario.id_rol_id == Rol.ROL_CLIENTE:
        try:
            from clientes.models import Cliente
            cliente = Cliente.objects.get(id_usuario=usuario)
            from empenos.models import Empeno
            empenos = Empeno.objects.filter(
                id_cliente=cliente
            ).select_related('id_articulo').order_by('-fecha_inicio')
        except Exception:
            pass

    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario,
        'cliente': cliente,
        'empenos': empenos,
    })

def perfil_detalle_view(request, id_usuario):
    """Vista para que admin/empleado vea el perfil completo de cualquier usuario."""
    from django.db.models import Sum, Count
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    usuario = get_object_or_404(Usuario.objects.select_related('id_rol'), pk=id_usuario)

    cliente  = None
    empenos  = []
    stats    = {}

    if usuario.id_rol_id == Rol.ROL_CLIENTE:
        try:
            from clientes.models import Cliente
            from empenos.models import Empeno, Cuota, Pago
            cliente = Cliente.objects.get(id_usuario=usuario)
            empenos = Empeno.objects.filter(
                id_cliente=cliente
            ).select_related('id_articulo').order_by('-fecha_inicio')

            # Estadísticas
            total_empenos    = empenos.count()
            empenos_activos  = empenos.filter(estado='Activo').count()
            empenos_vencidos = empenos.filter(estado='Vencido').count()
            empenos_vendidos = empenos.filter(estado='Vendido').count()
            monto_total      = empenos.aggregate(t=Sum('monto_prestado'))['t'] or 0
            cuotas_pagadas   = Cuota.objects.filter(
                id_empeno__id_cliente=cliente, estado='Pagada'
            ).count()
            cuotas_pendientes = Cuota.objects.filter(
                id_empeno__id_cliente=cliente, estado='Pendiente'
            ).count()
            total_pagado     = Pago.objects.filter(
                id_cliente=cliente
            ).aggregate(t=Sum('monto'))['t'] or 0

            stats = {
                'total_empenos':     total_empenos,
                'empenos_activos':   empenos_activos,
                'empenos_vencidos':  empenos_vencidos,
                'empenos_vendidos':  empenos_vendidos,
                'monto_total':       monto_total,
                'cuotas_pagadas':    cuotas_pagadas,
                'cuotas_pendientes': cuotas_pendientes,
                'total_pagado':      total_pagado,
            }
        except Exception:
            pass

    return render(request, 'usuarios/perfil_detalle.html', {
        'usuario': usuario,
        'cliente': cliente,
        'empenos': empenos,
        'stats':   stats,
    })