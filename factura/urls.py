from django.urls import path
from . import views

app_name = 'factura'

urlpatterns = [
    path('',                                    views.listar_facturas,  name='listar'),
    path('crear/',                              views.crear_factura,    name='crear'),
    path('detalle/<int:id_factura>/',           views.detalle_factura,  name='detalle'),
]