from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path('', views.listar_compras, name='listar'),
    path('crear/', views.crear_compra, name='crear'),
    path('detalle/<int:id_compra>/', views.detalle_compra, name='detalle'),
    path('venta/<int:id_compra>/', views.registrar_venta, name='venta'),
    path('eliminar/<int:id_compra>/', views.eliminar_compra, name='eliminar'),
]