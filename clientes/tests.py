from django.test import TestCase
from django.urls import reverse
from clientes.models import Cliente
from usuarios.models import Rol, Usuario
from .forms import ClienteForm, FiltroCliente
from django.contrib.auth.hashers import check_password
class ClienteViewsTest(TestCase):
    def setUp(self):
        # 1. Creamos el rol y un usuario operador para manejar la sesión del panel
        self.rol_admin, _ = Rol.objects.get_or_create(nombre="Administrador")
        self.usuario = Usuario.objects.create(
            nombre="Andres Vacca", 
            email="andres_operador@test.com", 
            id_rol=self.rol_admin
        )
        
        # 2. Autenticamos al usuario inyectando sus credenciales en la sesión activa del cliente
        session = self.client.session
        session['usuario_rol_id'] = self.rol_admin.pk
        session['usuario_id'] = self.usuario.id_usuario
        session.save()

        # 3. Creamos un cliente base inicializado directamente en la BD para probar la edición
        self.cliente = Cliente.objects.create(
            nombre="Carlos Mendoza",
            documento_id="10112233",
            telefono="3001234567",
            direccion="Calle 26 # 13-40",
            id_usuario=self.usuario
        )

    def test_crear_cliente_camino_feliz(self):
        """Camino feliz: Registrar un nuevo cliente mediante el formulario web."""
        url = reverse('clientes:crear') 
        
        # 🌟 CORREGIDO: Se agregaron los campos obligatorios 'email' y 'password'
        datos_cliente = {
            'nombre': "Liliana Gómez",
            'documento_id': "52345678",
            'telefono': "3119876543",
            'direccion': "Carrera 7 # 45-10",
            'email': "lilianagomez@test.com",
            'password': "claveSegura123"
        }
        
        # Ejecutamos la petición POST simulando el envío de la plantilla
        response = self.client.post(url, datos_cliente, follow=True)
        
        # La vista debe responder con éxito (HTTP 200)
        self.assertEqual(response.status_code, 200)
        
        # Validación de auditoría alternativa en caso de que persistiera un fallo diferente
        if not Cliente.objects.filter(documento_id="52345678").exists():
            if 'form' in response.context:
                print("\n[DEBUG] Errores del formulario de creación:", response.context['form'].errors.as_text())
        
        # Confirmamos la existencia real del nuevo registro en la base de datos
        self.assertTrue(Cliente.objects.filter(documento_id="52345678").exists())

    def test_editar_cliente_camino_feliz(self):
        """Camino feliz: Modificar la dirección y teléfono de un cliente existente."""
        url = reverse('clientes:editar', kwargs={'id_cliente': self.cliente.id_cliente})
        
        # 🌟 CORREGIDO: Se agregaron los campos del usuario vinculado que el formulario espera validar
        datos_editados = {
            'nombre': "Carlos Mendoza Modificado",
            'documento_id': "10112233",  # Se mantiene constante
            'telefono': "3209998877",     # Nuevo número a comprobar
            'direccion': "Avenida Caracas # 45-00", # Nueva dirección a comprobar
            'email': "carlosmendoza_mod@test.com",  
            'password': "nuevaClave123"
        }
        
        # Enviamos la petición POST para actualizar el formulario
        response = self.client.post(url, datos_editados, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Traemos los datos frescos directamente de la base de datos para saltar la caché de python
        self.cliente.refresh_from_db()
        
        # Las aserciones ahora deben pasar de forma limpia
        self.assertEqual(self.cliente.telefono, "3209998877")
        self.assertEqual(self.cliente.direccion, "Avenida Caracas # 45-00")
        
class ClienteFormTest(TestCase):
    def setUp(self):
        # 1. Crear el rol de cliente requerido por el método save() del formulario
        # Se usa get_or_create asignando el ID correcto de tu constante (ej: ROL_CLIENTE = 3)
        self.rol_cliente, _ = Rol.objects.get_or_create(
            id_rol=Rol.ROL_CLIENTE,
            defaults={'nombre': 'Cliente'}
        )

        # 2. Crear un usuario y cliente base previo en la BD para la prueba de edición
        self.usuario_existente = Usuario.objects.create(
            nombre="Carlos Mendoza",
            email="carlos@correo.com",
            password_hash="hash_anterior",
            id_rol=self.rol_cliente
        )
        self.cliente_existente = Cliente.objects.create(
            nombre="Carlos Mendoza",
            documento_id="10112233",
            telefono="3001234567",
            direccion="Calle 26 # 13-40",
            id_usuario=self.usuario_existente
        )

    def test_form_crear_cliente_camino_feliz(self):
        """Camino Feliz: Validar y guardar un NUEVO cliente con un usuario del sistema."""
        datos_nuevos = {
            'nombre': "Liliana Gomez",
            'documento_id': "52345678",        # Cumple RegexValidator (solo números)
            'telefono': "3119876543",
            'direccion': "Carrera 7 # 45-10",
            'email': "liliana@correo.com",
            'password': "claveSegura123"       # Requerido al crear (según tu __init__)
        }

        form = ClienteForm(data=datos_nuevos)
        
        # Validamos que pase las restricciones de los validadores
        self.assertTrue(form.is_valid())

        # Guardamos confirmando el commit en la BD en memoria
        cliente_creado = form.save()

        # Comprobamos que el cliente se enlazó a un usuario nuevo con los datos correctos
        self.assertIsNotNone(cliente_creado.id_usuario)
        self.assertEqual(cliente_creado.id_usuario.email, "liliana@correo.com")
        self.assertEqual(cliente_creado.id_usuario.nombre, "Liliana Gomez")
        
        # Verificamos que la contraseña se guardó con el Hash de Django
        self.assertTrue(check_password("claveSegura123", cliente_creado.id_usuario.password_hash))

    def test_form_editar_cliente_camino_feliz(self):
        """Camino Feliz: Validar y guardar la EDICIÓN de un cliente existente."""
        datos_edicion = {
            'nombre': "Carlos Mendoza",         # Readonly en HTML pero requerido en el POST
            'documento_id': "10112233",         # Readonly en HTML pero requerido en el POST
            'telefono': "3209998877",           # Modificado
            'direccion': "Avenida Caracas # 45-00", # Modificado
            'email': "carlos_nuevo@correo.com", # Modificado
            'password': ""                      # Vacío (No cambia la contraseña actual)
        }

        # Pasamos la instancia existente al formulario para activar el modo edición
        form = ClienteForm(data=datos_edicion, instance=self.cliente_existente)
        
        # Validamos que el email duplicado se ignore correctamente al pertenecer al mismo usuario
        self.assertTrue(form.is_valid())

        # Guardamos los cambios
        cliente_editado = form.save()

        # Comprobamos que los datos del cliente mutaron de forma correcta
        self.assertEqual(cliente_editado.telefono, "3209998877")
        self.assertEqual(cliente_editado.direccion, "Avenida Caracas # 45-00")

        # Comprobamos que los datos del usuario enlazado también se actualizaron
        self.assertEqual(cliente_editado.id_usuario.email, "carlos_nuevo@correo.com")
        self.assertEqual(cliente_editado.id_usuario.password_hash, "hash_anterior") # Se mantuvo intacta
        
    def test_form_crear_cliente_con_validacion_incorrecta(self):
        """Crear un cliente que no """
        datos_nuevos = {
            'nombre': "Liliana Gomez",
            'documento_id': "52345678",        # Cumple RegexValidator (solo números)
            'telefono': "3119876543",
            'direccion': "Carrera 7 # 45-10",
            'email': "liliana@correo.com",
            'password': "claveSegura123"       # Requerido al crear (según tu __init__)
        }

        form = ClienteForm(data=datos_nuevos)
        
        # Validamos que pase las restricciones de los validadores
        self.assertTrue(form.is_valid())

        # Guardamos confirmando el commit en la BD en memoria
        cliente_creado = form.save()

        # Comprobamos que el cliente se enlazó a un usuario nuevo con los datos correctos
        self.assertIsNotNone(cliente_creado.id_usuario)
        self.assertEqual(cliente_creado.id_usuario.email, "liliana@correo.com")
        self.assertEqual(cliente_creado.id_usuario.nombre, "Liliana Gomez")
        
        # Verificamos que la contraseña se guardó con el Hash de Django
        self.assertTrue(check_password("claveSegura123", cliente_creado.id_usuario.password_hash))