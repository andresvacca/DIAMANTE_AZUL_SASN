from django.db import models


class Compra(models.Model):
    ESTADO_CHOICES = [
        ('En Venta', 'En Venta'),
        ('Vendido', 'Vendido'),
    ]

    id_compra = models.AutoField(primary_key=True)
    fecha_compra = models.DateField(auto_now_add=True)
    id_cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='compras'
    )
    id_articulo = models.ForeignKey(
        'articulos.Articulos',
        on_delete=models.PROTECT,
        related_name='compras'
    )
    precio_pagado = models.DecimalField(max_digits=12, decimal_places=2)
    precio_reventa = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='En Venta')
    id_factura_compra = models.OneToOneField(  # factura al comprar
        'factura.Factura',
        on_delete=models.PROTECT,
        related_name='compra_origen',
        null=True
    )
    id_factura_venta = models.OneToOneField(   # factura al revender
        'factura.Factura',
        on_delete=models.SET_NULL,
        related_name='compra_venta',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'compra'

    def __str__(self):
        return f"Compra {self.id_compra} — {self.id_articulo}"


class VentaArticulo(models.Model):
    id_venta = models.AutoField(primary_key=True)
    
    # Relación con la Compra (para saber qué artículo se vendió)
    # Usamos ForeignKey para que un artículo pueda tener historial si regresa al sistema
    id_compra = models.ForeignKey('compras.Compra', on_delete=models.PROTECT, related_name='ventas')
    
    # Relación con la Factura (el documento contable)
    id_factura = models.OneToOneField('factura.Factura', on_delete=models.CASCADE, related_name='detalle_venta')
    
    # Datos específicos de la salida
    precio_venta_final = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Mantenemos este como el "almacén" del cálculo para poder hacer SUM y AVG en SQL
    utilidad_generada = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        editable=False, # Evita que alguien lo edite manualmente en el Admin
        null=True
    )

    def save(self, *args, **kwargs):
        # Lógica centralizada: El cálculo solo existe aquí
        if self.precio_venta_final and self.id_compra:
            self.utilidad_generada = self.precio_venta_final - self.id_compra.precio_pagado
        super().save(*args, **kwargs)

    # Si REALMENTE necesitas una property para algo extra (ej. formato), 
    # úsala solo para visualización, no para el cálculo base.
    @property
    def utilidad_formateada(self):
        return f"$ {self.utilidad_generada}"