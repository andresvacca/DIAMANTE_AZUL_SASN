from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore  # 💡 Forzamos el backend de BD
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from usuarios.models import Rol, Usuario
from clientes.models import Cliente
from articulos.models import Articulos
from factura.models import Factura, DetalleFactura
from factura.views import generar_factura_automatica

class FacturacionBaseTest(TransactionTestCase):
    """Clase base para inicializar usuarios, clientes y artículos de prueba."""
    
    def setUp(self):
        self.client = Client()
        
        # 1. Inicialización segura del Rol de Administrador
        self.rol_admin, _ = Rol.objects.get_or_create(
            id_rol=1, 
            defaults={'nombre': "Administrador"}
        )
        
        # 2. Creación del Usuario Administrador (Juan Guillermo)
        self.usuario_admin, _ = Usuario.objects.get_or_create(
            email="juanvacca@testin2.com",
            defaults={
                'nombre': "Juan Guillermo",
                'password_hash': make_password("password123"),
                'id_rol': self.rol_admin,
            }
        )
        
        # 🤝 Cliente de pruebas amarrado al administrador del sistema
        self.cliente = Cliente.objects.create(
            nombre="Andres Vacca",
            telefono="3001234567",
            direccion="Calle 26, Bogotá",
            id_usuario=self.usuario_admin
        )
        
        # 💎 Artículo en vitrina para ventas directas
        self.articulo = Articulos.objects.create(
            nombre="Reloj de Oro Rolex",
            descripcion="18 quilates usado",
            numero_serie="ROL-O-999",
            categoria="Oro",
            estado="Disponible",
            precio_sugerido_venta=12000000,
            quilataje="18"
        )
        
        self._autenticar_cliente()

    def _autenticar_cliente(self):
        """Crea la sesión de forma física en la BD y sincroniza el cliente del test."""
        # Creación en base de datos de pruebas mediante SessionStore
        s = SessionStore()
        
        # 🔑 INYECCIÓN REDUNDANTE DE SEGURIDAD:
        # Cubrimos todas las variantes posibles de nombres que tus decoradores de roles puedan validar
        s['usuario_id'] = self.usuario_admin.id_usuario
        s['id_usuario'] = self.usuario_admin.id_usuario
        s['usuario_rol'] = self.rol_admin.id_rol
        s['id_rol'] = self.rol_admin.id_rol
        s['rol_id'] = self.rol_admin.id_rol
        s['rol'] = self.rol_admin.nombre
        s['rol_nombre'] = self.rol_admin.nombre
        s['es_admin'] = True
        s['is_admin'] = True
        s.save()
        
        # 1. Enganchamos la cookie de sesión al cliente simulado para los headers HTTP
        self.client.cookies[settings.SESSION_COOKIE_NAME] = s.session_key
        
        # 2. Sincronizamos la sesión en memoria del objeto cliente usando dict() nativo
        session_cliente = self.client.session
        session_cliente.update(dict(s.items()))  # 💡 CORRECCIÓN: dict(s.items()) en lugar de to_dict()
        session_cliente.save()

class FacturaHelperMotorTest(FacturacionBaseTest):
    """Prueba el comportamiento del helper automatizado de auditoría general."""

    def test_generar_factura_automatica_cuota(self):
        """Mide que el motor registre correctamente un cobro de cuotas financieras."""
        factura = generar_factura_automatica(
            usuario=self.usuario_admin,
            cliente=self.cliente,
            tipo_movimiento='Cuota',
            monto=150000,
            id_empeno=45,
            descripcion="Pago de Intereses - Cuota #2"
        )
        
        self.assertEqual(factura.tipo_movimiento, 'Cuota')
        self.assertEqual(factura.total_neto, Decimal('150000.00'))
        self.assertEqual(factura.id_empeno_asociado, 45)
        
        detalle = DetalleFactura.objects.get(id_factura=factura)
        self.assertIsNone(detalle.id_articulo)
        self.assertEqual(detalle.descripcion_servicio, "Pago de Intereses - Cuota #2")


class FacturaVistasHTTPTest(FacturacionBaseTest):
    """Valida los controladores HTTP, inserciones manuales de vitrina y respuestas."""

    def test_vista_listar_facturas_renderiza(self):
        """Comprueba el renderizado de la tabla histórica de caja."""
        self._autenticar_cliente()
        url = reverse('factura:listar')
        response = self.client.get(url)
        
        # Diagnóstico claro si sigue devolviendo un redirect inesperado
        if response.status_code == 302:
            print(f"\n🚨 LISTAR redirigió a: {response.url}")
            
        self.assertEqual(response.status_code, 200)

    def test_crear_factura_venta_directa_exitosa(self):
            """Simula una venta directa de vitrina procesando arreglos dinámicos en el POST."""
            url = reverse('factura:crear')
            
            # Sincronizamos el payload añadiendo el campo obligatorio 'monto_pagado'
            payload = {
                'id_cliente': self.cliente.pk,
                'id_usuario': self.usuario_admin.pk,
                'metodo_pago': 'Transferencia',
                'tipo_movimiento': 'Venta',
                'articulo': [self.articulo.pk],
                'articulo[]': [self.articulo.pk],
                'precio': ['12000000.00'],
                'precio[]': ['12000000.00'],
                'cantidad': ['1'],
                'cantidad[]': ['1'],
                'total_neto': '12000000.00',
                'monto_pagado': '12000000.00',  # 💡 ¡SOLUCIÓN! El campo que el formulario estaba pidiendo a gritos
            }
            
            self._autenticar_cliente()
            response = self.client.post(url, payload, follow=False)
            
            if response.status_code == 200 and hasattr(response, 'context') and response.context and 'form' in response.context:
                print("\n🚨 ERRORES DEL FORMULARIO EN EL TEST:", response.context['form'].errors.as_json())
            
            self.assertIn(response.status_code, [200, 302], f"La vista respondió con un código inesperado: {response.status_code}")
            
            # Ahora sí debería encontrar el registro guardado con éxito
            nueva_factura = Factura.objects.filter(id_cliente=self.cliente).first()
            self.assertIsNotNone(nueva_factura, "La factura no se guardó en la base de datos. El formulario fue rechazado.")