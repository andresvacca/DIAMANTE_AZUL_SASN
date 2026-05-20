from django.db import models

METODO_CHOICES = [
    ('Efectivo', 'Efectivo'),
    ('Transferencia', 'Transferencia'),
    ('Tarjeta', 'Tarjeta'),
]

# 📝 NUEVOS TIPOS DE MOVIMIENTO PARA AUDITORÍA
TIPO_MOVIMIENTO_CHOICES = [
    ('Venta', 'Venta Directa de Artículo'),
    ('Desembolso', 'Desembolso de Empeño (Salida de Caja)'),
    ('Cuota', 'Pago de Cuota / Interés (Entrada de Caja)'),
    ('Abono', 'Abono a Capital (Entrada de Caja)'),
    ('Retiro', 'Liquidación y Retiro de Artículo (Entrada de Caja)'),
]

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.PROTECT)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=15, choices=METODO_CHOICES, default='Efectivo')
    
    # 🌟 NUEVOS CAMPOS CLAVE
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES, default='Venta')
    # Guardamos el ID del empeño como entero o relación genérica para no generar dependencias circulares duras si están en apps separadas
    id_empeno_asociado = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'facturas'

    def __str__(self):
        return f"{self.tipo_movimiento} #{self.id_factura} - {self.id_cliente}"


class DetalleFactura(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    # Volvemos null=True el artículo, porque un pago de cuota o interés no vende el artículo, solo factura el servicio financiero
    id_articulo = models.ForeignKey('articulos.Articulos', on_delete=models.PROTECT, null=True, blank=True)
    # Descripción textual obligatoria para cuando no es un artículo físico (ej: "Pago de Interés - Cuota #2")
    descripcion_servicio = models.CharField(max_length=255, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalles_factura'