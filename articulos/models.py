from django.db import models

# Create your models here.
class Articulos(models.Model):
    CATEGORIA_CHOICES = [
        ('Bicicletas', 'Bicicletas'), ('Neveras', 'Neveras'),('Oro', 'Oro'), ('Plata', 'Plata'),('Ollas','Ollas'),('VideoJuegos','Videojuegos'),('Relojes','Relojes'),('Computadores','Computadores'),('Otro','Otro')
    ]
    ESTADO_CHOICES = [
        ('En venta','En venta'), ('Empeñado','Empeñado'),
        ('Vendido','Vendido'), ('Vencido','Vencido'),
    ]
    QUILATAJE_CHOICES = [('18','18'),('16','16'),('14','14'),('10','10'),('0','0')]

    id_articulo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True)
    numero_serie = models.CharField(max_length=50, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Disponible')
    precio_sugerido_venta = models.DecimalField(max_digits=10, decimal_places=2)
    quilataje = models.CharField(max_length=3, choices=QUILATAJE_CHOICES, null=True)

    class Meta:
        db_table = 'articulos'

    def __str__(self):
        return self.nombre
