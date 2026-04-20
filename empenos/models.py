from django.db import models
from contratos.models import Contrato
from django.utils import timezone

class Empeno(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('En venta', 'En venta'),
        ('Vencido', 'Vencido'),
        ('Vendido', 'Vendido')
    ]

    id_empeno = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    id_articulo = models.ForeignKey('articulos.Articulos', on_delete=models.PROTECT)
    id_contrato = models.ForeignKey('contratos.Contrato', null=True, blank=True, on_delete=models.SET_NULL)
    num_cuotas = models.IntegerField(default=1)
    monto_prestado = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    monto_entregado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # 1. Guardamos el empeño primero para tener un ID generado
        super(Empeno, self).save(*args, **kwargs)

        # 2. Verificamos si ya tiene un contrato asignado para no duplicar
        if not self.id_contrato:
            # 3. Creamos el contrato usando los datos del empeño
            nuevo_contrato = Contrato.objects.create(
                id_cliente=self.id_cliente,
                id_articulo=self.id_articulo,
                id_empeno=self,
                fecha_contrato=self.fecha_inicio if hasattr(self, 'fecha_inicio') else timezone.now().date(),
                tipo_contrato='Normal',  # Valor por defecto
                estado_contrato='Disponible' # Valor por defecto
            )
            
            # 4. Vinculamos el contrato recién creado al empeño
            # Usamos update para evitar que vuelva a llamar al save y cree un bucle
            Empeno.objects.filter(pk=self.pk).update(id_contrato=nuevo_contrato)
            
    

    class Meta:
        db_table = 'empenos'

    def __str__(self):
        return f"Empeño {self.id_empeno} - {self.id_cliente}"


class Cuota(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Pagada', 'Pagada'),
        ('Vencida', 'Vencida'),
    ]

    id_cuota = models.AutoField(primary_key=True)
    id_empeno = models.ForeignKey(Empeno, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, null=True)
    numero_cuota = models.IntegerField()
    fecha_programada = models.DateField()
    capital = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mora = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    class Meta:
        db_table = 'cuotas'

    def __str__(self):
        return f"Cuota {self.numero_cuota} - Empeño {self.id_empeno_id}"


class Pago(models.Model):
    METODO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta', 'Tarjeta'),
    ]

    id_pago = models.AutoField(primary_key=True)
    id_cuota = models.ForeignKey(Cuota, on_delete=models.PROTECT)
    id_cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    id_contrato = models.ForeignKey('contratos.Contrato', null=True, on_delete=models.SET_NULL)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=15, choices=METODO_CHOICES, default='Efectivo')

    class Meta:
        db_table = 'pagos'

    def __str__(self):
        return f"Pago {self.id_pago} - ${self.monto}"