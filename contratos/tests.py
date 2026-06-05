from django.test import TestCase
from django.urls import reverse
from usuarios.models import Rol, Usuario

class CoberturaMasivaVistasGetTest(TestCase):

    def setUp(self):
        # 🛡️ get_or_create evita colisionar si el ID 1 ya existe en la sesión de pruebas de MySQL
        self.rol_admin, _ = Rol.objects.get_or_create(
            id_rol=1, 
            defaults={'nombre': "Administrador"}
        )
        
        self.usuario_admin, _ = Usuario.objects.get_or_create(
            email="admin_pruebas_masivas@diamante.com",
            defaults={
                'nombre': "Admin de Pruebas",
                'id_rol': self.rol_admin,
                'password_hash': 'hash_simulado_test'
            }
        )

    def test_vistas_principales_html_renderizan_200_ok(self):
        """Test Masivo: Comprueba que todas las vistas de administración carguen correctamente."""
        # Inyectamos la sesión una sola vez
        session = self.client.session
        session['usuario_rol_id'] = self.rol_admin.id_rol
        session['usuario_id'] = self.usuario_admin.id_usuario
        session.save()

        # 🌟 LISTA DE URLS A TESTEAR DE GOLPE
        # Añade aquí los names de tus urls que carguen listados o páneles (vistas GET)
        # Reemplaza la lista de URLs que se itera en tu test masivo por esta:
        urls_a_probar = [
            'usuarios:listar',      # En tu urls.py es: path('', views.listar_usuarios, name='listar')
            'clientes:listar',      # En tu urls.py es: path('', views.listar_clientes, name='listar')
            'articulos:listar',     # En tu urls.py es: path('', views.listar_articulos, name='listar')
            'compras:listar',       # En tu urls.py es: path('', views.listar_compras, name='listar')
            'contratos:listar',     # En tu urls.py es: path('', views.listar_contratos, name='listar')
            'cuadre_caja:index',    # 🛡️ CORRECCIÓN: Tu app_name es 'cuadre_caja' y tu path name es 'index'
        ]

        for url_name in urls_a_probar:
            with self.subTest(url=url_name): # subTest evita que si una falla, las demás se detengan
                response = self.client.get(reverse(url_name))
                self.assertEqual(
                    response.status_code, 200, 
                    f"La vista {url_name} falló devolviendo un {response.status_code} en lugar de 200"
                )