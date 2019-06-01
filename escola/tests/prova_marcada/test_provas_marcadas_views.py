#  Developed by Vinicius José Fritzen
#  Last Modified 31/05/19 07:26.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
import pytest
from django.urls import reverse
from escola.models import Turma
from django.test import TestCase

from django.test.client import Client

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
def test_create_prova_materia_professor(professor_client: Client, tc: TestCase):
    response = professor_client.get(reverse('escola:marcar-prova-materia'))
    tc.assertContains(response, "<h1>Marcar uma prova</h1>")
    tc.assertTemplateUsed(response, "escola/provas_marcadas/marcar_prova_professor.html")


@pytest.mark.provas_marcadas
def test_create_prova_area_professor(professor_client: Client, tc: TestCase):
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
def test_detail_prova_materia_get(prova_marcada_materia, tc: TestCase, aluno_client: Client):
    response = aluno_client.get(prova_marcada_materia.get_absolute_url())
    tc.assertContains(response, prova_marcada_materia.get_nome())
    tc.assertContains(response, prova_marcada_materia.get_descricao())
    tc.assertContains(response, prova_marcada_materia.get_apresentacao())
    tc.assertTemplateUsed(response, 'escola/provas_marcadas/detail_prova.html')


@pytest.mark.provas_marcadas
def test_detail_prova_area_get(prova_marcada_area, tc: TestCase, aluno_client: Client):
    response = aluno_client.get(prova_marcada_area.get_absolute_url())
    tc.assertContains(response, prova_marcada_area.get_nome())
    tc.assertContains(response, prova_marcada_area.get_descricao())
    tc.assertTemplateUsed(response, 'escola/provas_marcadas/detail_prova.html')


@pytest.mark.provas_marcadas
def test_calendario_turma_get(turma: Turma, tc: TestCase, professor_client: Client):
    response = professor_client.get(reverse('escola:turma-provas-calendario', args=[turma.pk, ]))
    tc.assertTemplateUsed(response, 'escola/provas_marcadas/calendarioDatasLivres.html')
