from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.logar, name='login'),
    path('logout/', views.deslogar, name='logout'),
    path('pessoas/', views.pessoas, name='pessoas'),
    path('cad-pessoa/', views.cad_pessoa, name='cadastro'),
    path('apagar-pessoa/<int:pessoa_id>', views.apagar_pessoa, name='apagar'),
    path('editar-pessoa/<int:pessoa_id>', views.editar_pessoa, name='editar'),
    path('relatorios/', views.relatorios, name='relatorios')
]