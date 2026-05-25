from django.test import TestCase
from django.urls import reverse
from .models import Usuario, Rol

class UsuarioTest(TestCase):
    def setUp(self):
        self.rol_admin = Rol.objects.create(nombre="Administrador")
        self.rol_empleado = Rol.objects.create(nombre="Empleado")
        self.rol_cliente = Rol.objects.create(nombre="Cliente")
        self.password_hash = "Pablito123!"
        
        self.usuario = Usuario.objects.create(
            nombre = "Juan Guillermo Vacca",
            email = "juanvacca@gmail.com",
            password_hash = self.password_hash,
            id_rol=self.rol_admin,
        )
        
        return 
    
    def test_creacion_usuario(self):
        self.assertEqual(self.usuario.nombre, "Juan Guillermo Vacca"),
        self.assertEqual(self.usuario.id_rol.nombre, "Administrador"),# Verificamos la relación
        self.assertEqual(self.usuario.email, "juanvacca@gmail.com"),
        
        self.assertTrue(Usuario.objects.filter(email="juanvacca@gmail.com").exists())