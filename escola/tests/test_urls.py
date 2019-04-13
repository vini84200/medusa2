"""Realiza testes para verificar que os urls foram inicializados de forma correta."""
#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 10:21.
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


def test_turma_delete_url_is_resolved():
    url = reverse('escola:delete-turma', args=[1, ])
    assert resolve(url).func == views_turma.delete_turma


def test_populate_alunos_url_is_resolved():
    url = reverse('escola:populate-alunos')
    assert resolve(url).func == views_aluno.populate_alunos


def test_list_cargo_url_is_resolved():
    url = reverse('escola:list-cargos', args=[1, ])
    assert resolve(url).func == views_cargo.list_cargos


def test_add_cargo_url_is_resolved():
    url = reverse('escola:add-cargo', args=[1, ])
    assert resolve(url).func == views_cargo.add_cargo


def test_edit_cargo_url_is_resolved():
    url = reverse('escola:edit-cargo', args=[1, ])
    assert resolve(url).func == views_cargo.edit_cargo


def test_delete_cargo_url_is_resolved():
    url = reverse('escola:delete-cargo', args=[1, ])
    assert resolve(url).func == views_cargo.delete_cargo


def test_list_alunos_url_is_resolved():
    url = reverse('escola:list-alunos', args=[1, ])
    assert resolve(url).func == views_aluno.list_alunos


def test_add_aluno_url_is_resolved():
    url = reverse('escola:add-aluno', args=[1, ])
    assert resolve(url).func == views_aluno.add_aluno


def test_edit_aluno_url_is_resolved():
    url = reverse('escola:edit-aluno', args=[1, ])
    assert resolve(url).func == views.edit_aluno


def test_delete_aluno_url_is_resolved():
    url = reverse('escola:delete-aluno', args=[1, ])
    assert resolve(url).func == views.delete_aluno


def test_ver_horario_url_is_resolved():
    url = reverse('escola:show-horario', args=[1, ])
    assert resolve(url).func == views_horario.ver_horario


#          name='alterar-horario'),
def test_edit_horario_url_is_resolved():
    url = reverse('escola:alterar-horario', args=[1, 1, 1, ])
    assert resolve(url).func == views_horario.alterar_horario


def test_add_professor_url_is_resolved():
    url = reverse('escola:add-professor')
    assert resolve(url).func == views_professor.add_professor


def test_list_professor_url_is_resolved():
    url = reverse('escola:list-professores')
    assert resolve(url).func == views_professor.list_professores


def test_edit_professor_url_is_resolved():
    url = reverse('escola:edit-professor', args=[1, ])
    assert resolve(url).func == views_professor.edit_professor


def test_delete_professor_url_is_resolved():
    url = reverse('escola:delete-professor', args=[1, ])
    assert resolve(url).func == views_professor.delete_professor


def test_add_materia_url_is_resolved():
    url = reverse('escola:add-materia', args=[1, ])
    assert resolve(url).func == views_materia.add_materia


def test_list_materia_url_is_resolved():
    url = reverse('escola:list-materias', args=[1, ])
    assert resolve(url).func == views_materia.list_materias


def test_edit_materia_url_is_resolved():
    url = reverse('escola:edit-materia', args=[1, ])
    assert resolve(url).func == views_materia.edit_materia


def test_delete_materia_url_is_resolved():
    url = reverse('escola:delete-materia', args=[1, ])
    assert resolve(url).func == views_materia.delete_materia


#          name='detail-materia'),
def test_detail_materia_url_is_resolved():
    url = reverse('escola:detail-materia', args=[1, ])
    assert resolve(url).func.__name__ == views_materia.MateriaDaTurmaDetailView.as_view().__name__


def test_add_tarefa_url_is_resolved():
    url = reverse('escola:add-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.add_tarefa


def test_list_tarefas_url_is_resolved():
    url = reverse('escola:list-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.list_tarefa


def test_edit_tarefa_url_is_resolved():
    url = reverse('escola:edit-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.edit_tarefa


def test_delete_tarefa_url_is_resolved():
    url = reverse('escola:delete-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.delete_tarefa


def test_concluir_tarefa_url_is_resolved():
    url = reverse('escola:concluir-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.concluir_tarefa


def test_detalhes_tarefa_url_is_resolved():
    url = reverse('escola:detalhes-tarefa', args=[1, ])
    assert resolve(url).func == views_tarefa.detalhes_tarefa


def test_seguir_url_is_resolved():
    url = reverse('escola:seguir', args=[1, ])
    assert resolve(url).func == views.seguir_manager


def test_conteudo_detail_url_is_resolved():
    url = reverse('escola:conteudo-detail', args=[1, ])
    assert resolve(url).func.__name__ == views_conteudo.ConteudoDetail.as_view().__name__


def test_add_conteudo_url_is_resolved():
    url = reverse('escola:conteudo_add', args=[1, ])
    assert resolve(url).func.__name__ == views_conteudo.ConteudoCreate.as_view().__name__


def test_add_conteudo_with_parent_url_is_resolved():
    url = reverse('escola:conteudo_add')
    assert resolve(url).func.__name__ == views_conteudo.ConteudoCreate.as_view().__name__


def test_add_conteudo_materia_url_is_resolved():
    url = reverse('escola:add-conteudo-materia', args=[1, ])
    assert resolve(url).func.__name__ == views_conteudo.addConteudosAMateria.as_view().__name__


def test_add_link_conteudo_url_is_resolved():
    url = reverse('escola:add-link-conteudo', args=[1, ])
    assert resolve(url).func.__name__ == views_conteudo.LinkConteudoCreateView.as_view().__name__


#              name='add-link-conteudo'),
def test_add_link_conteudo_with_categoria_url_is_resolved():
    url = reverse('escola:add-link-conteudo', args=[1, 1, ])
    assert resolve(url).func.__name__ == views_conteudo.LinkConteudoCreateView.as_view().__name__


def test_notificacoes_url_is_resolved():
    url = reverse('escola:notificacoes-list')
    assert resolve(url).func.__name__ == views.NotificacaoListView.as_view().__name__


def test_sobre_url_is_resolved():
    url = reverse('escola:sobre')
    assert resolve(url).func.__name__ == views.SobreView.as_view().__name__


def test_self_materias_url_is_resolved():
    url = reverse('escola:materias_professor')
    assert resolve(url).func.__name__ == views_professor.MateriaProfessorListView.as_view().__name__


def test_self_conteudos_url_is_resolved():
    url = reverse('escola:conteudos-professor')
    assert resolve(url).func.__name__ == views_conteudo.MeusConteudosListView.as_view().__name__
