#  Developed by Vinicius José Fritzen
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

import pytest
from django.test import Client, TestCase
from django.urls import reverse

from escola.models import Conteudo, Profile

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.django_db
# Testes das views para garantir que aparecem


@pytest.mark.conteudo
def test_create_conteudo_raiz_get(professor_client: Client, tc: TestCase):
    response = professor_client.get(reverse('escola:conteudo_add'))
    tc.assertTemplateUsed(response, 'escola/conteudo/create_conteudo.html')


@pytest.mark.conteudo
def test_create_conteudo_filho_get(professor_client: Client, tc: TestCase, conteudo: Conteudo):
    response = professor_client.get(reverse('escola:conteudo_add', args=(conteudo.pk,)))
    tc.assertTemplateUsed(response, 'escola/conteudo/create_conteudo.html')


@pytest.mark.conteudo
def test_update_conteudo_get(conteudo: Conteudo, tc: TestCase, client: Client):
    user = conteudo.professor.user
    client.force_login(user)
    response = client.get(reverse('escola:update-conteudo', args=(conteudo.pk, )))
    tc.assertTemplateUsed(response, 'escola/conteudo/create_conteudo.html')


@pytest.mark.conteudo
def test_detail_conteudo_get(conteudo, aluno_client, tc):
    response = aluno_client.get(reverse('escola:conteudo-detail', args=(conteudo.pk, )))
    tc.assertTemplateUsed(response, 'escola/conteudo_detail.html')


@pytest.mark.conteudo
def test_add_link_conteudo_get(conteudo, tc, client):
    user = conteudo.professor.user
    client.force_login(user)
    p, c = Profile.objects.get_or_create(user=user, defaults={'is_aluno': False, 'is_professor': False})
    p.is_professor = True
    p.save()
    response = client.get(reverse('escola:add-link-conteudo', args=(conteudo.pk, )))
    print(response)
    tc.assertTemplateUsed(response, 'escola/linkconteudo_form.html')


@pytest.mark.conteudo
def test_add_conteudo_materia_get(materia, client, tc):
    user = materia.professor.user
    client.force_login(user)
    response = client.get(reverse('escola:add-conteudo-materia', args=(materia.pk, )))
    tc.assertTemplateUsed(response, 'escola/conteudo/addConteudoToMateria.html')


@pytest.mark.conteudo
def test_meus_conteudos_get(professor_client, tc):
    response = professor_client.get(reverse('escola:conteudos-professor'))
    tc.assertTemplateUsed(response, 'escola/professor/listConteudos.html')
