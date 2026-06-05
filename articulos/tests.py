from django.test import TestCase
from articulos.models import Articulos
from .forms import ArticuloForm, FiltroArticuloForm
import io
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class ArticuloTest(TestCase):
    def setUp(self):
        self.articulo = Articulos.objects.create(
            nombre="Reloj de Oro",
            descripcion="Reloj suizo de lujo",
            numero_serie="SN-12345",
            categoria="Oro",
            estado="Empeñado", # Usamos uno que sí está en tus choices
            precio_sugerido_venta=500.00,
            quilataje="18"
        )

    def test_articulo_form_camino_feliz(self):
        """Formulario Artículo: Datos válidos y correctos deben pasar la validación."""
        datos_validos = {
            'nombre': "Anillo de Oro de 18k",      
            'numero_serie': "SERIE-9988X",         
            'descripcion': "Anillo con esmeralda colombiana",
            'categoria': "Oro",
            'estado': "En venta",
            'precio_sugerido_venta': 1250000.00,
            'quilataje': "18"
        }
        form = ArticuloForm(data=datos_validos)
        
        # 🌟 SI FALLA, IMPRIMIMOS EL ERROR EXACTO EN CONSOLA
        if not form.is_valid():
            print("\n[DEBUG ARTICULOS] Errores del formulario:", form.errors.as_text())
            
        self.assertTrue(form.is_valid())
        
        

    def test_editar_articulo_camino_feliz(self):
        """Camino feliz: Modificar exitosamente las propiedades de un artículo mediante POST."""
        session = self.client.session
        session['usuario_rol_id'] = 1 
        session.save()

        # 🌟 CORREGIDO: Cambiamos temporalmente el estado en el objeto de prueba a 'Disponible'
        # para que la lógica de tu vista permita procesar la edición por formulario.
        self.articulo.estado = "Disponible"
        self.articulo.save()

        from django.urls import reverse
        url = reverse('articulos:editar', kwargs={'id_articulo': self.articulo.id_articulo})
        
        datos_nuevos = {
            'nombre': "Reloj de Oro Modificado",
            'descripcion': "Nueva descripción de lujo",
            'numero_serie': "SN-54321",
            'categoria': "Oro",
            'estado': "En venta", 
            'precio_sugerido_venta': 650.00,
            'quilataje': "18"
        }
        
        response = self.client.post(url, datos_nuevos, follow=True)
        self.assertEqual(response.status_code, 200)
        
        self.articulo.refresh_from_db()
        self.assertEqual(self.articulo.nombre, "Reloj de Oro Modificado")
        self.assertEqual(self.articulo.estado, "En venta")
        
class ArticuloFormTest(TestCase):

    def test_articulo_form_camino_feliz(self):
        """Formulario Artículo: Datos válidos y correctos deben pasar la validación."""
        datos_validos = {
            'nombre': "Anillo de Oro de 18k",      # Cumple MinLengthValidator(5)
            'numero_serie': "SERIE-9988X",         # Cumple MinLengthValidator(5)
            'descripcion': "Anillo con esmeralda colombiana",
            'categoria': "Oro",
            'estado': "En venta",
            'precio_sugerido_venta': 1250000.00,
            'quilataje': "18"
        }
        form = ArticuloForm(data=datos_validos)
        self.assertTrue(form.is_valid())

    def test_articulo_form_nombre_demasiado_corto(self):
        """Formulario Artículo: Si el nombre tiene menos de 5 caracteres debe fallar."""
        datos_invalidos = {
            'nombre': "Oro",                       # ❌ Falla MinLengthValidator(5)
            'numero_serie': "SERIE-9988X",
            'descripcion': "Descripción de prueba",
            'categoria': "Oro",
            'estado': "En venta",
            'precio_sugerido_venta': 50000.00,
            'quilataje': "18"
        }
        form = ArticuloForm(data=datos_invalidos)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertEqual(form.errors['nombre'][0], "El nombre debe tener al menos 5 caracteres")

    def test_articulo_form_numero_serie_obligatorio(self):
        """Formulario Artículo: Si la serie falta o está vacía debe fallar."""
        datos_sin_serie = {
            'nombre': "Reloj Rolex Usado",
            'numero_serie': "",                    # ❌ Campo obligatorio
            'categoria': "Relojes",
            'estado': "En venta",
            'precio_sugerido_venta': 8500000.00,
        }
        form = ArticuloForm(data=datos_sin_serie)
        self.assertFalse(form.is_valid())
        self.assertIn('numero_serie', form.errors)

    def test_filtro_articulo_form_vacio_es_valido(self):
        """Filtro Artículo: Si no se mandan parámetros, es válido (muestra todos)."""
        datos_vacios = {'buscar_id': '', 'q': '', 'estado': '', 'categoria': ''}
        form = FiltroArticuloForm(data=datos_vacios)
        self.assertTrue(form.is_valid())

    def test_filtro_articulo_form_con_parametros(self):
        """Filtro Artículo: Debe procesar y limpiar correctamente los filtros aplicados."""
        datos_filtro = {
            'buscar_id': 45,
            'q': "Cadena",
            'estado': "Empeñado",
            'categoria': "Oro"
        }
        form = FiltroArticuloForm(data=datos_filtro)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('buscar_id'), 45)
        

class ArticuloCargaMasivaTest(TestCase):

    def setUp(self):
        # Configurar la sesión del administrador para saltar los controles de seguridad
        session = self.client.session
        session['usuario_rol_id'] = 1  # Administrador
        session.save()

    def test_carga_masiva_csv_camino_feliz(self):
        """Camino feliz: Sube un archivo CSV con artículos válidos y los inserta en la BD."""
        from django.urls import reverse
        from django.core.files.uploadedfile import SimpleUploadedFile
        from articulos.models import Articulos

        url = reverse('articulos:carga_masiva')

        # 1. Estructuramos el contenido simulado tal como lo lee tu lector_csv posicional:
        # Fila[0]=nombre, Fila[1]=descripcion, Fila[2]=numero_serie, Fila[3]=categoria...
        # Pasamos el precio como entero limpio para la validación .isdigit() de tu vista
        contenido_csv = (
            "nombre,descripcion,numero_serie,categoria,estado,precio_sugerido_venta,quilataje\n"
            "Cadena de Oro Tejida,Cadena de 20gr,CAD-TEJ-101,Oro,Disponible,2500000,18\n"
        )
        
        archivo_simulado = SimpleUploadedFile(
            name='carga_inventario.csv',
            content=contenido_csv.encode('utf-8'),
            content_type='text/csv'
        )

        # 🛡️ CLAVE CORREGIDA: Cambiamos 'archivo' por 'archivo_masivo' para sincronizar con tu views.py
        response = self.client.post(url, {'archivo_masivo': archivo_simulado}, follow=True)
        
        # Bloque de asistencia en consola por si necesitas ver qué sucede en el flujo
        if not Articulos.objects.filter(numero_serie="CAD-TEJ-101").exists():
            print("\n" + "="*60)
            print("[DIAGNÓSTICO EN VIVO]")
            if 'messages' in response.context:
                print("Mensajes de la vista:", [m.message for m in response.context['messages']])
            print("="*60 + "\n")

        # Verificaciones finales
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Articulos.objects.filter(numero_serie="CAD-TEJ-101").exists())

    def test_carga_masiva_archivo_invalido_o_vacio(self):
        """Camino alterno: Si el archivo no tiene el formato correcto, debe fallar controladamente."""
        from django.urls import reverse
        # Modifica la línea 181 dentro de test_carga_masiva_archivo_invalido_o_vacio
        url = reverse('articulos:carga_masiva') # 👈 Cambiado a su nombre real

        # Subimos un archivo con formato de texto basura que rompería el parseador lógico
        archivo_invalido = SimpleUploadedFile(
            name='documento_invalido.txt',
            content=b"Texto plano aleatorio que no es un CSV estructurado",
            content_type='text/plain'
        )

        response = self.client.post(url, {'archivo': archivo_invalido}, follow=True)
        
        # El sistema debe manejar el error sin lanzar un error 500 (debe retornar 200 con mensajes de alerta)
        self.assertEqual(response.status_code, 200)
        
        # Verificamos que la base de datos permanezca limpia y vacía ante la falla
        self.assertEqual(Articulos.objects.count(), 1)
        


    def setUp(self):
        # Creamos un artículo base para interactuar con los detalles y la eliminación
        self.articulo = Articulos.objects.create(
            nombre="Anillo de Plata Precolombino",
            descripcion="Anillo grabado ley 925",
            numero_serie="ANI-PL-777",
            categoria="Plata",
            estado="Disponible",
            precio_sugerido_venta=180000,
            quilataje="0"
        )

    def test_vista_detalle_articulo_existente(self):
        """Verifica que la página de detalles de un artículo cargue correctamente."""
        url = reverse('articulos:detalle', args=[self.articulo.id_articulo])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ANI-PL-777")

    def test_eliminar_articulo_exitoso(self):
        """Verifica que un POST a la vista eliminar remueva el registro de la BD."""
        url = reverse('articulos:eliminar', args=[self.articulo.id_articulo])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        # Verificamos que ya no exista en la base de datos
        self.assertFalse(Articulos.objects.filter(id_articulo=self.articulo.id_articulo).exists())

    def test_descargar_csv_ejemplo_formato(self):
        """Verifica que la descarga del CSV de ejemplo devuelva el tipo de contenido correcto."""
        url = reverse('articulos:descargar_csv_ejemplo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')

    def test_exportar_excel_response(self):
        """Verifica que la exportación a Excel genere un archivo binario válido."""
        url = reverse('articulos:exportar_excel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_exportar_pdf_response(self):
        """Verifica que la exportación a PDF responda con la cabecera de documento PDF."""
        url = reverse('articulos:exportar_pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')