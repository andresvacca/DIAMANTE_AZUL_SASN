from django.test import TestCase
from django.urls import reverse
from .models import Usuario, Rol

class UsuarioTest(TestCase):
    def setUp(self):
        self.rol_admin = Rol.objects.create(nombre="Administrador")
        self.rol_empleado = Rol.objects.create(nombre="Empleado")
        self.rol_cliente = Rol.objects.create(nombre="Cliente")
        
        self.usuario = Usuario.objects.create(
            nombre = "Juan Guillermo Vacca",
            email = "juanvacca@gmail.com",
           
        )
        
        return 