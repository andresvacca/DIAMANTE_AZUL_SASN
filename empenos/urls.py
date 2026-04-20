from django.urls import path
from . import views

app_name = 'empenos'

urlpatterns = [
    path('', views.listar_empenos, name='listar'),
    path('crear/', views.crear_empeno, name='crear'),
    path('detalle/<int:id_empeno>/', views.detalle_empeno, name='detalle'),
    path('editar/<int:id_empeno>/', views.editar_empeno, name='editar'),
    path('eliminar/<int:id_empeno>/', views.eliminar_empeno, name='eliminar'),
    path('cuotas/<int:id_empeno>/', views.ver_cuotas, name='cuotas'),
    path('pagar/<int:id_cuota>/', views.registrar_pago, name='pagar'),
    # Asegúrate de que termine en .api_reporte_empenos
    path('api/reporte-prestamos/', views.api_reporte_empenos, name='api_reporte_empenos'),
    path('panel-reportes/', views.pagina_reportes, name='pagina_reportes'),
    path('empeno/<int:id_empeno>/abono/', views.registrar_abono, name='registrar_abono'),
]
