#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 10:16.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.urls import reverse, resolve

from escola import views, views_turma, views_aluno, views_cargo, views_horario, views_professor, views_materia, \
    views_tarefa, views_conteudo


# path('api/v1/', include(router.urls)),
# TODO: 13/04/2019 por wwwvi: Add test for API resolved

def test_index_url_is_resolved():
    """Test index url"""
    url = reverse('escola:index')
    assert resolve(url).func == views.index


def test_turmas_list_url_is_resolved():
    """Test turmas list url is resolved"""
    url = reverse('escola:list-turmas')
    assert resolve(url).func == views_turma.list_turmas


def test_turmas_add_url_is_resolved():
    url = reverse('escola:add-turma')
    assert resolve(url).func == views_turma.add_turma


def test_turma_edit_url_is_resolved():
    url = reverse('escola:edit-turma', args=[1, ])
    assert resolve(url).func == views_turma.edit_turma


#     path('turmas/delete/<int:pk>', escola.views_turma.delete_turma, name='delete-turma'),
def test_turma_delete_url_is_resolved():
    url = reverse('escola:delete-turma', args=[1, ])
    assert resolve(url).func == views_turma.delete_turma


#     path('alunos/populate/', escola.views_aluno.populate_alunos, name='populate-alunos'),
def test_populate_alunos_url_is_resolved():
    url = reverse('escola:populate-alunos')
    assert resolve(url).func == views_aluno.populate_alunos


#     path('turmas/<int:pk_turma>/cargos', escola.views_cargo.list_cargos, name='list-cargos'),


def test_list_cargo_url_is_resolved():
    url = reverse('escola:list-cargos', args=[1, ])
    assert resolve(url).func == views_cargo.list_cargos


#     path('turmas/<int:turma_pk>/cargos/add', escola.views_cargo.add_cargo, name='add-cargo'),
def test_add_cargo_url_is_resolved():
    url = reverse('escola:add-cargo', args=[1, ])
    assert resolve(url).func == views_cargo.add_cargo


#     path('turmas/cargos/edit/<int:pk>', escola.views_cargo.edit_cargo, name='edit-cargo'),
def test_edit_cargo_url_is_resolved():
    url = reverse('escola:edit-cargo', args=[1, ])
    assert resolve(url).func == views_cargo.edit_cargo


#     path('turmas/cargos/delete/<int:pk>', escola.views_cargo.delete_cargo, name='delete-cargo'),
def test_delete_cargo_url_is_resolved():
    url = reverse('escola:delete-cargo', args=[1, ])
    assert resolve(url).func == views_cargo.delete_cargo


#     path('turma/<int:turma_pk>/alunos', escola.views_aluno.list_alunos, name='list-alunos'),

def test_list_alunos_url_is_resolved():
    url = reverse('escola:list-alunos', args=[1, ])
    assert resolve(url).func == views_aluno.list_alunos


#     path('turma/<int:turma_pk>/alunos/add', escola.views_aluno.add_aluno, name='add-aluno'),

def test_add_aluno_url_is_resolved():
    url = reverse('escola:add-aluno', args=[1, ])
    assert resolve(url).func == views_aluno.add_aluno


#     path('turmas/aluno/<int:aluno_pk>/edit', views.edit_aluno, name='edit-aluno'),
def test_edit_aluno_url_is_resolved():
    url = reverse('escola:edit-aluno', args=[1, ])
    assert resolve(url).func == views.edit_aluno


#     path('turmas/aluno/<int:aluno_pk>/delete', views.delete_aluno, name='delete-aluno'),
def test_delete_aluno_url_is_resolved():
    url = reverse('escola:delete-aluno', args=[1, ])
    assert resolve(url).func == views.delete_aluno


#     path('turma/<int:turma_pk>/horario', escola.views_horario.ver_horario, name='show-horario'),
def test_ver_horario_url_is_resolved():
    url = reverse('escola:show-horario', args=[1, ])
    assert resolve(url).func == views_horario.ver_horario


#     path('turma/<int:turma_pk>/horario/edit/<int:turno_cod>/<int:dia_cod>', escola.views_horario.alterar_horario,
#          name='alterar-horario'),
def test_edit_horario_url_is_resolved():
    url = reverse('escola:alterar-horario', args=[1, 1, 1, ])
    assert resolve(url).func == views_horario.alterar_horario


#     path('professores/add', escola.views_professor.add_professor, name='add-professor'),
def test_add_professor_url_is_resolved():
    url = reverse('escola:add-professor')
    assert resolve(url).func == views_professor.add_professor


#     path('professores/', escola.views_professor.list_professores, name='list-professores'),
def test_list_professor_url_is_resolved():
    url = reverse('escola:list-professores')
    assert resolve(url).func == views_professor.list_professores


#     path('professor/<int:pk>/edit', escola.views_professor.edit_professor, name='edit-professor'),
def test_edit_professor_url_is_resolved():
    url = reverse('escola:edit-professor', args=[1, ])
    assert resolve(url).func == views_professor.edit_professor


#     path('professor/<int:pk>/delete', escola.views_professor.delete_professor, name='delete-professor'),
def test_delete_professor_url_is_resolved():
    url = reverse('escola:delete-professor', args=[1, ])
    assert resolve(url).func == views_professor.delete_professor


#     path('turma/<int:turma_pk>/materias/add', escola.views_materia.add_materia, name='add-materia'),
def test_add_materia_url_is_resolved():
    url = reverse('escola:add-materia', args=[1, ])
    assert resolve(url).func == views_materia.add_materia


#     path('turma/<int:turma_pk>/materias', escola.views_materia.list_materias, name='list-materias'),
def test_list_materia_url_is_resolved():
    url = reverse('escola:list-materias', args=[1, ])
    assert resolve(url).func == views_materia.list_materias


#     path('materia/<int:materia_pk>/edit', escola.views_materia.edit_materia, name='edit-materia'),
def test_edit_materia_url_is_resolved():
    url = reverse('escola:edit-materia', args=[1, ])
    assert resolve(url).func == views_materia.edit_materia
#     path('materia/<int:materia_pk>/delete', escola.views_materia.delete_materia,
#          name='delete-materia'),
def test_delete_materia_url_is_resolved():
    url = reverse('escola:delete-materia', args=[1, ])
    assert resolve(url).func == views_materia.delete_materia

#     path('materia/<int:pk>', escola.views_materia.MateriaDaTurmaDetailView.as_view(),
#          name='detail-materia'),
def test_detail_materia_url_is_resolved():
    url = reverse('escola:detail-materia', args=[1, ])
    assert resolve(url).func.__name__ == views_materia.MateriaDaTurmaDetailView.as_view().__name__
#     path('turma/<int:turma_pk>/tarefas/add', escola.views_tarefa.add_tarefa, name='add-tarefa'),
def test_add_tarefa_url_is_resolved():
    url = reverse('escola:add-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.add_tarefa
#     path('turma/<int:turma_pk>/tarefas', escola.views_tarefa.list_tarefa, name='list-tarefa'),
def test_list_tarefas_url_is_resolved():
    url = reverse('escola:list-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.list_tarefa
#     path('turma/tarefa/<int:tarefa_pk>/edit', escola.views_tarefa.edit_tarefa, name='edit-tarefa'),
def test_edit_tarefa_url_is_resolved():
    url = reverse('escola:edit-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.edit_tarefa
#     path('turma/tarefa/<int:tarefa_pk>/delete', escola.views_tarefa.delete_tarefa, name='delete-tarefa'),
def test_delete_tarefa_url_is_resolved():
    url = reverse('escola:delete-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.delete_tarefa
#     path('turma/tarefa/<int:tarefa_pk>/concluir', escola.views_tarefa.concluir_tarefa, name='concluir-tarefa'),
def test_concluir_tarefa_url_is_resolved():
    url = reverse('escola:concluir-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.concluir_tarefa
#     path('turma/tarefa/<int:tarefa_pk>', escola.views_tarefa.detalhes_tarefa, name='detalhes-tarefa'),
def test_detalhes_tarefa_url_is_resolved():
    url = reverse('escola:detalhes-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.detalhes_tarefa

#     path('seguir/<int:pk>', views.seguir_manager, name='seguir'),
def test_seguir_url_is_resolved():
    url = reverse('escola:seguir', args=[1, ])
    assert resolve(url).func == views.seguir_manager

# # Conteudos
# urlpatterns += \
#     [
#         path('conteudo/<int:pk>', escola.views_conteudo.ConteudoDetail.as_view(), name='conteudo-detail'),
def test_conteudo_detail_url_is_resolved():
    url = reverse('escola:conteudo-detail', args=[1, ])
    assert resolve(url).func.__name__ == views_conteudo.ConteudoDetail.as_view().__name__
#         path('conteudo/add/<int:pk_parent>', escola.views_conteudo.ConteudoCreate.as_view(), name='conteudo_add'),
def test_add_conteudo_url_is_resolved():
    url = reverse('escola:conteudo_add', args=[1, ])
    assert resolve(url).func.__name__ == views_conteudo.ConteudoCreate.as_view().__name__
#         path('conteudo/add/', escola.views_conteudo.ConteudoCreate.as_view(), name='conteudo_add'),
def test_add_conteudo_url_is_resolved():
    url = reverse('escola:conteudo_add')
    assert resolve(url).func.__name__ == views_conteudo.ConteudoCreate.as_view().__name__
#         path('materia/<int:materia>/addConteudos', escola.views_conteudo.addConteudosAMateria.as_view(),
#              name='add-conteudo-materia'),
def test_add_conteudo_materia_url_is_resolved():
    url = reverse('escola:add-conteudo-materia', args=[1, ])
    assert resolve(url).func.__name__ == views_conteudo.addConteudosAMateria.as_view().__name__
#         path('conteudo/<int:pk>/add', escola.views_conteudo.LinkConteudoCreateView.as_view(),
#              name='add-link-conteudo'),
def test_add_link_conteudo_url_is_resolved():
    url = reverse('escola:add-link-conteudo', args=[1, ])
    assert resolve(url).func.__name__ == views_conteudo.LinkConteudoCreateView.as_view().__name__
#         path('conteudo/<int:pk>/add/<int:cat>', escola.views_conteudo.LinkConteudoCreateView.as_view(),
#              name='add-link-conteudo'),
def test_add_link_conteudo_with_categoria_url_is_resolved():
    url = reverse('escola:add-link-conteudo', args=[1,1, ])
    assert resolve(url).func.__name__ == views_conteudo.LinkConteudoCreateView.as_view().__name__
# path('notificacoes', escola.views.NotificacaoListView.as_view(), name='notificacoes-list'),
def test_notificacoes_url_is_resolved():
    url = reverse('escola:notificacoes-list')
    assert resolve(url).func.__name__ == views.NotificacaoListView.as_view().__name__

#         path('sobre', escola.views.SobreView.as_view(), name='sobre'),
def test_sobre_url_is_resolved():
    url = reverse('escola:sobre')
    assert resolve(url).func.__name__ == views.SobreView.as_view().__name__
#         path('self/materias', escola.views_professor.MateriaProfessorListView.as_view(), name='materias_professor'),
def test_self_materias_url_is_resolved():
    url = reverse('escola:materias_professor')
    assert resolve(url).func.__name__ == views_professor.MateriaProfessorListView.as_view().__name__
#         path('self/conteudos', escola.views_conteudo.MeusConteudosListView.as_view(), name='conteudos-professor'),
def test_self_conteudos_url_is_resolved():
    url = reverse('escola:conteudos-professor')
    assert resolve(url).func.__name__ == views_conteudo.MeusConteudosListView.as_view().__name__
#     ]
