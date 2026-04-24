from django.urls import path
from . import views
from empenos import views

app_name = 'cuotas'

urlpatterns = [
    path('', views.listar_cuotas, name='listar'),
    path('detalle/<int:id_empeno>/', views.ver_cuotas, name='detalle'),
    path('pagar_multiples/<int:id_empeno>/', views.pagar_multiples, name='pagar_multiples'),
    path('agregar-cuota/<int:id_empeno>/', views.agregar_cuota_manual, name='agregar_cuota'),
]