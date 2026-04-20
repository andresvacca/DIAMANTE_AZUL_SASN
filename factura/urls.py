from django.urls import path
from . import views

app_name = 'factura'

urlpatterns = [
    path('',                                    views.listar_facturas,  name='listar'),
    path('crear/',                              views.crear_factura,    name='crear'),
    path('detalle/<int:id_factura>/',           views.detalle_factura,  name='detalle'),
    path('editar/<int:id_factura>/',            views.editar_factura,   name='editar'),
    path('eliminar/<int:id_factura>/',          views.eliminar_factura, name='eliminar'),
    path('detalle/eliminar/<int:id_detalle>/',  views.eliminar_detalle, name='eliminar_detalle'),
]