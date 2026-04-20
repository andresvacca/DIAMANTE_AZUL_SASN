from django.urls import path
from . import views

app_name = 'cuotas'

urlpatterns = [
    path('', views.listar_cuotas, name='listar'),
]