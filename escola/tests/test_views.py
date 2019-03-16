from django.http import HttpResponseRedirect
from django.test.client import Client
import pytest
from escola.models import *
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.urls import reverse
from django.test.testcases import TestCase

pytestmark = pytest.mark.django_db


def create_aluno():
    user = mixer.blend(User)
    profile = mixer.blend(Profile, user=user, is_aluno=True, is_professor=False)
    aluno = mixer.blend(Aluno, user=user)
    return aluno


def create_aluno(turma):
    user = mixer.blend(User, turma=turma)
    profile = mixer.blend(Profile, user=user, is_aluno=True, is_professor=False)
    aluno = mixer.blend(Aluno, user=user)
    return aluno


def create_professor():
    user = mixer.blend(User)
    profile = mixer.blend(Profile, user=user, is_aluno=False, is_professor=True)
    professor = mixer.blend(Professor, user=user)
    return professor


def create_turma():
    turma = mixer.blend(Turma)
    aluno = create_aluno(turma=turma)
    prof = create_professor()
    materia = mixer.blend(MateriaDaTurma, professor=prof, turma=turma)
    return turma


class TestIndex:
    page_name = 'escola:index'

    def test_annonymous(self, client: Client, rf):
        response = client.get(reverse(self.page_name), follow=False)
        assert response.status_code == 302, 'Caso um usario não logue deve ser redirecionado'
        assert reverse('login') in response.url

    def test_user_not_escola(self, client, rf):
        client.login(username='cazuza', password='senha1234')
        response = client.get(reverse(self.page_name), follow=False)
        assert response.status_code == 302, 'Caso um usario não seja aluno deve ser redirecionado'
        assert reverse('login') in response.url

    # def test_aluno(self):


# class TestAddTurma:
#
# class TestListTurmas:
#
# class TestEditTurmas:
#
# class TestDeleteTurmas:
#
# class TestPopulateAlunos:
#
# class TestAddCargo:
#
# class TestListCargos:
#
# class TestEditCargo:
#
# class TestDeleteCargo:
#
# class TestAddAluno:
#
# class TestListAlunos:
#
# class TestVerHorario:
#
# class TestAlterarHorario:
#
# class TestEditAluno:
#
# class TestDeleteAluno:
#
# class TestAddProfessor:
#
# class TestListProfessor:
#
# class TestEditProfessor:
#
# class TestDeleteProfessor:
#
# class TestAddMateria:
#
# class TestListMaterias:
#
# class TestEditMateria:
#
# class TestDeleteMateria:
#
# class TestAddTarefa:
#
# class TestListTarefa:
#
# class TestEditTarefa:
#
# class TestDeleteTarefa:
#
class TestConcluirTarefa(TestCase):
    def test_permited(self):
        c = Client()
        turma = create_turma()
        tarefa = mixer.blend(Tarefa, turma = turma, materia=turma.materiadaturma_set.all()[0])
        response = c.get(reverse('escola:concluir-tarefa', args=[tarefa.pk,]))



# class TestDetalhesTarefa:
#
# class TestSobre:
#     # Hãn?
#
class TestSeguirManager(TestCase):
    page_name = 'escola:seguir'

    def test_permited(self):
        c = Client()
        response = c.get(reverse(self.page_name, args=[1, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse(self.page_name, args=[1, ]))

    def test_cria_conexao(self):
        # Cria o Cliente
        c = Client()
        # Cria aluno
        aluno = create_aluno()
        # Cria um seguidor para o aluno seguir
        seguidor = mixer.blend(SeguidorManager)
        # Faz login(forcado)
        c.force_login(aluno.user)
        # Pega a resposta dessa operação
        response = c.get(reverse('escola:seguir', args=[seguidor.pk, ]), follow=True)
        # Asserts:
        # Garante que houve um redirecionamento;
        self.assertEqual(response.status_code, 302)
        # Garante que foi redirecionado para o lado certo;
        self.assertRedirects(response, reverse('escola:index'))
        # Garante que o usuario esta seguindo o Seguidor;
        assert seguidor.is_seguidor(aluno.user)
