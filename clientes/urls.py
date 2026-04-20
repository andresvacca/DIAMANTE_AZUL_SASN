from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.listar_clientes, name='listar'),
    path('crear/', views.crear_cliente, name='crear'),
    path('editar/<int:id_cliente>/', views.editar_cliente, name='editar'),
    path('eliminar/<int:id_cliente>/', views.eliminar_cliente, name='eliminar'),
    path('crear-ajax/', views.crear_cliente_ajax, name='crear_ajax'),
    path('municipios/', views.municipios_api, name='municipios'),
]
