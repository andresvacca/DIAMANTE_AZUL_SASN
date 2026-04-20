from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm, FiltroCliente
from usuarios.views import _requiere_admin, _requiere_empleado
from django.db.models import Q
from usuarios.models import Rol
import json
from django.http import JsonResponse
import requests
from django.http import JsonResponse
from django.db.models import ProtectedError

def listar_clientes(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')
    form = FiltroCliente(request.GET)
    clientes = Cliente.objects.all().order_by('nombre')
    if form.is_valid():
        query = form.cleaned_data.get('q')
        if query:
            clientes = clientes.filter(
                Q(nombre__icontains=query) | Q(documento_id__icontains=query)
            )
    return render(request, 'clientes/listar.html', {'clientes': clientes, 'form': form})


def crear_cliente(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado correctamente.')
            return redirect('clientes:listar')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear.html', {'form': form})


def editar_cliente(request, id_cliente):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clientes:listar')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar.html', {'form': form, 'cliente': cliente})


def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    if request.method == 'POST':
        try:
            usuario = cliente.id_usuario
            cliente.delete()
            if usuario:
                usuario.delete()
            messages.success(request, 'Cliente eliminado correctamente.')
            return redirect('clientes:listar')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar este cliente porque tiene empeños o pagos registrados.')
            return redirect('clientes:listar')
    return render(request, 'clientes/eliminar.html', {'cliente': cliente})

def crear_cliente_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = ClienteForm(data)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({'ok': True, 'id': cliente.id_cliente, 'nombre': cliente.nombre})
        else:
            errores = {campo: e[0] for campo, e in form.errors.items()}
            return JsonResponse({'ok': False, 'error': errores})
    return JsonResponse({'ok': False, 'error': 'Método no permitido.'})

#SEGUNADA LLAMADA DE APIS
def municipios_por_departamentos(request):
    dep = request.GET.get('departamento', '')
    url = f'https://www.datos.gov.co/resource/gdxc-w37w.json?nom_dep={dep}&$limit=200'
    resp = request.get(url, timeout=5)
    data = resp.json()
    municipios = sorted([m['nom_mpio'] for m in data if 'nom_mpio' in m])
    return JsonResponse(municipios, safe=False)

#LLAMADA DE APIS
def municipios_api(request):
    import requests as req
    from django.http import JsonResponse
    dep = request.GET.get('dep', '').strip()
    if not dep:
        return JsonResponse([], safe=False)
    try:
        deps = req.get('https://api-colombia.com/api/v1/Department', timeout=6).json()
        dep_obj = next((d for d in deps if d['name'].upper() == dep.upper()), None)
        if not dep_obj:
            return JsonResponse([], safe=False)
        ciudades = req.get(
            f"https://api-colombia.com/api/v1/Department/{dep_obj['id']}/cities",
            timeout=6
        ).json()
        municipios = sorted(c['name'] for c in ciudades)
    except Exception:
        municipios = []
    return JsonResponse(municipios, safe=False)