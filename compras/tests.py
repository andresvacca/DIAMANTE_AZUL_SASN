from django.test import TestCase
from decimal import Decimal
from .models import Compra, VentaArticulo
# Asegúrate de importar tus modelos de clientes, articulos y factura

class UtilidadTest(TestCase):
    def setUp(self):
        # 1. Creamos los objetos necesarios para la compra
        # (Asumiendo que tienes una forma rápida de crear estos objetos)
        self.compra = Compra.objects.create(
            id_cliente=self.cliente,
            id_articulo=self.articulo,
            precio_pagado=Decimal('100.00'),
            precio_reventa=Decimal('200.00'),
            estado='En Venta'
        )

    def test_calculo_automatico_utilidad(self):
        """Verifica que la utilidad se calcule sola al guardar la venta."""
        # 2. Creamos la venta asociada a la compra
        venta = VentaArticulo.objects.create(
            id_compra=self.compra,
            id_factura=self.factura_venta,
            precio_venta_final=Decimal('150.00')
        )
        
        # 3. Recargamos de la BD para asegurar que el modelo guardó el cálculo
        venta.refresh_from_db()
        
        # 4. Verificamos: 150 (venta) - 100 (compra) = 50 (utilidad)
        expected_utilidad = Decimal('50.00')
        self.assertEqual(venta.utilidad_generada, expected_utilidad)