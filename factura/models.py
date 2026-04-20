from django.db import models

METODO_CHOICES = [
    ('Efectivo', 'Efectivo'),
    ('Transferencia', 'Transferencia'),
    ('Tarjeta', 'Tarjeta'),
]

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=15, choices=METODO_CHOICES, default='Efectivo')

    class Meta:
        db_table = 'facturas'

    def __str__(self):
        return f"Factura {self.id_factura} - {self.id_cliente}"


class DetalleFactura(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    id_articulo = models.ForeignKey('articulos.Articulos', on_delete=models.PROTECT)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_factura'

    def __str__(self):
        return f"Detalle {self.id_detalle} - Factura {self.id_factura_id}"