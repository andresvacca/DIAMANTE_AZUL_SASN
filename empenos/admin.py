from django.contrib import admin
from .models import Empeno, Cuota # Importa tus modelos

admin.site.register(Empeno)


@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    # Esto creará columnas para ver el ID del empeño, el número y el estado
    list_display = ('id_empeno', 'numero_cuota', 'estado')
    # Esto añade un buscador por el ID del empeño
    search_fields = ('id_empeno__id_empeno',)