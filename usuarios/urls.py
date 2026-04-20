from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # CRUD (admin)
    path('', views.listar_usuarios, name='listar'),
    path('crear/', views.crear_usuario, name='crear'),
    path('editar/<int:id_usuario>/', views.editar_usuario, name='editar'),
    path('eliminar/<int:id_usuario>/', views.eliminar_usuario, name='eliminar'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/<int:id_usuario>/', views.perfil_detalle_view, name='perfil_detalle'),
]

