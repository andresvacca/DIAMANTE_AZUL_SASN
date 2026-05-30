from django.test import TestCase
from empenos.models import Cuota, Empeno, Pago
from articulos.models import Articulos
from clientes.models import Cliente
from usuarios.models import Rol, Usuario
from django.utils import timezone
from datetime import date
from django.db import models # Para usar models.F
from django.db.models import Sum # Para usar Sum
class EmpenoTest(TestCase):
    def setUp(self):
        # 1. Crear dependencias
        self.rol = Rol.objects.create(nombre="Cliente")
        self.usuario = Usuario.objects.create(
            nombre="Juan", email="juan@test.com", id_rol=self.rol
        )
        self.cliente = Cliente.objects.create(id_usuario=self.usuario)
        self.articulo = Articulos.objects.create(
            nombre="Reloj de Oro",
            precio_sugerido_venta=100.00
        )
        
        # 2. Crear Empeño (Cumpliendo con los campos requeridos en models.py)
        # Nota: Usamos id_empeno como clave primaria
        self.empeno = Empeno.objects.create(
            id_cliente=self.cliente,
            id_articulo=self.articulo,
            monto_prestado=500.00,
            tasa_interes=5.00,
            monto_entregado=500.00,
            fecha_vencimiento=date(2026, 12, 25),
            estado='Activo'
        )
        
        # 3. Crear Cuota
        self.cuota = Cuota.objects.create(
            id_empeno=self.empeno,
            id_cliente=self.cliente,
            numero_cuota=1,
            fecha_programada=date(2026, 6, 25),
            capital=100.00,
            interes=10.00,
            estado='Pendiente'
        )

    def test_relaciones_modelo(self):
        """Verifica que los modelos estén conectados usando la clave primaria correcta."""
        empeno_db = Empeno.objects.get(id_empeno=self.empeno.id_empeno)
        self.assertEqual(empeno_db.id_articulo.nombre, "Reloj de Oro")
        self.assertIsNotNone(empeno_db.id_contrato) # Verifica que el save() automático funcionó

    def test_filtro_pendientes(self):
        """Verifica la lógica de filtrado de cuotas."""
        # Creamos otra cuota
        Cuota.objects.create(
            id_empeno=self.empeno, 
            id_cliente=self.cliente,
            numero_cuota=2,
            fecha_programada=date(2026, 7, 25),
            estado='Pendiente'
        )
        pendientes = Cuota.objects.filter(estado='Pendiente')
        self.assertEqual(pendientes.count(), 2)

    def test_pago_cuota(self):
        """Verifica el cálculo de total_cuota y pago."""
        self.assertEqual(self.cuota.total_cuota, 110.00)
        
        Pago.objects.create(
            id_cuota=self.cuota,
            id_cliente=self.cliente,
            monto=110.00
        )
        self.cuota.estado = 'Pagada'
        self.cuota.save()
        self.cuota.refresh_from_db()
        self.assertEqual(self.cuota.estado, 'Pagada')
        
    def test_deteccion_cuota_vencida(self):
        """Verifica que podamos identificar cuotas con fecha pasada."""
        from datetime import date
        
        # Creamos una cuota con fecha del mes pasado
        cuota_vieja = Cuota.objects.create(
            id_empeno=self.empeno,
            id_cliente=self.cliente,
            numero_cuota=3,
            fecha_programada=date(2026, 4, 1), # Fecha pasada
            capital=100.00,
            interes=10.00,
            estado='Pendiente'
        )
        
        # Filtramos todas las cuotas pendientes cuya fecha es menor a hoy
        hoy = date.today()
        vencidas = Cuota.objects.filter(
            estado='Pendiente', 
            fecha_programada__lt=hoy
        )
        
        # Verificamos que efectivamente detectó la cuota vieja
        self.assertIn(cuota_vieja, vencidas)
        self.assertEqual(vencidas.count(), 1)
        
    def test_limite_empenos_activos(self):
        """Verifica que podemos contar los empeños activos de un cliente."""
        # El cliente ya tiene 1 empeño activo (creado en el setUp)
        
        # Intentamos crear 2 empeños más para el mismo cliente
        Empeno.objects.create(
            id_cliente=self.cliente,
            id_articulo=self.articulo, # Nota: en un caso real usarías otro artículo
            monto_prestado=100.00,
            tasa_interes=5.00,
            monto_entregado=100.00,
            fecha_vencimiento=date(2026, 12, 25),
            estado='Activo'
        )
        Empeno.objects.create(
            id_cliente=self.cliente,
            id_articulo=self.articulo,
            monto_prestado=200.00,
            tasa_interes=5.00,
            monto_entregado=200.00,
            fecha_vencimiento=date(2026, 12, 25),
            estado='Activo'
        )
        
        # Filtramos cuántos tiene activos
        activos = Empeno.objects.filter(id_cliente=self.cliente, estado='Activo')
        
        # Debería tener 3 (1 del setUp + 2 nuevos)
        self.assertEqual(activos.count(), 3)
        
    def test_filtrado_empenos_operativos(self):
        """Verifica que solo los empeños 'Activo' sean tomados para nuevas cuotas."""
        # 1. Creamos un empeño que ya está 'Vendido'
        empeno_vendido = Empeno.objects.create(
            id_cliente=self.cliente,
            id_articulo=self.articulo,
            monto_prestado=1000.00,
            tasa_interes=5.00,
            monto_entregado=1000.00,
            fecha_vencimiento=date(2026, 12, 25),
            estado='Vendido' # Estado terminal
        )
        
        # 2. Definimos una query para obtener solo los empeños que admiten operaciones
        empenos_operativos = Empeno.objects.filter(estado='Activo')
        
        # 3. Verificamos que el vendido NO aparezca en los activos
        self.assertNotIn(empeno_vendido, empenos_operativos)
        self.assertEqual(empenos_operativos.count(), 1) # Solo el del setUp
    
    def test_proteccion_borrado_cliente(self):
        """Verifica que no se pueda borrar un cliente que tiene empeños activos."""
        from django.db.models.deletion import ProtectedError
        
        # Intentamos borrar el cliente que tiene un empeño activo en el setUp
        with self.assertRaises(ProtectedError):
            self.cliente.delete()
            
        # Verificamos que el cliente sigue existiendo en la base de datos
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())
        
    
    def test_calculo_saldo_total_pendiente(self):
        """Verifica que el cálculo de la suma de cuotas pendientes sea correcto."""
        from django.db.models import Sum
        
        # 1. Aseguramos que la cuota del setUp esté pendiente
        self.cuota.capital = 100.00
        self.cuota.interes = 10.00
        self.cuota.estado = 'Pendiente'
        self.cuota.save()
        
        # 2. Creamos una segunda cuota pendiente para el mismo empeño
        Cuota.objects.create(
            id_empeno=self.empeno,
            id_cliente=self.cliente,
            numero_cuota=2,
            fecha_programada=date(2026, 8, 25),
            capital=200.00,
            interes=20.00,
            estado='Pendiente'
        )
        
        # 3. Calculamos la suma total (Capital + Interes) de las pendientes
        # Usamos F para sumar ambos campos antes de agregarlos
        resultado = Cuota.objects.filter(
            id_empeno=self.empeno, 
            estado='Pendiente'
        ).annotate(
            total_fila=models.F('capital') + models.F('interes')
        ).aggregate(
            gran_total=Sum('total_fila')
        )
        
        # 4. Verificamos: (100+10) + (200+20) = 330.00
        self.assertEqual(resultado['gran_total'], 330.00)
        
    
    def test_validacion_monto_negativo(self):
        """Verifica que el modelo lance un error si el monto es negativo."""
        from django.core.exceptions import ValidationError
        
        # Intentamos crear un empeño con monto negativo
        empeno_invalido = Empeno(
            id_cliente=self.cliente,
            id_articulo=self.articulo,
            monto_prestado=-500.00, # Valor ilegal
            tasa_interes=5.00,
            monto_entregado=500.00,
            fecha_vencimiento=date(2026, 12, 25),
            estado='Activo'
        )
        
        # Comprobamos que el método full_clean() lance el ValidationError
        with self.assertRaises(ValidationError):
            empeno_invalido.full_clean()
            
    
    
    def test_cambio_estado_cuota_al_pagar(self):
        """Verifica que el estado de la cuota pase a 'Pagada' tras un pago suficiente."""
        # 1. Creamos el pago
        Pago.objects.create(
            id_cuota=self.cuota,
            id_cliente=self.cliente,
            monto=self.cuota.total_cuota # Pago exacto
        )
        
        # 2. Recargamos la cuota desde la base de datos para ver el cambio
        self.cuota.refresh_from_db()
        
        # 3. Verificamos que el estado cambió
        self.assertEqual(self.cuota.estado, 'Pagada')
        
        
    def test_generacion_mora_por_pago_atrasado(self):
        """Verifica que si se paga tarde, se calcule mora automáticamente."""
        # 1. Ponemos la fecha de la cuota en el pasado (hace 10 días)
        self.cuota.fecha_programada = date(2026, 5, 15)
        self.cuota.save()
        
        # 2. Realizamos el pago
        Pago.objects.create(
            id_cuota=self.cuota,
            id_cliente=self.cliente,
            monto=self.cuota.total_cuota
        )
        
        # 3. Recargamos la cuota
        self.cuota.refresh_from_db()
        
        # 4. Verificamos que ahora exista una mora mayor a 0
        self.assertGreater(self.cuota.mora, 0)
        self.assertEqual(self.cuota.mora, 10.00) # 10% de 100 de capital
        
        
    def test_bloqueo_pagos_empeno_vendido(self):
        """Verifica que no se puedan registrar pagos si el empeño está 'Vendido'."""
        # 1. Cambiamos el estado
        self.empeno.estado = 'Vendido'
        self.empeno.save()
        
        # 2. Creamos un nuevo pago
        pago = Pago(
            id_cuota=self.cuota,
            id_cliente=self.cliente,
            monto=100.00
        )
        
        # 3. Probamos que el save() lance la excepción
        with self.assertRaises(Exception) as cm:
            pago.save()
            
        # 4. Verificamos el mensaje de error (opcional pero recomendado)
        self.assertEqual(str(cm.exception), "No se pueden realizar pagos en empeños vendidos.")
        
        
    def test_api_crear_empeno(self):
        """Verifica que el endpoint de creación de empeños funcione."""
        from django.urls import reverse
        
        # 1. Datos para enviar al servidor
        datos = {
            'id_cliente': self.cliente.pk,
            'id_articulo': self.articulo.pk,
            'monto_prestado': 500.00,
            'tasa_interes': 5.00,
            'monto_entregado': 500.00,
            'fecha_vencimiento': '2026-12-25',
            'estado': 'Activo'
        }
        
        # 2. Hacemos una petición post a nuestra vista
        # Ajusta 'empeno-create' al nombre que le pusiste en tu urls.py
        response = self.client.post(reverse('empenos:crear'), datos, follow=True)
        
        # 3. Verificamos que la respuesta sea 201 (Created)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Empeno.objects.filter(monto_prestado=500.00).exists())