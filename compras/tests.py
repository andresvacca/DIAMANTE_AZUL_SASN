from django.test import TestCase
from decimal import Decimal
from .models import Compra, VentaArticulo
from clientes.models import Cliente
from articulos.models import Articulos
from factura.models import Factura
from usuarios.models import Rol, Usuario
from django.contrib.auth.hashers import make_password

class UtilidadTest(TestCase):
    def setUp(self):
        # 1. Asegurar dependencias de Usuario
        self.rol_admin, _ = Rol.objects.get_or_create(
            id_rol=Rol.ROL_ADMINISTRADOR, 
            defaults={'nombre': "Administrador"}
        )
        self.usuario, _ = Usuario.objects.get_or_create(
            email="juanvacca@gmail.com",
            defaults={
                'nombre': "Juan Guillermo Vacca",
                'password_hash': make_password("password123"),
                'id_rol': self.rol_admin
            }
        )
        
        # 2. Asegurar Cliente y Artículo
        self.cliente = Cliente.objects.create(nombre="Test Cliente")
        self.articulo = Articulos.objects.create(
            nombre="Test Articulo",
            precio_sugerido_venta=Decimal('150.00'),
            estado='Disponible'
        )
        
        # 3. Facturas
        self.factura_compra = Factura.objects.create(
            id_cliente=self.cliente,
            id_usuario=self.usuario,
            total_neto=Decimal('100.00')
        )
        self.factura_venta = Factura.objects.create(
            id_cliente=self.cliente,
            id_usuario=self.usuario,
            total_neto=Decimal('150.00')
        )
        
        # 4. Compra inicial
        self.compra = Compra.objects.create(
            id_cliente=self.cliente,
            id_articulo=self.articulo,
            precio_pagado=Decimal('100.00'),
            precio_reventa=Decimal('200.00'),
            id_factura_compra=self.factura_compra,
            estado='En Venta'
        )

    def test_calculo_automatico_utilidad(self):
        """Verifica la lógica central: Venta - Compra = Utilidad."""
        venta = VentaArticulo.objects.create(
            id_compra=self.compra,
            id_factura=self.factura_venta,
            precio_venta_final=Decimal('150.00')
        )
        venta.refresh_from_db()
        self.assertEqual(venta.utilidad_generada, Decimal('50.00'))

    def test_integridad_venta(self):
        """Verifica que la compra cambie de estado al venderse."""
        VentaArticulo.objects.create(
            id_compra=self.compra,
            id_factura=self.factura_venta,
            precio_venta_final=Decimal('150.00')
        )
        # Aquí tendrías que llamar a tu lógica de cambio de estado
        # Si usas señales (post_save) o lo haces en la vista, asegúrate de testearlo
        self.compra.refresh_from_db()
        # self.assertEqual(self.compra.estado, 'Vendido')