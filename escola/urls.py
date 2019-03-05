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
    path('turmas/aluno/<int:aluno_pk>/edit', views.edit_aluno, name='edit-aluno'),
    path('turmas/aluno/<int:aluno_pk>/delete', views.delete_aluno, name='delete-aluno'),
    path('turma/<int:turma_pk>/horario', views.ver_horario, name='show-horario'),
    path('turma/<int:turma_pk>/horario/edit/<int:turno_cod>/<int:dia_cod>', views.alterar_horario, name='alterar-horario'),
    path('professores/add', views.add_professor, name='add-professor'),
    path('professores/', views.list_professores, name='list-professores'),
    path('professor/<int:pk>/edit', views.edit_professor, name='edit-professor'),
    path('professor/<int:pk>/edit', views.delete_professor, name='delete-professor'),
    path('turma/<int:turma_pk>/materias/add', views.add_materia, name='add-materia'),
    path('turma/<int:turma_pk>/materias', views.list_materias, name='list-materias'),
    path('turma/<int:turma_pk>/materia/<int:materia_pk>/edit', views.edit_materia, name='edit-materia'),
    path('turma/<int:turma_pk>/materia/<int:materia_pk>/delete', views.delete_materia, name='delete-materia'),
]