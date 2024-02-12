from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.logar, name='login'),
    path('logout/', views.deslogar, name='logout'),
    path('pessoas/', views.pessoas, name='pessoas'),
    path('apagar-pessoa/<int:pessoa_id>', views.apagar_pessoa, name='apagar'),
    path('editar-pessoa/<int:pessoa_id>', views.editar_pessoa, name='editar')
]