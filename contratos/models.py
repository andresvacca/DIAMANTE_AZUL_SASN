# contratos/models.py
from django.db import models


class Contrato(models.Model):
    TIPO_CHOICES = [
        ('Normal', 'Normal'),
        ('Plazo Maximo', 'Plazo Maximo'),
        ('Contrato sobre Oro', 'Contrato sobre Oro'),
        ('Oro Maximo', 'Oro Maximo'),
    ]
    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Vencido', 'Vencido'),
        ('Retirado', 'Retirado'),
    ]

    id_contrato = models.AutoField(primary_key=True)
    id_pago = models.ForeignKey('empenos.Pago', null=True, on_delete=models.SET_NULL)
    id_cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    id_articulo = models.ForeignKey('articulos.Articulos', on_delete=models.PROTECT)
    id_cuota = models.ForeignKey('empenos.Cuota', null=True, on_delete=models.SET_NULL)
    id_factura = models.ForeignKey('factura.Factura', null=True, on_delete=models.SET_NULL)
    id_empeno = models.ForeignKey('empenos.Empeno', null=True, on_delete=models.SET_NULL)
    fecha_contrato = models.DateField()
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CHOICES, null=True)
    estado_contrato = models.CharField(max_length=10, choices=ESTADO_CHOICES, null=True)

    class Meta:
        db_table = 'contrato'

    def __str__(self):
        return f"Contrato {self.id_contrato} - {self.tipo_contrato}"