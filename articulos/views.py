from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Articulos
from .forms import ArticuloForm, FiltroArticuloForm
import json
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.db.models import Q
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import csv
import openpyxl
from django.core.paginator import Paginator


def listar_articulos(request):
    # Seguridad (opcional, si quieres restringir quién ve el inventario)
    # if not (_requiere_admin(request) or _requiere_empleado(request)):
    #     return redirect('usuarios:login')

    # 1. Iniciamos el queryset
    articulos = Articulos.objects.all().order_by('-id_articulo')    
    
    # 2. Procesamos el formulario de filtro
    form = FiltroArticuloForm(request.GET)
    
    if form.is_valid():
        buscar_id = form.cleaned_data.get('buscar_id')
        q = form.cleaned_data.get('q')
        estado = form.cleaned_data.get('estado')
        categoria = form.cleaned_data.get('categoria')
        
        if buscar_id:
            articulos = articulos.filter(id_articulo=buscar_id)
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
    articulos_por_pagina = 10
    paginator = Paginator(articulos, articulos_por_pagina)
    
    # 2. Capturamos qué página está viendo el usuario desde la URL (ej: ?page=2)
    numero_pagina = request.GET.get('page')
    
    # 3. Extraemos los registros que corresponden únicamente a esa página
    page_obj = paginator.get_page(numero_pagina)
    
    # 🚨 IMPORTANTE: Al HTML ahora le pasamos 'page_obj' en lugar de 'articulos'
    return render(request, 'articulos/listar.html', {'articulos': page_obj, 'form': form})


def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo registrado correctamente.')
            return redirect('articulos:listar')
        
        # Este bloque se ejecuta SI HAY ERRORES de validación
        print("ERRORES:", form.errors.as_data()) # Para ver el fallo en la consola
        messages.error(request, 'Por favor corrige los errores del formulario.')
    
    else:
        # Este bloque se ejecuta la PRIMERA VEZ que entras (GET)
        form = ArticuloForm()
    
    # Este return DEBE estar al final, alineado con el primer 'if'
    # Así siempre devuelve la página, ya sea con el form vacío o con errores
    return render(request, 'articulos/crear.html', {'form': form})


def editar_articulo(request, id_articulo):
    articulo = get_object_or_404(Articulos, pk=id_articulo)
    if articulo.estado in ['Vendido', 'Retirado', 'Empeñado']:
        messages.error(request, f"No se puede editar el articulo por motivos de seguridad  (estado: {articulo.estado})")
        return redirect('articulos:listar')
    
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
    if request.method == 'POST':
        archivo = request.FILES.get('archivo_masivo') 
        
        if not archivo:
            messages.error(request, 'No has seleccionado ningún archivo.')
            return redirect('articulos:carga_masiva')

        nombre_archivo = file_name = archivo.name.lower()

        # 🛡️ FILTRO RADICAL
        if not (nombre_archivo.endswith('.csv') or nombre_archivo.endswith('.xlsx') or nombre_archivo.endswith('.xls')):
            messages.error(request, 'Formato inválido. ¡Aquí solo se acepta CSV o Excel!')
            return redirect('articulos:carga_masiva')

        try:
            # 📈 CASO 1: EXCEL (.xlsx)
            if nombre_archivo.endswith('.xlsx') or nombre_archivo.endswith('.xls'):
                wb = openpyxl.load_workbook(archivo, data_only=True)
                hoja = wb.active
                
                for fila in hoja.iter_rows(min_row=2, values_only=True):
                    if not fila or not fila[0]: 
                        continue
                        
                    # 🎯 CORRECCIÓN: 'Articulo' en singular (revisa si tu modelo es así)
                    Articulos.objects.create(
                        nombre=fila[0],
                        descripcion=fila[1],
                        numero_serie=fila[2],
                        categoria=fila[3],
                        estado=fila[4],
                        precio_sugerido_venta=fila[5] if fila[5] else 0,
                        quilataje=fila[6] if fila[6] else 0
                    )

            # 📄 CASO 2: CSV
            elif nombre_archivo.endswith('.csv'):
                try:
                    contenido_decodificado = archivo.read().decode('utf-8')
                except UnicodeDecodeError:
                    archivo.seek(0)
                    contenido_decodificado = archivo.read().decode('latin-1')

                lector_csv = csv.reader(contenido_decodificado.splitlines(), delimiter=';') 
                next(lector_csv, None)  # Saltar cabecera
                
                for fila in lector_csv:
                    if not fila or not fila[0]:
                        continue
                        
                    # 🎯 CORRECCIÓN: 'Articulos' en singular
                    Articulos.objects.create(
                        nombre=fila[0],
                        descripcion=fila[1],
                        numero_serie=fila[2],
                        categoria=fila[3],
                        estado=fila[4],
                        precio_sugerido_venta=fila[5] if fila[5] else 0,
                        quilataje=fila[6] if fila[6] else 0
                    )

            # 🚀 RETORNO EXITOSO DEL POST
            messages.success(request, '¡Carga masiva procesada con éxito')
            return redirect('articulos:listar')

        except Exception as e:
            messages.error(request, f'Hubo un error procesando el archivo: {str(e)}')
            return redirect('articulos:carga_masiva')

    # 🚨 LA PIEZA FALTANTE: Render del GET totalmente alineado al borde izquierdo
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
        pagos = empeno.cuota_set.all().order_by('-fecha_programada')

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