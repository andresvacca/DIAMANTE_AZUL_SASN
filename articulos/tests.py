from django.test import TestCase
from articulos.models import Articulos
from .forms import ArticuloForm, FiltroArticuloForm

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