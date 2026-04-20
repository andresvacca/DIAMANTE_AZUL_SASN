from django.urls import path
from . import views

app_name = 'articulos'

urlpatterns = [
    path('', views.listar_articulos, name='listar'),
    path('crear/', views.crear_articulo, name='crear'),
    path('editar/<int:id_articulo>/', views.editar_articulo, name='editar'),
    path('eliminar/<int:id_articulo>/', views.eliminar_articulo, name='eliminar'),
    path('crear-ajax/', views.crear_articulo_ajax, name='crear_ajax'),
    path('carga-masiva/', views.carga_masiva_articulos, name='carga_masiva'),
    path('carga-masiva/ejemplo/', views.descargar_csv_ejemplo, name='descargar_csv_ejemplo'),
    path('articulo-detalles/<int:id_articulo>/', views.detalle_articulo, name='detalle'),
    path('exportar-excel/', views.exportar_articulos_excel, name='exportar_excel'),
    path('exportar-pdf/', views.exportar_articulos_pdf, name='exportar_pdf'),
]
