from django.test import TestCase
from articulos.models import Articulos

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

    def test_creacion_articulo(self):
        """Verifica que el articulo se cree con los datos correctos."""
        # Buscamos por el ID real que definiste
        articulo_db = Articulos.objects.get(id_articulo=self.articulo.id_articulo)
        
        self.assertEqual(articulo_db.nombre, "Reloj de Oro")
        self.assertEqual(articulo_db.categoria, "Oro")
        self.assertEqual(articulo_db.quilataje, "18")