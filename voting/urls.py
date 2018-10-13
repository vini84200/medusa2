from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'voting'
urlpatterns = [
    path('presenca/tela/', views.presenca_painel, name='PresecaPainel'),
    path('home/', views.loged_home, name='home'),
    path('presenca/registrar/<int:sessao>', views.registrar_presenca, name='registrarPresenca'),
]
