from django.contrib import admin
from django.urls import path, include
from . import views # Importamos el views.py que acabamos de crear

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('articulos/', include('articulos.urls')),
    path('clientes/', include('clientes.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('empenos/', include('empenos.urls')),
    path('contratos/', include('contratos.urls')),
    path('factura/', include('factura.urls')),
    path('cuotas/', include('cuotas.urls')),
    path('compras/', include('compras.urls')),
    path('notificaciones/', include('notificaciones.urls')),
    path('cuadre/', include('cuadre.urls')),  # o la app donde pongas el cuadre
]