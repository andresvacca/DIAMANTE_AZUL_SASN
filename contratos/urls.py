from django.urls import path
from . import views

app_name = 'contratos'

urlpatterns = [
    path('', views.listar_contratos, name='listar'),
    path('crear/', views.crear_contrato, name='crear'),
    path('detalle/<int:id_contrato>/', views.detalle_contrato, name='detalle'),
    path('eliminar/<int:id_contrato>/', views.eliminar_contrato, name='eliminar'),  # ✅ agregado
    path('ajax/get-empeno/<int:pk>/', views.get_empeno_detalles, name='get_empeno_detalles'),
    path('empeno-datos/<int:id_empeno>/', views.datos_empeno_api, name='empeno_datos'),
    path('descargar/<int:id_contrato>/', views.descargar_pdf_contrato, name='descargar_pdf'),
    path('buscar-clientes/', views.buscar_clientes_api, name='buscar_clientes'),
    path('empenos-cliente/<int:id_cliente>/', views.empenos_sin_contrato_api, name='empenos_cliente'),
]