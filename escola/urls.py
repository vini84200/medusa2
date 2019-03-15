from django.urls import path

from . import views

app_name = 'escola'
urlpatterns = [
    path('', views.index, name='index'),
    # turma
    path('turmas/', views.list_turmas, name='list-turmas'),
    path('turmas/add/', views.add_turma, name='add-turma'),
    path('turmas/edit/<int:pk>', views.edit_turma, name='edit-turma'),
    path('turmas/delete/<int:pk>', views.delete_turma, name='delete-turma'),
    path('alunos/populate/', views.populate_alunos, name='populate-alunos'),
    # cargos
    path('turmas/<int:pk_turma>/cargos', views.list_cargos , name='list-cargos'),
    path('turmas/<int:pk_turma>/cargos/add', views.add_cargo, name='add-cargo'),
    path('turmas/cargos/edit/<int:pk>', views.edit_cargo, name='edit-cargo'),
    path('turmas/cargos/delete/<int:pk>', views.delete_cargo, name='delete-cargo'),
    # alunos
    path('turma/<int:turma_pk>/alunos', views.list_alunos, name='list-alunos'),
    path('turma/<int:turma_pk>/alunos/add', views.add_aluno, name='add-aluno'),
    path('turmas/aluno/<int:aluno_pk>/edit', views.edit_aluno, name='edit-aluno'),
    path('turmas/aluno/<int:aluno_pk>/delete', views.delete_aluno, name='delete-aluno'),
    # horario
    path('turma/<int:turma_pk>/horario', views.ver_horario, name='show-horario'),
    path('turma/<int:turma_pk>/horario/edit/<int:turno_cod>/<int:dia_cod>', views.alterar_horario, name='alterar-horario'),
    # professores
    path('professores/add', views.add_professor, name='add-professor'),
    path('professores/', views.list_professores, name='list-professores'),
    path('professor/<int:pk>/edit', views.edit_professor, name='edit-professor'),
    path('professor/<int:pk>/delete', views.delete_professor, name='delete-professor'),
    # materias
    path('turma/<int:turma_pk>/materias/add', views.add_materia, name='add-materia'),
    path('turma/<int:turma_pk>/materias', views.list_materias, name='list-materias'),
    path('turma/<int:turma_pk>/materia/<int:materia_pk>/edit', views.edit_materia, name='edit-materia'),
    path('turma/<int:turma_pk>/materia/<int:materia_pk>/delete', views.delete_materia, name='delete-materia'),
    # tarefa
    path('turma/<int:turma_pk>/tarefas/add', views.add_tarefa, name='add-tarefa'),
    path('turma/<int:turma_pk>/tarefas', views.list_tarefa, name='list-tarefa'),
    path('turma/tarefa/<int:tarefa_pk>/edit', views.edit_tarefa, name='edit-tarefa'),
    path('turma/tarefa/<int:tarefa_pk>/delete', views.delete_tarefa, name='delete-tarefa'),
    path('turma/tarefa/<int:tarefa_pk>/concluir', views.concluir_tarefa, name='concluir-tarefa'),
    path('turma/tarefa/<int:tarefa_pk>', views.detalhes_tarefa, name='detalhes-tarefa'),
    # Seguir
    path('seguir/<int:pk>', views.seguir_manager, name='seguir'),
]