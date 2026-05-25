from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
# Importamos los modelos correctamente
from usuarios.models import Usuario, Rol

class UsuarioTest(TestCase):
    def setUp(self):
        # Creamos los roles necesarios
        self.rol_admin = Rol.objects.create(nombre="Administrador")
        self.rol_cliente = Rol.objects.create(nombre="Cliente")
        
        # Creamos un usuario de prueba (sin forzar IDs para evitar errores de duplicados)
        self.usuario = Usuario.objects.create(
            nombre="Juan Guillermo Vacca",
            email="juanvacca@gmail.com",
            password_hash=make_password("password123"),
            id_rol=self.rol_admin,
        )

    def test_creacion_usuario(self):
        """Verifica que el usuario se guarde correctamente en la BD."""
        usuario_db = Usuario.objects.get(email="juanvacca@gmail.com")
        self.assertEqual(usuario_db.nombre, "Juan Guillermo Vacca")
        self.assertEqual(usuario_db.id_rol.nombre, "Administrador")

    def test_seguridad_contrasena(self):
        """Verifica que el sistema maneje el hash y no el texto plano."""
        raw_password = "password123"
        # Comprobamos que el hash funciona
        self.assertTrue(check_password(raw_password, self.usuario.password_hash))
        # Comprobamos que no se guardó el texto plano
        self.assertNotEqual(self.usuario.password_hash, raw_password)

    def test_roles_helper(self):
        """Verifica que los métodos del modelo funcionen."""
        # Validamos que el usuario creado sea reconocido como Administrador
        self.assertEqual(self.usuario.get_rol_nombre(), "Administrador")