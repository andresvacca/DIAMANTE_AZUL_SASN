from django.db import models


class Rol(models.Model):
    ROL_ADMINISTRADOR = 1
    ROL_EMPLEADO = 2
    ROL_CLIENTE = 3

    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'usuarios_rol'


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    password_hash = models.CharField(max_length=255)
    id_rol = models.ForeignKey(
        Rol, on_delete=models.SET_NULL, null=True, db_column='id_rol'
    )

    def __str__(self):
        return self.nombre

    def get_rol_nombre(self):
        return self.id_rol.nombre if self.id_rol else 'Sin rol'

    def es_administrador(self):
        return self.id_rol_id == Rol.ROL_ADMINISTRADOR

    def es_empleado(self):
        return self.id_rol_id == Rol.ROL_EMPLEADO

    def es_cliente(self):
        return self.id_rol_id == Rol.ROL_CLIENTE

    class Meta:
        db_table = 'usuarios_usuario'
