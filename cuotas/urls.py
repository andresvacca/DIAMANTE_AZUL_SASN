from django.urls import path
from . import views
from empenos import views

app_name = 'cuotas'

urlpatterns = [
    path('', views.listar_cuotas, name='listar'),
    path('detalle/<int:id_empeno>/', views.ver_cuotas, name='detalle'),
]