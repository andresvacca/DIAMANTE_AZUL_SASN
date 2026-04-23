from django.urls import path
from . import views

app_name = 'cuotas'

urlpatterns = [
    path('', views.listar_cuotas, name='listar'),
    path('detalle/<int:id_cuota>/', views.detalle_cuota, name='detalle'),
]