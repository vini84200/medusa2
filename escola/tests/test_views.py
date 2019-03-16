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


def create_professor():
    user = mixer.blend(User)
    profile = mixer.blend(Profile, user=user, is_aluno=False, is_professor=True)
    professor = mixer.blend(Professor, user=user)
    return professor


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
# class TestConcluirTarefa:
#
# class TestDetalhesTarefa:
#
# class TestSobre:
#     # Hãn?
#
class TestSeguirManager(TestCase):
    page_name = 'escola:seguir'

    def test_permited(self):
        response = self.client.get(reverse(self.page_name), follow=False)
        assert response.status_code == 302, 'Caso um usario não logue deve ser redirecionado'
        assert reverse('login') in response.url

    def test_cria_conexao(self):
        c= Client()
        aluno = create_aluno()
        print(aluno.user)
        seguidor = mixer.blend(SeguidorManager)
        print(aluno.user.username)

        #print(c.login(username='abcde', password='123456'))  # defined in fixture or with factory in setUp()
        c.force_login(aluno.user)
        print(aluno.user.profile_escola.is_aluno)

        response = c.get(reverse('escola:seguir', args=[seguidor.pk, ]), follow=True)
        print(response)
        print(response.status_code)
        print(response.redirect_chain)
        print(aluno.user.profile_escola.is_aluno)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('escola:index'))
        assert seguidor.is_seguidor(aluno.user)
