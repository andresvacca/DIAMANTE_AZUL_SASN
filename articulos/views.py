from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Articulos
from .forms import ArticuloForm, FiltroArticuloForm
import json
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.http import HttpResponse
from .models import Articulos
from django.db.models import Q
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def listar_articulos(request):
    # Seguridad (opcional, si quieres restringir quién ve el inventario)
    # if not (_requiere_admin(request) or _requiere_empleado(request)):
    #     return redirect('usuarios:login')

    # 1. Iniciamos el queryset
    articulos = Articulos.objects.all().order_by('-id_articulo')
    
    # 2. Procesamos el formulario de filtro
    form = FiltroArticuloForm(request.GET)
    
    if form.is_valid():
        q = form.cleaned_data.get('q')
        estado = form.cleaned_data.get('estado')
        categoria = form.cleaned_data.get('categoria')

        # Filtros multicriterio
        if q:
            # Busca en nombre, descripción o número de serie
            articulos = articulos.filter(
                Q(nombre__icontains=q) | 
                Q(descripcion__icontains=q) | 
                Q(numero_serie__icontains=q)
            )
        if estado:
            articulos = articulos.filter(estado=estado)
        if categoria:
            articulos = articulos.filter(categoria=categoria)

    # 3. Lógica extra para el reporte: Calculamos totales rápidos
    total_articulos = articulos.count()
    valor_inventario = articulos.aggregate(Sum('precio_sugerido_venta'))['precio_sugerido_venta__sum'] or 0

    context = {
        'articulos': articulos,
        'form': form,
        'total_count': total_articulos,
        'valor_total': valor_inventario
    }
    
    return render(request, 'articulos/listar.html', context)


def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo registrado correctamente.')
            return redirect('articulos:listar')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ArticuloForm()
    return render(request, 'articulos/crear.html', {'form': form})


def editar_articulo(request, id_articulo):
    articulo = get_object_or_404(Articulos, pk=id_articulo)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo actualizado correctamente.')
            return redirect('articulos:listar')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'articulos/editar.html', {'form': form, 'articulo': articulo})


def eliminar_articulo(request, id_articulo):
    articulo = get_object_or_404(Articulos, pk=id_articulo)
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, 'Artículo eliminado correctamente.')
        return redirect('articulos:listar')
    return render(request, 'articulos/eliminar.html', {'articulo': articulo})


def crear_articulo_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Inyectamos estado antes de validar
        data['estado'] = 'Empeñado'
        form = ArticuloForm(data)
        if form.is_valid():
            articulo = form.save()
            return JsonResponse({'ok': True, 'id': articulo.id_articulo, 'nombre': articulo.nombre})
        else:
            errores = {campo: e[0] for campo, e in form.errors.items()}
            return JsonResponse({'ok': False, 'error': errores})
    return JsonResponse({'ok': False, 'error': 'Método no permitido.'})

def carga_masiva_articulos(request):
    from usuarios.views import _requiere_admin, _requiere_empleado
    if not (_requiere_admin(request) or _requiere_empleado(request)):
        return redirect('usuarios:login')

    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        import csv
        import io
        from django.contrib import messages

        archivo = request.FILES['archivo_csv']
        decoded = archivo.read().decode('utf-8')
        reader  = csv.DictReader(io.StringIO(decoded))

        categorias_validas = ['Bicicletas','Neveras','Oro','Plata','Ollas','VideoJuegos','Relojes','Computadores','Otro']
        estados_validos    = ['En venta','Empeñado','Vendido','Vencido']
        quilatajes_validos = ['18','16','14','10','0']

        nuevos   = []
        errores  = []

        for i, fila in enumerate(reader, start=2):
            try:
                nombre    = fila.get('nombre', '').strip()
                categoria = fila.get('categoria', '').strip()
                estado    = fila.get('estado', 'En venta').strip()
                precio    = fila.get('precio_sugerido_venta', '0').strip()
                quilataje = fila.get('quilataje', '0').strip()

                if not nombre:
                    errores.append(f"Fila {i}: el campo 'nombre' es obligatorio.")
                    continue
                if categoria not in categorias_validas:
                    errores.append(f"Fila {i}: categoría '{categoria}' no válida.")
                    continue
                if estado not in estados_validos:
                    errores.append(f"Fila {i}: estado '{estado}' no válido.")
                    continue
                if quilataje not in quilatajes_validos:
                    quilataje = '0'

                nuevos.append(Articulos(
                    nombre               = nombre,
                    descripcion          = fila.get('descripcion', '').strip() or None,
                    numero_serie         = fila.get('numero_serie', '').strip() or None,
                    categoria            = categoria,
                    estado               = estado,
                    precio_sugerido_venta= float(precio),
                    quilataje            = quilataje,
                ))
            except Exception as e:
                errores.append(f"Fila {i}: error — {e}")

        if nuevos:
            Articulos.objects.bulk_create(nuevos)
            messages.success(request, f'{len(nuevos)} artículos cargados correctamente.')
        if errores:
            for err in errores:
                messages.warning(request, err)

        return redirect('articulos:listar')

    return render(request, 'articulos/carga_masiva.html')

def descargar_csv_ejemplo(request):
    from django.http import HttpResponse
    contenido = "nombre,descripcion,numero_serie,categoria,estado,precio_sugerido_venta,quilataje\n"
    contenido += "Bicicleta Trek,Bicicleta de montaña azul,TRK-001,Bicicletas,En venta,350000,0\n"
    response = HttpResponse(contenido, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="articulos_ejemplo.csv"'
    return response


def detalle_articulo(request, id_articulo):
    articulo = get_object_or_404(Articulos, pk=id_articulo)
    
    # Obtenemos el empeño relacionado
    empeno = articulo.empeno_set.first()
    contrato = None
    pagos = []
    
    if empeno:
        # Si hay empeño, buscamos su contrato y sus pagos
        from contratos.models import Contrato # Import local para evitar circularidad
        contrato = Contrato.objects.filter(id_empeno=empeno).first()
        pagos = empeno.pago_set.all().order_by('-fecha_pago')

    return render(request, 'articulos/detalle.html', {
        'articulo': articulo,
        'empeno': empeno,
        'contrato': contrato,
        'pagos': pagos,
    })



'''FUNCION REPORTES EXCEL O PDF'''
# Función auxiliar para filtrar (evita repetir código)
def _obtener_articulos_filtrados(request):
    q = request.GET.get('q')
    estado = request.GET.get('estado')
    categoria = request.GET.get('categoria')
    
    articulos = Articulos.objects.all()
    if q:
        articulos = articulos.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    if estado:
        articulos = articulos.filter(estado=estado)
    if categoria:
        articulos = articulos.filter(categoria=categoria)
    return articulos

# --- EXPORTAR A EXCEL ---
def exportar_articulos_excel(request):
    articulos = _obtener_articulos_filtrados(request)
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventario Artículos"

    # Cabeceras
    headers = ['ID', 'Nombre', 'Categoría', 'Estado', 'Precio Sugerido', 'Quilataje']
    ws.append(headers)

    # Datos
    for art in articulos:
        ws.append([art.id_articulo, art.nombre, art.categoria, art.estado, art.precio_sugerido_venta, art.quilataje])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_articulos.xlsx"'
    wb.save(response)
    return response

# --- EXPORTAR A PDF ---
def exportar_articulos_pdf(request):
    articulos = _obtener_articulos_filtrados(request)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_articulos.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Diamante Azul - Reporte de Inventario", styles['Title']))

    # Crear tabla para el PDF
    data = [['ID', 'Nombre', 'Categoría', 'Estado', 'Precio']]
    for art in articulos:
        data.append([art.id_articulo, art.nombre[:20], art.categoria, art.estado, f"${art.precio_sugerido_venta}"])

    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.cadetblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(t)
    doc.build(elements)
    return response