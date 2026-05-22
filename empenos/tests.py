from django.test import TestCase
from django.utils import timezone
from .models import Cuota, Empeno, Pago, Cliente, Rol
from .views import pagar_multiples # O donde viva tu lógica

class PagoMultipleTest(TestCase):
    def setUp(self):
        # 1. Creamos datos mínimos necesarios (Jerarquía)
        self.rol = Rol.objects.create(nombre="Cliente")
        self.cliente = Cliente.objects.create(nombre="Juan", id_usuario=1, rol=self.rol)
        self.empeno = Empeno.objects.create(id_cliente=self.cliente, estado='Pendiente')
        self.cuota = Cuota.objects.create(
            id_empeno=self.empeno, 
            id_cliente=self.cliente, 
            capital=100, interes=10, mora=0, 
            estado='Pendiente'
        )

    def test_proceso_pago_exitoso(self):
        # Simulamos que seleccionamos la cuota
        # (Llamamos a la lógica que calcula y guarda)
        
        # Aquí probarías tu lógica de pago:
        total_pago = self.cuota.capital + self.cuota.interes + self.cuota.mora
        
        # Ejecutamos el registro del pago
        Pago.objects.create(
            id_cuota=self.cuota,
            id_cliente=self.cliente,
            monto=total_pago,
            metodo_pago='Efectivo'
        )
        self.cuota.estado = 'Pagada'
        self.cuota.save()
        
        # Assert: Verificamos que todo cambió como esperábamos
        self.cuota.refresh_from_db() # Recargamos para ver el cambio real en la BD
        self.assertEqual(self.cuota.estado, 'Pagada')
        self.assertTrue(Pago.objects.filter(id_cuota=self.cuota).exists())
        
    def test_filtro_por_estado_pendiente(self):
        # Creamos una cuota pendiente y una pagada
        Cuota.objects.create(..., estado='Pendiente')
        Cuota.objects.create(..., estado='Pagada')
        
        # Aquí probarías si el query que hiciste en la vista filtra bien
        pendientes = Cuota.objects.filter(estado='Pendiente')
        self.assertEqual(pendientes.count(), 1)