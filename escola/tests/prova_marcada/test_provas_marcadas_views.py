#  Developed by Vinicius José Fritzen
#  Last Modified 31/05/19 07:26.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

import pytest
from django.contrib import auth
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from escola.models import MateriaDaTurma, Turma, AreaConhecimento, ProvaMateriaMarcada, ProvaAreaMarcada

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.django_db
# Testes das views para garantir que aparecem


@pytest.mark.provas_marcadas
def test_lista_provas_turma(aluno_client: Client, turma: Turma, tc: TestCase):
    response = aluno_client.get(reverse('escola:provas-turma-list', args=[turma.pk, ]))
    tc.assertContains(response, f"<h1>Provas Marcadas da {turma.__str__()}</h1>")
    tc.assertContains(response, "<table")
    tc.assertTemplateUsed(response, "escola/panels/listaProvasMarcadas.html")


@pytest.mark.provas_marcadas
def test_create_prova_materia_professor_get(professor_client: Client, tc: TestCase):
    response = professor_client.get(reverse('escola:marcar-prova-materia'))
    tc.assertContains(response, "<h1>Marcar uma prova</h1>")
    tc.assertTemplateUsed(response, "escola/provas_marcadas/marcar_prova_professor.html")


@pytest.mark.provas_marcadas
def test_create_prova_area_professor_get(professor_client: Client, tc: TestCase):
    response = professor_client.get(reverse('escola:marcar-prova-area'))
    tc.assertContains(response, "<h1>Marcar uma prova</h1>")
    tc.assertTemplateUsed(response, "escola/provas_marcadas/marcar_prova_professor.html")


@pytest.mark.provas_marcadas
def test_list_provas_professor(professor_client: Client, tc: TestCase):
    response = professor_client.get(reverse('escola:provas-professor'))
    tc.assertContains(response, "<h1>Minhas Provas marcadas</h1>")
    tc.assertTemplateUsed(response, 'escola/provas_marcadas/listProvasProfessor.html')


@pytest.mark.provas_marcadas
def test_delete_prova_materia_get(prova_marcada_materia, tc: TestCase, client: Client):
    client.force_login(prova_marcada_materia.get_owner())
    response = client.get(reverse('escola:provas-materia-delete', args=[prova_marcada_materia.pk]))
    tc.assertTemplateUsed(response, 'escola/base_delete.html')


@pytest.mark.provas_marcadas
def test_delete_prova_area_get(prova_marcada_area, tc: TestCase, client: Client):
    client.force_login(prova_marcada_area.get_owner())
    response = client.get(reverse('escola:provas-area-delete', args=[prova_marcada_area.pk]))
    tc.assertTemplateUsed(response, 'escola/base_delete.html')


@pytest.mark.provas_marcadas
def test_detail_prova_materia(prova_marcada_materia, tc: TestCase, aluno_client: Client):
    response = aluno_client.get(prova_marcada_materia.get_absolute_url())
    tc.assertContains(response, prova_marcada_materia.get_nome())
    tc.assertContains(response, prova_marcada_materia.get_descricao())
    tc.assertContains(response, prova_marcada_materia.get_apresentacao())
    tc.assertTemplateUsed(response, 'escola/provas_marcadas/detail_prova.html')


@pytest.mark.provas_marcadas
def test_detail_prova_area(prova_marcada_area, tc: TestCase, aluno_client: Client):
    response = aluno_client.get(prova_marcada_area.get_absolute_url())
    tc.assertContains(response, prova_marcada_area.get_nome())
    tc.assertContains(response, prova_marcada_area.get_descricao())
    tc.assertTemplateUsed(response, 'escola/provas_marcadas/detail_prova.html')


@pytest.mark.provas_marcadas
def test_calendario_turma(turma: Turma, tc: TestCase, professor_client: Client):
    response = professor_client.get(reverse('escola:turma-provas-calendario', args=[turma.pk, ]))
    tc.assertTemplateUsed(response, 'escola/provas_marcadas/calendarioDatasLivres.html')

# Testes de funções das views (POST)


@pytest.mark.provas_marcadas
def test_create_prova_area_professor_post(professor_client: Client, tc: TestCase, faker):
    user = auth.get_user(professor_client)
    materia: MateriaDaTurma = user.professor.materias.first()
    area: AreaConhecimento = materia.area
    area.turma.regente = user
    area.turma.save()
    titulo = faker.sentence()
    response = professor_client.post(reverse('escola:marcar-prova-area'), {'titulo': titulo, 'data': faker.future_datetime(), 'descricao': faker.paragraph(), 'area': area.pk})
    tc.assertRedirects(response, reverse('escola:index'))
    assert len(area.provas_area.all()) == 1
    assert area.provas_area.first().get_nome() == titulo


@pytest.mark.provas_marcadas
def test_create_prova_materia_professor_post(professor_client: Client, tc: TestCase, faker):
    user = auth.get_user(professor_client)
    materia: MateriaDaTurma = user.professor.materias.first()
    titulo = faker.sentence()
    response = professor_client.post(reverse('escola:marcar-prova-materia'), {'titulo': titulo, 'data': faker.future_datetime(), 'descricao': faker.paragraph(), 'materia': materia.pk})
    tc.assertRedirects(response, reverse('escola:index'))
    assert len(materia.provas_materia.all()) == 1
    assert materia.provas_materia.first().get_nome() == titulo


@pytest.mark.provas_marcadas
def test_delete_prova_materia_post(prova_marcada_materia, tc, client):
    user = prova_marcada_materia.get_owner()
    client.force_login(user)
    client.post(reverse('escola:provas-materia-delete', args=[prova_marcada_materia.pk, ]))
    assert 0 == len(ProvaMateriaMarcada.objects.filter(pk=prova_marcada_materia.pk))


@pytest.mark.provas_marcadas
def test_delete_prova_area_post(prova_marcada_area, tc, client):
    user = prova_marcada_area.get_owner()
    client.force_login(user)
    client.post(reverse('escola:provas-area-delete', args=[prova_marcada_area.pk, ]))
    assert 0 == len(ProvaAreaMarcada.objects.filter(pk=prova_marcada_area.pk))


# Testes de permissão falha
# TODO
