from django.db import migrations, models
import django.db.models.deletion


def seed_roles(apps, schema_editor):
    Rol = apps.get_model('usuarios', 'Rol')
    roles = [
        {'id_rol': 1, 'nombre': 'Administrador'},
        {'id_rol': 2, 'nombre': 'Empleado'},
        {'id_rol': 3, 'nombre': 'Cliente'},
    ]
    for r in roles:
        Rol.objects.get_or_create(id_rol=r['id_rol'], defaults={'nombre': r['nombre']})


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'usuarios_rol',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('id_rol', models.ForeignKey(
                    db_column='id_rol',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='usuarios.Rol',
                )),
            ],
            options={
                'db_table': 'usuarios_usuario',
            },
        ),
        migrations.RunPython(seed_roles, migrations.RunPython.noop),
    ]
