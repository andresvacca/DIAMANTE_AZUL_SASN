from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from . import views  # Importamos el views.py de tu proyecto principal

# Manejadores para las páginas de error personalizadas
handler404 = 'diamante_azul.views.error_404_view'
handler500 = 'diamante_azul.views.error_500_view'

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
    path('test-500/', views.error_500_view, name='test_500'),
]

# PARCHE PARA SERVIR ESTÁTICOS EN LOCAL CON DEBUG = FALSE
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
    ]