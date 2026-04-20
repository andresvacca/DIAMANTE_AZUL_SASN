from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('',                          views.listar_notificaciones, name='listar'),
    path('leida/<int:id_notificacion>/', views.marcar_leida,       name='marcar_leida'),
    path('conteo/',                   views.conteo_no_leidas,      name='conteo'),
]