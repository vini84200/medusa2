from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'escola'
urlpatterns = [
    path('', views.index, name='index'),
    path('turmas/add/', views.add_turma, name='add-turma'),
    path('turmas/', views.list_turmas, name='list-turmas')
]