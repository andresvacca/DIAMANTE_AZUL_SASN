from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from usuarios.models import Rol, Usuario
from clientes.models import Cliente
from articulos.models import Articulos
from factura.models import Factura, DetalleFactura
from factura.views import generar_factura_automatica


class FacturacionBaseTest(TransactionTestCase):
    """Clase base: inicializa usuarios, clientes y artículos de prueba."""

    def setUp(self):
        self.client = Client()

        self.rol_admin, _ = Rol.objects.get_or_create(
            id_rol=1,
            defaults={'nombre': "Administrador"}
        )

        self.usuario_admin, _ = Usuario.objects.get_or_create(
            email="juanvacca@testin2.com",
            defaults={
                'nombre': "Juan Guillermo",
                'password_hash': make_password("password123"),
                'id_rol': self.rol_admin,
            }
        )

        self.cliente = Cliente.objects.create(
            nombre="Andres Vacca",
            telefono="3001234567",
            direccion="Calle 26, Bogotá",
            id_usuario=self.usuario_admin
        )

        self.articulo = Articulos.objects.create(
            nombre="Reloj de Oro Rolex",
            descripcion="18 quilates usado",
            numero_serie="ROL-O-999",
            categoria="Oro",
            estado="Disponible",
            precio_sugerido_venta=12000000,
            quilataje="18"
        )

        # Una sola inyección de sesión al final del setUp
        self._autenticar_cliente()

    def _autenticar_cliente(self):
        """
        Crea una sesión física en la BD con la clave exacta que leen
        _requiere_admin y _requiere_empleado: 'usuario_rol_id'.
        """
        s = SessionStore()
        s['usuario_id']     = self.usuario_admin.id_usuario
        s['usuario_rol_id'] = self.rol_admin.id_rol   # ← CLAVE QUE USAN LOS DECORADORES
        s.save()

        # Apuntar la cookie del cliente a esta sesión
        self.client.cookies[settings.SESSION_COOKIE_NAME] = s.session_key


class FacturaHelperMotorTest(FacturacionBaseTest):
    """Prueba el helper automatizado de auditoría."""

    def test_generar_factura_automatica_cuota(self):
        """El motor debe registrar correctamente un cobro de cuota financiera."""
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
    """Valida los controladores HTTP de facturación."""

    def test_vista_listar_facturas_renderiza(self):
        """La tabla histórica de caja debe responder 200."""
        response = self.client.get(reverse('factura:listar'))
        self.assertEqual(response.status_code, 200)

    def test_crear_factura_venta_directa_exitosa(self):
        """Venta directa de vitrina: debe guardar la factura en BD."""
        payload = {
            'id_cliente':   self.cliente.pk,
            'id_usuario':   self.usuario_admin.pk,
            'metodo_pago':  'Transferencia',
            'monto_pagado': '12000000.00',
            'articulo[]':   [str(self.articulo.pk)],
            'precio[]':     ['12000000.00'],
        }

        response = self.client.post(reverse('factura:crear'), payload, follow=False)

        # Diagnóstico detallado si el form rechaza el POST
        if response.status_code == 200 \
                and hasattr(response, 'context') \
                and response.context \
                and 'form' in response.context:
            print("\n🚨 ERRORES DEL FORMULARIO:", response.context['form'].errors.as_json())

        self.assertIn(
            response.status_code, [200, 302],
            f"Código inesperado: {response.status_code}"
        )

        nueva_factura = Factura.objects.filter(id_cliente=self.cliente).first()
        self.assertIsNotNone(
            nueva_factura,
            "La factura no se guardó. El formulario fue rechazado."
        )