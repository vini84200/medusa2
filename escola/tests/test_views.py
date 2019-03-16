from django.test.client import Client
import pytest
from escola.models import *
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.urls import reverse
from django.test.testcases import TestCase

pytestmark = pytest.mark.django_db


def create_admin():
    user = mixer.blend(User, is_superuser=True)
    return user


def create_aluno(turma=None):
    if not turma:
        turma = mixer.blend(Turma)
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


class TestIndex(TestCase):
    page_name = 'escola:index'

    def test_annonymous(self):
        client = Client()
        response = client.get(reverse(self.page_name), follow=False)
        assert response.status_code == 302, 'Caso um usario não logue deve ser redirecionado'
        assert reverse('login') in response.url

    def test_user_not_escola(self):
        client = Client()
        client.login(username='cazuza', password='senha1234')
        response = client.get(reverse(self.page_name), follow=False)
        assert response.status_code == 302, 'Caso um usario não seja aluno deve ser redirecionado'
        assert reverse('login') in response.url

    def test_aluno(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'escola/home.html')

    def test_prof(self):
        c = Client()
        prof = create_professor()
        c.force_login(prof.user)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'escola/home.html')

    def test_aparece_horario(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<h2>Horario:</h2>')
        # TODO: Adicionar mais aspectos a serem verificados

    def test_aparece_tarefas(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<h2>Proximas tarefas</h2>')
        # TODO: Adicionar mais aspectos;

    def test_aparece_notificacoes(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        # Como não há uma notificação, a aba de notificações não deve aparecer;
        self.assertNotContains(response, '<h2>Notificações</h2>')
        # Cria uma notificação para aparecer
        noti = mixer.blend(Notificacao, user=aluno.user, visualizado=False)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<h2>Notificações</h2>')
        self.assertContains(response, f'<h3>{noti.title}</h3>')
        self.assertContains(response, f'<p>{noti.msg}</p>')
        # Confirma que as notificações foram marcadas como lidas;
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        # Como todas as notificações foram lidas, ela deve desapaarecer
        self.assertNotContains(response, '<h2>Notificações</h2>')
        self.assertNotContains(response, f'<h3>{noti.title}</h3>')
        self.assertNotContains(response, f'<p>{noti.msg}</p>')

    def test_notificacao_bar_nenhuma_noti(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Você não tem notificações.')

    def test_notificacao_bar_uma_noti(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        noti1 = mixer.blend(Notificacao, user=aluno.user, visualizado=False)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Você tem 1 notificação.')

    def test_notificacao_bar_duas_noti(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        noti2 = mixer.blend(Notificacao, user=aluno.user, visualizado=False)
        noti3 = mixer.blend(Notificacao, user=aluno.user, visualizado=False)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Você tem 2 notificações.')

    def test_nao_aparece_notificacoes_alheias(self):
        c = Client()
        aluno = create_aluno()
        aluno_2 = create_aluno()
        c.force_login(aluno.user)
        noti = mixer.blend(Notificacao, user=aluno_2.user, visualizado=False)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        # Como todas as notificações foram lidas, ela deve desapaarecer
        self.assertNotContains(response, '<h2>Notificações</h2>')
        self.assertNotContains(response, f'<h3>{noti.title}</h3>')
        self.assertNotContains(response, f'<p>{noti.msg}</p>')


class TestAddTurma(TestCase):
    def test_permission_anonymous(self):
        c = Client()
        c.logout()
        response = c.get(reverse('escola:add-turma'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:add-turma'))

    def test_permission_user_not_admin(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        response = c.get(reverse('escola:add-turma'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:add-turma'))

    def test_permission_admin(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        response = c.get(reverse('escola:add-turma'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'escola/turma/criarForm.html')

    def test_blank_values(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        response = c.post(reverse('escola:add-turma'), {})
        self.assertFormError(response, 'form', 'numero', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'ano', 'Este campo é obrigatório.')

    def test_create_invalid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        response = c.post(reverse('escola:add-turma'), {'numero': -12, 'ano': 2.4})
        self.assertFormError(response, 'form', 'numero', 'Número invalido, por favor informe um número positivo.')
        self.assertFormError(response, 'form', 'ano', 'Informe um número inteiro.')
        response = c.post(reverse('escola:add-turma'), {'numero': 4.5, 'ano': 1936})
        self.assertFormError(response, 'form', 'numero', 'Informe um número inteiro.')
        self.assertFormError(response, 'form', 'ano', 'Ano invalido, por favor informe um ano posterior a 1940.')

    def test_create_with_valid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        response = c.post(reverse('escola:add-turma'), {'numero': 133, 'ano': 2019})
        self.assertRedirects(response, reverse('escola:list-turmas'))

        turma_criada = Turma.objects.get(numero=133)
        assert turma_criada.numero == 133
        assert turma_criada.ano == 2019


class TestListTurmas(TestCase):
    def test_todas_aparecem(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        response = c.get(reverse('escola:list-turmas'))
        self.assertTemplateUsed(response, 'escola/turma/listaTurmas.html')
        self.assertEqual(200, response.status_code)
        assert len(response.context['turmas']) == len(Turma.objects.all())
        for a in range(len(Turma.objects.all())):
            assert response.context['turmas'][a] == Turma.objects.all()[a]


#   TODO: Testa links de permissões
class TestEditTurmas(TestCase):
    def test_permission_anonymous(self):
        c = Client()
        c.logout()
        turma = create_turma()
        response = c.get(reverse('escola:edit-turma', args=[turma.pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:edit-turma', args=[turma.pk, ]))

    def test_permission_user_not_admin(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        turma = create_turma()
        response = c.get(reverse('escola:edit-turma', args=[turma.pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:edit-turma', args=[turma.pk, ]))

    def test_permission_admin(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma = create_turma()
        response = c.get(reverse('escola:edit-turma', args=[turma.pk, ]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'escola/turma/criarForm.html')

    def test_blank_values(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma = create_turma()
        response = c.post(reverse('escola:edit-turma', args=[turma.pk, ]), {})
        self.assertFormError(response, 'form', 'numero', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'ano', 'Este campo é obrigatório.')

    def test_edit_invalid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma = create_turma()
        response = c.post(reverse('escola:edit-turma', args=[turma.pk, ]), {'numero': -12, 'ano': 2.4})
        self.assertFormError(response, 'form', 'numero', 'Número invalido, por favor informe um número positivo.')
        self.assertFormError(response, 'form', 'ano', 'Informe um número inteiro.')
        response = c.post(reverse('escola:edit-turma', args=[turma.pk, ]), {'numero': 4.5, 'ano': 1936})
        self.assertFormError(response, 'form', 'numero', 'Informe um número inteiro.')
        self.assertFormError(response, 'form', 'ano', 'Ano invalido, por favor informe um ano posterior a 1940.')

    def test_edit_with_valid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma = create_turma()
        response = c.post(reverse('escola:edit-turma', args=[turma.pk, ]), {'numero': 133, 'ano': 2019})
        self.assertRedirects(response, reverse('escola:list-turmas'))

        turma_criada = Turma.objects.get(numero=133)
        assert turma_criada.numero == 133
        assert turma_criada.ano == 2019

class TestDeleteTurmas(TestCase):
#   TODO: Testa Permissões
    def test_permission_anonymous(self):
        c = Client()
        c.logout()
        turma = create_turma()
        response = c.get(reverse('escola:delete-turma', args=[turma.pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:delete-turma', args=[turma.pk, ]))


    def test_permission_user_not_admin(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        turma = create_turma()
        response = c.get(reverse('escola:delete-turma', args=[turma.pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:delete-turma', args=[turma.pk, ]))

    def test_permission_admin(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma = create_turma()
        turma_pk = turma.pk
        response = c.get(reverse('escola:delete-turma', args=[turma.pk, ]))
        self.assertRedirects(response, reverse('escola:list-turmas'))
        self.assertRaises(Exception, lambda: Turma.objects.get(pk=turma_pk))
# class TestPopulateAlunos:
#   TODO: Testa com dados invalidos
#   TODO: Testa permissões
#   TODO: Testa com dados, apenas nome e turma
#   TODO: Testa com nome de usuario ja usado
#   TODO: Testa com apenas nome de usuario
# class TestAddCargo:
#   TODO: Testa Permissões
#   TODO: Tenta com dados invalidos
#   TODO: Tenta com dados válidos
# class TestListCargos:
#   TODO: Testa que todas os Cargos da turma aparecem
#   TODO: Testa as permisões dos Links
# class TestEditCargo:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestDeleteCargo:
#   TODO: Testa Permissão
#   TODO: Testa apagar
# class TestAddAluno:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestListAlunos:
#   TODO: Testa que todas aparacem
#   TODO: Testa links de permissões
# class TestVerHorario:
#   TODO: Testa o aparecimento do horario.
# class TestAlterarHorario:
#   TODO: Aparecem apenas materias da turma certa;
# class TestEditAluno:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestDeleteAluno:
#   TODO: Testa Permissão
#   TODO: Testa apagar
# class TestAddProfessor:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestListProfessor:
#   TODO: Testa que todas aparacem
#   TODO: Testa links de permissões
# class TestEditProfessor:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestDeleteProfessor:
#   TODO: Testa Permissão
#   TODO: Testa apagar
# class TestAddMateria:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestListMaterias:
#   TODO: Testa que todas aparacem
#   TODO: Testa links de permissões
# class TestEditMateria:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestDeleteMateria:
#   TODO: Testa Permissão
#   TODO: Testa apagar
# class TestAddTarefa:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestListTarefa:
#   TODO: Testa que todas aparacem
#   TODO: Testa links de permissões
# class TestEditTarefa:
#   TODO: Testa permissões
#   TODO: Testa com dados invalidos
#   TODO: Testa com dados validos
# class TestDeleteTarefa:
#   TODO: Testa Permissão
#   TODO: Testa apagar
class TestConcluirTarefa(TestCase):
    def test_permited(self):
        c = Client()
        turma = create_turma()
        tarefa = mixer.blend(Tarefa, turma=turma, materia=turma.materiadaturma_set.all()[0])
        response = c.get(reverse('escola:concluir-tarefa', args=[tarefa.pk, ]))
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:concluir-tarefa', args=[1, ]))


# class TestDetalhesTarefa:
#   TODO: testa que existe
#   TODO: Testa permisões
#   TODO: Testa que comentarios aparecem
#   TODO: Testa comenta vazio
#   TODO: Testa Comenta valido
# class TestSobre:
#     # Hãn?
#   TODO: Testa que aparece, e que o template coreto foi usado
class TestSeguirManager(TestCase):
    page_name = 'escola:seguir'

    def test_permited(self):
        c = Client()
        c.logout()
        response = c.get(reverse(self.page_name, args=[1, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:seguir', args=[1, ]))

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
        # Garante que foi redirecionado para o lado certo;
        self.assertRedirects(response, reverse('escola:index'))
        # Garante que o usuario esta seguindo o Seguidor;
        assert seguidor.is_seguidor(aluno.user)
