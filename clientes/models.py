from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import usuarios

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    documento_id = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True)
    direccion = models.TextField(null=True)
    lugar_expedicion = models.CharField(max_length=100, null=True, blank=True)
    departamento_expedicion = models.CharField(max_length=100, null=True, blank=True)
    id_usuario = models.OneToOneField(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario'
    )
    

    class Meta:
        db_table = 'clientes'

    def __str__(self):
        return self.nombre
    


@receiver(pre_delete, sender=Cliente)
def eliminar_usuario_al_eliminar_cliente(sender, instance, **kwargs):
    if instance.id_usuario:
        instance.id_usuario.delete()