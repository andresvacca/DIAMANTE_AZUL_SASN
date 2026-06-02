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

def descargar_csv_ejemplo(request):
    """
    Genera y descarga dinámicamente el archivo CSV de ejemplo 
    con la estructura exacta que requiere el sistema.
    """
    # Configurar la respuesta HTTP para la descarga de un archivo CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="articulos_ejemplo.csv"'
    
    writer = csv.writer(response)
    
    # 1. Escribir los encabezados de las columnas (Fila 1)
    writer.writerow(['nombre', 'descripcion', 'numero_serie', 'categoria', 'estado', 'precio_sugerido_venta', 'quilataje'])
    
    # 2. Escribir una fila de ejemplo para guiar al usuario (Fila 2)
    writer.writerow(['Bicicleta Trek', 'Bicicleta de montaña azul', 'TRK-001', 'Bicicletas', 'En venta', '350000', '0'])
    
    return response


def carga_masiva_articulos(request):
    if request.method == 'POST':
        archivo_subido = request.FILES.get('archivo_masivo') # Sincronizado con tu nuevo HTML
        
        if not archivo_subido:
            messages.error(request, 'Por favor, selecciona un archivo CSV para subir.')
            return render(request, 'articulos/carga_masiva.html')
        
        try:
            # 1. Leer y decodificar el contenido limpiando espacios en blanco extraños
            contenido_bloque = archivo_subido.read().decode('utf-8', errors='ignore')
            lineas = [linea.strip() for linea in contenido_bloque.splitlines() if linea.strip()]
            
            if not lineas:
                messages.error(request, 'El archivo está vacío.')
                return render(request, 'articulos/carga_masiva.html')

            # 2. DETECTOR AUTOMÁTICO DE SEPARADORES (Coma , o Punto y coma ;)
            try:
                # Intenta adivinar si usa , o ; analizando las primeras líneas
                dialecto = csv.Sniffer().sniff(contenido_bloque[:2048], delimiters=',;')
                lector_csv = csv.reader(lineas, dialecto)
            except Exception:
                # Si falla el detector, por defecto usamos comas
                lector_csv = csv.reader(lineas, delimiter=',')
            
            # Saltarse la primera línea de encabezados (nombre, descripcion...)
            next(lector_csv, None)
            
            articulos_creados = 0
            
            for fila in lector_csv:
                # Si por alguna razón la fila quedó vacía tras el procesado, la saltamos
                if not fila or len(fila) == 0:
                    continue
                
                # 🔥 EL BLINDAJE ABSOLUTO: Forzamos a que la lista tenga siempre mínimo 7 columnas
                # Si viene mocha (ej. con 3 o 5 columnas), se rellena con None y NO se rompe
                while len(fila) < 7:
                    fila.append(None)
                
                # Validar que el campo obligatorio (nombre) contenga texto
                if not fila[0] or str(fila[0]).strip() == '':
                    continue

                # 3. Mapeo e inserción segura en la base de datos de Diamante Azul
                Articulos.objects.create(
                    nombre=str(fila[0]).strip(),
                    descripcion=str(fila[1]).strip() if fila[1] else None,
                    numero_serie=str(fila[2]).strip() if fila[2] else None,
                    categoria=str(fila[3]).strip() if fila[3] else 'Otro',
                    estado=str(fila[4]).strip() if fila[4] else 'En venta',
                    precio_sugerido_venta=float(fila[5]) if fila[5] and str(fila[5]).strip().replace('.','',1).isdigit() else 0,
                    quilataje=str(fila[6]).strip() if fila[6] else '0'
                )
                articulos_creados += 1
                
            if articulos_creados > 0:
                messages.success(request, f'¡Carga masiva exitosa! Se registraron {articulos_creados} artículos correctamente.')
            else:
                messages.warning(request, 'No se procesó ningún artículo válido. Verifica el formato.')
                
            return redirect('articulos:carga_masiva')

        except Exception as e:
            messages.error(request, f'Error crítico al procesar las columnas: {str(e)}')
            return render(request, 'articulos/carga_masiva.html')

    return render(request, 'articulos/carga_masiva.html')

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