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