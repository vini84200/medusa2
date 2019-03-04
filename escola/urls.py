from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'escola'
urlpatterns = [
    path('', views.index, name='index'),
    path('turmas/', views.list_turmas, name='list-turmas'),
    path('turmas/add/', views.add_turma, name='add-turma'),
    path('turmas/edit/<int:pk>', views.edit_turma, name='edit-turma'),
    path('turmas/delete/<int:pk>', views.delete_turma, name='delete-turma'),
    path('turmas/populate/<int:pk>', views.populate_turma, name='populate-turma'),
    path('turmas/<int:pk_turma>/cargos', views.list_cargos , name='list-cargos'),
    path('turmas/<int:pk_turma>/cargos/add', views.add_cargo, name='add-cargo'),
    path('turmas/cargos/edit/<int:pk>', views.edit_cargo, name='edit-cargo'),
    path('turmas/cargos/delete/<int:pk>', views.delete_cargo, name='delete-cargo'),
    path('turma/<int:turma_pk>/alunos', views.list_alunos, name='list-alunos'),
    path('turma/<int:pk_turma>/alunos/add', views.add_aluno, name='add-aluno'),

]