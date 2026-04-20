from django.urls import path
from . import views
app_name = 'cuadre_caja'
urlpatterns = [path('', views.cuadre_caja, name='index')]