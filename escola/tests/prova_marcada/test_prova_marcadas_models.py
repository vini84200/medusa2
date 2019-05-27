import datetime

import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from escola import user_utils
from escola.models import Evento, EventoTurma, ProvaMarcada, ProvaAreaMarcada, ProvaMateriaMarcada, Turma, \
    MateriaDaTurma, AreaConhecimento, Conteudo

pytestmark = pytest.mark.django_db


# Turma


def test_turma_get_alunos(faker):
    turma: Turma = mixer.blend(Turma)
    assert len(turma.get_list_alunos()) == 0
    aluno0 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    assert aluno0 in turma.get_list_alunos()
    assert len(turma.get_list_alunos()) == 1
    aluno1 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    assert aluno1 in turma.get_list_alunos()
    assert len(turma.get_list_alunos()) == 2


# Evento


def test_evento_create(faker):
    initial = Evento.objects.count()
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert initial + 1 == Evento.objects.count()


def test_evento_get_nome(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.get_nome() == nome


def test_evento_get_data(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.get_data() == data


def test_evento_get_descricao(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.get_descricao() == descricao


def test_evento_get_owner(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.get_owner() == owner


def test_evento_somebody_has_permition_to_edit_denies(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    somebody = mixer.blend(User)
    assert a.has_permition_edit(somebody) is False


def test_evento_owner_has_permition_to_edit_accept(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.has_permition_edit(owner) is True


def test_evento_update(faker):
    nome_original = faker.sentence()
    nome_novo = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome_original, data, descricao, owner)
    assert not nome_novo == nome_original  # Se isso der problema, rode novamente
    assert a.get_nome() == nome_original
    a.update(nome=nome_novo)
    assert a.get_nome() == nome_novo


# Test Evento Turma


def test_evento_turma_create(faker):
    initial = EventoTurma.objects.count()
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    assert initial + 1 == EventoTurma.objects.count()


def test_evento_turma_get_nome(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    assert a.get_nome() == nome


def test_evento_turma_get_data(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    assert a.get_data() == data


def test_evento_turma_get_descricao(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    assert a.get_descricao() == descricao


def test_evento_turma_get_owner(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    assert a.get_owner() == owner


def test_evento_turma_get_turma(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    assert a.get_turma() == turma


def test_evento_turma_somebody_has_permition_to_edit_denies(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    somebody = mixer.blend(User)
    assert a.has_permition_edit(somebody) is False


def test_evento_turma_owner_has_permition_to_edit_accept(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    assert a.has_permition_edit(owner) is True


def test_evento_turma_update(faker):
    turma_original = mixer.blend(Turma)
    turma_nova = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = EventoTurma.create(turma_original, nome, data, descricao, owner)
    assert not turma_nova == turma_original  # Se isso der problema, rode novamente
    assert a.get_turma() == turma_original
    a.update(turma=turma_nova)
    assert a.get_turma() == turma_nova


def test_evento_turma_get_participantes(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    aluno0 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    aluno1 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    a = EventoTurma.create(turma, nome, data, descricao, owner)
    assert aluno0 in a.get_participantes()
    assert aluno1 in a.get_participantes()
    assert len(a.get_participantes()) == 2


# Prova Marcada


def test_prova_marcada_create(faker):
    initial = ProvaMarcada.objects.count()
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    assert initial + 1 == ProvaMarcada.objects.count()


def test_prova_marcada_get_nome(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    assert a.get_nome() == nome


def test_prova_marcada_get_data(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    assert a.get_data() == data


def test_prova_marcada_get_descricao(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    assert a.get_descricao() == descricao


def test_prova_marcada_get_owner(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    assert a.get_owner() == owner


def test_prova_marcada_get_turma(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    assert a.get_turma() == turma


def test_prova_marcada_somebody_has_permition_to_edit_denies(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    somebody = mixer.blend(User)
    assert a.has_permition_edit(somebody) is False


def test_prova_marcada_owner_has_permition_to_edit_accept(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    assert a.has_permition_edit(owner) is True


def test_prova_marcada_get_participantes(faker):
    turma = mixer.blend(Turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    aluno0 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    aluno1 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    a = ProvaMarcada.create(turma, nome, data, descricao, owner)
    assert aluno0 in a.get_participantes()
    assert aluno1 in a.get_participantes()
    assert len(a.get_participantes()) == 2


def test_prova_marcada_get_materias(faker):
    materia = mixer.blend(MateriaDaTurma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert a._prova.get_materias() == a.get_materias()
    assert a._prova.get_materias() == [materia, ]


# def test_prova_marcada_get_conteudos(faker):
#     turma = mixer.blend(Turma)
#     nome = faker.sentence()
#     data = faker.date_time()
#     descricao = faker.paragraph()
#     owner = mixer.blend(User)
#     a = ProvaMarcada.create(turma, nome, data, descricao, owner)
#     assert None is a.get_conteudos()
#     c = mixer.blend(Conteudo)
#     a.conteudos.add(c)
#     assert a.get_conteudos() == [c, ]
#
#
# def test_prova_marcada_add_conteudo(faker):
#     turma = mixer.blend(Turma)
#     nome = faker.sentence()
#     data = faker.date_time()
#     descricao = faker.paragraph()
#     owner = mixer.blend(User)
#     a = ProvaMarcada.create(turma, nome, data, descricao, owner)
#     assert a.get_conteudos() == []
#     c = mixer.blend(Conteudo)
#     a.add_conteudo(c)
#     assert a.get_conteudos() == [c, ]
#
#
# def test_prova_marcada_add_conteudos(faker):
#     turma = mixer.blend(Turma)
#     nome = faker.sentence()
#     data = faker.date_time()
#     descricao = faker.paragraph()
#     owner = mixer.blend(User)
#     a = ProvaMarcada.create(turma, nome, data, descricao, owner)
#     assert a.get_conteudos() == []
#     c0 = mixer.blend(Conteudo)
#     c1 = mixer.blend(Conteudo)
#     a.add_conteudos([c0, c1, ])
#     assert a.get_conteudos() == [c0, c1, ]

# Prova Marcada Materia


def test_prova_marcada_materia_create(faker):
    initial = ProvaMateriaMarcada.objects.count()
    materia = mixer.blend(MateriaDaTurma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert a.get_materias() == [materia, ]


def test_prova_marcada_materia_get_nome(faker):
    materia = mixer.blend(MateriaDaTurma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert a.get_nome() == nome


def test_prova_marcada_materia_get_data(faker):
    materia = mixer.blend(MateriaDaTurma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert a.get_data() == data


def test_prova_marcada_materia_get_descricao(faker):
    materia = mixer.blend(MateriaDaTurma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert a.get_descricao() == descricao


def test_prova_marcada_materia_get_owner(faker):
    materia = mixer.blend(MateriaDaTurma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert a.get_owner() == owner


def test_prova_marcada_materia_get_turma(faker):
    turma = mixer.blend(Turma)
    materia = mixer.blend(MateriaDaTurma, turma=turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert a.get_turma() == turma


def test_prova_marcada_materia_somebody_has_permition_to_edit_denies(faker):
    materia = mixer.blend(MateriaDaTurma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    somebody = mixer.blend(User)
    assert a.has_permition_edit(somebody) is False


def test_prova_marcada_materia_owner_has_permition_to_edit_accept(faker):
    materia = mixer.blend(MateriaDaTurma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert a.has_permition_edit(owner) is True


def test_prova_marcada_materia_get_participantes(faker):
    turma = mixer.blend(Turma)
    materia = mixer.blend(MateriaDaTurma, turma=turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    aluno0 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    aluno1 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    a = ProvaMateriaMarcada.create(materia, nome, data, descricao, owner)
    assert aluno0 in a.get_participantes()
    assert aluno1 in a.get_participantes()
    assert len(a.get_participantes()) == 2


# Prova Marcada Area

def test_prova_marcada_area_create(faker):
    initial = ProvaAreaMarcada.objects.count()
    area = mixer.blend(AreaConhecimento)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    assert initial + 1 == ProvaAreaMarcada.objects.count()


def test_prova_marcada_area_get_nome(faker):
    area = mixer.blend(AreaConhecimento)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    assert a.get_nome() == nome


def test_prova_marcada_area_get_data(faker):
    area = mixer.blend(AreaConhecimento)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    assert a.get_data() == data


def test_prova_marcada_area_get_descricao(faker):
    area = mixer.blend(AreaConhecimento)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    assert a.get_descricao() == descricao


def test_prova_marcada_area_get_owner(faker):
    area = mixer.blend(AreaConhecimento)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    assert a.get_owner() == owner


def test_prova_marcada_area_get_turma(faker):
    turma = mixer.blend(Turma)
    area = mixer.blend(AreaConhecimento, turma=turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    assert a.get_turma() == turma


def test_prova_marcada_area_somebody_has_permition_to_edit_denies(faker):
    area = mixer.blend(AreaConhecimento)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    somebody = mixer.blend(User)
    assert a.has_permition_edit(somebody) is False


def test_prova_marcada_area_owner_has_permition_to_edit_accept(faker):
    area = mixer.blend(AreaConhecimento)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    assert a.has_permition_edit(owner) is True


def test_prova_marcada_area_get_participantes(faker):
    turma = mixer.blend(Turma)
    area = mixer.blend(AreaConhecimento, turma=turma)
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    aluno0 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    aluno1 = user_utils.create_aluno_user(faker.user_name(), faker.password(), turma, faker.name)
    a = ProvaAreaMarcada.create(area, nome, data, descricao, owner)
    assert aluno0 in a.get_participantes()
    assert aluno1 in a.get_participantes()
    assert len(a.get_participantes()) == 2
