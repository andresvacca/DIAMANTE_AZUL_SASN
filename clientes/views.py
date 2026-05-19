from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm, FiltroCliente
from usuarios.views import _requiere_admin, _requiere_empleado
from django.db.models import Q, Count
from usuarios.models import Rol
import json
from django.http import JsonResponse
import requests
from django.http import JsonResponse
from django.db.models import ProtectedError
from empenos.models import Empeno

def listar_clientes(request):
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')
        
    form = FiltroCliente(request.GET)
    clientes = Cliente.objects.annotate(total_empenos=Count('empeno')).order_by('id_cliente')
    
    if form.is_valid():
        buscar_id = form.cleaned_data.get('buscar_id')
        query = form.cleaned_data.get('q')
        
        if buscar_id:
            clientes = clientes.filter(id_cliente=buscar_id)
        if query:
            query = query.strip()
            
            # Base del filtro multicriterio (Texto)
            filtros = Q(nombre__icontains=query) | \
                      Q(documento_id__icontains=query) | \
                      Q(telefono__icontains=query) | \
                      Q(direccion__icontains=query)
            
            # 🚀 INVESTIGAR POR ID: Si el empleado digita solo números, buscamos también por el ID exacto
            if query.isdigit():
                filtros |= Q(id_cliente=int(query))
                
            clientes = clientes.filter(filtros)
            
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
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    usuario = cliente.id_usuario  

    if request.method == 'POST':
        # 📌 TRUCO MAESTRO: Copiamos los datos del POST para poder modificarlos
        datos_post = request.POST.copy()
        
        # 🛠️ Forzamos que viajen los datos actuales de la BD si no vienen en el POST
        if 'nombre' not in datos_post or not datos_post['nombre']:
            datos_post['nombre'] = cliente.nombre
        if 'documento_id' not in datos_post or not datos_post['documento_id']:
            datos_post['documento_id'] = cliente.documento_id

        # Pasamos los datos parchados al formulario
        form = ClienteForm(datos_post, instance=cliente)

        if form.is_valid():
            form.save() 
            messages.success(request, "Cliente actualizado con éxito.")
            return redirect('clientes:listar') # Revisa si usas 'listar' o 'listar_clientes'
    else:
        correo_actual = usuario.email if usuario else ''
        form = ClienteForm(instance=cliente, initial={'email': correo_actual})

    return render(request, 'clientes/editar.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    
    # 🔐 VALIDACIÓN DE SEGURIDAD EN EL BACKEND REAL:
    # Filtramos en la tabla Empeno si existe algún registro con el id de este cliente
    if Empeno.objects.filter(id_cliente=cliente).exists():
        messages.error(request, 'Acción inválida: Este cliente posee empeños activos.')
        return redirect('clientes:listar')

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