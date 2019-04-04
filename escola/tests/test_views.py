import pytest
from django.contrib.auth import authenticate
from django.test.client import Client
from django.test.testcases import TestCase
from helpers.utils import create_admin, create_aluno, create_professor, create_turma
from mixer.backend.django import mixer

from escola.models import *

pytestmark = pytest.mark.django_db


# TODO Test username_present()


class Verificaton:
    """Uma verificação de um objeto"""

    def verify(self, *args, **kwargs):
        """Retorna o resultado da verificação"""
        pass


class VerificationResponse(Verificaton):
    """ Uma verificação especifica para uma response """

    def verify(self, response, *args, **kwargs):
        """ Faz a verificação"""
        pass


class VerificationStatusCode(VerificationResponse):
    """Verifica se o resutado é o esperado"""
    expected_code = 0

    def __init__(self, code):
        self.expected_code = code

    def verify(self, response, *args, **kwargs):
        """ Faz a verificação pelo status_code"""
        assert self.expected_code == response.status_code


class Verification200(VerificationStatusCode):
    """Verifica se o status_code é 200"""

    def __init__(self):
        super().__init__(200)


class VerificationTemplate(VerificationResponse):
    """Verifica se o template usado foi o certo"""

    template_path = ""

    def __init__(self, template_path):
        self.template_path = template_path

    def verify(self, response, *args, **kwargs):
        """Faz a verificação"""
        TestCase.assertTemplateUsed(TestCase(), response, self.template_path)


class VerificationLoginInUrl(VerificationResponse):
    """Verifica se a url possui a url de login."""
    login_page = 'login'

    def __init__(self, login_page):
        self.login_page = login_page

    def verify(self, response, *args, **kwargs):
        """Faz a verificação de url de login na url"""
        assert reverse('login') in response.url


class ResponseAssert:
    """Verifica uma resposta com uma list de verifications prefeita"""
    test_list = []
    follow = True

    def __init__(self, *args, **kwargs):
        pass

    def verify(self, response, *args, **kwargs):
        """Realiza a verificação"""
        for test in self.test_list:
            test.verify(response)

    def get_follow(self):
        """ Retorna o valor de follow para o uso quando ocorer o request"""
        return self.follow


class Assert200AndTemplate(ResponseAssert):
    """Verifica o status_code como 200, e que o template seja o mesmo."""

    def __init__(self, template, *args, **kwargs):
        super(Assert200AndTemplate, self).__init__(args, kwargs)
        self.test_list = [Verification200(),
                          VerificationTemplate(template)]


class AssertRedirects(ResponseAssert):
    """Verifica um redirecionamento"""
    pass


class AssertRedirectsLogin(ResponseAssert):
    """Verifica que foi redirecionado para o login"""
    login_pagename = 'login'
    follow = False

    def __init__(self, *args, **kwargs):
        super(AssertRedirectsLogin, self).__init__(args, kwargs)
        self.test_list = [VerificationStatusCode(302)]


class _TestView:
    """Teste generico para views"""
    page_name = ""
    page_parameters = []

    annonymous = ResponseAssert()
    loged_not_escola = ResponseAssert()
    aluno = ResponseAssert()
    professor = ResponseAssert()
    aluno_e_professor = ResponseAssert()
    admin = ResponseAssert()

    def set_up(self):
        """Inicia tudo, é chamada no inicio"""
        pass

    def get_response(self, client, response_assert):
        """ Retorna um response com metodo GET e com dados do response_assert"""
        r = client.get(reverse(self.page_name, args=self.page_parameters), follow=response_assert.get_follow())
        print(r.status_code)
        print(response_assert.test_list)
        return r

    def test_get_annonymous(self):
        """Testa com Anonimo"""
        self.set_up()
        # Get Client
        client = Client()
        # Get response
        response = self.get_response(client, self.annonymous)
        # Test response
        self.annonymous.verify(response)

    def test_get_user_not_escola(self):
        """ Testa com usuario logado, mas não há perfil"""
        self.set_up()
        # Get Client
        client = Client()
        client.login(username='cazuza', password='senha1234')
        # response
        response = self.get_response(client, self.loged_not_escola)
        # test
        self.loged_not_escola.verify(response)

    def test_get_aluno(self):
        """ Teste com usuario logado, com perfil de aluno"""
        self.set_up()
        # Get Client
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        # Response
        response = self.get_response(c, self.aluno)
        # test
        self.aluno.verify(response)

    def test_get_professor(self):
        """ Teste com usuario logado, com perfil de professor"""
        self.set_up()
        # Get Client
        c = Client()
        prof = create_professor()
        c.force_login(prof.user)
        # Response
        response = self.get_response(c, self.professor)
        # tests
        self.professor.verify(response)

    @pytest.mark.skip('Não foi adicionado uma função que permita isso.')
    def test_get_professor_aluno(self):
        """ Teste com usuario logado, com perfil de professor e aluno"""
        # TODO: 04/04/2019 por wwwvi: Adicionar metodo para isso.
        self.set_up()
        # Get Client
        c = Client()
        prof = create_professor()
        c.force_login(prof.user)
        # Response
        response = self.get_response(c, self.aluno_e_professor)
        # tests
        self.professor.verify(response)


class _TestFormView(_TestView):
    pass


class _TestViewOnlyUserEscola(_TestView):
    annonymous = AssertRedirectsLogin()
    loged_not_escola = AssertRedirectsLogin()


class _TestViewEspecificaParaTurma(_TestViewOnlyUserEscola):
    turma = None
    aluno = AssertRedirectsLogin()
    aluno_turma = ResponseAssert()
    aluno_e_professor = ResponseAssert()

    def set_up(self):
        """Inicia a turma"""
        super(_TestViewEspecificaParaTurma, self).set_up()
        self.turma = create_turma()

    def test_get_aluno(self):
        """ Teste com usuario logado, com perfil de aluno"""
        self.set_up()
        # Get Client
        c = Client()
        aluno = create_aluno(turma=self.turma)
        c.force_login(aluno.user)
        # Response
        response = self.get_response(c, self.aluno_turma)
        # test
        self.aluno_turma.verify(response)


class _TestFormViewEspecificoTurma(_TestViewEspecificaParaTurma, _TestFormView):
    def set_up(self):
        super(_TestFormViewEspecificoTurma, self).set_up()


class _TestViewEspecificoModel(_TestView):
    obj_class = None
    obj = None

    def set_up(self):
        """Cria objeto necessario"""
        super(_TestViewEspecificoModel, self).set_up()
        self.obj = mixer.blend(self.obj_class)


# --------------------------------------------------
#
#   Inicio dos Testes Propriamente ditos
#
# ------------------------------------------------
#


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

    def _test_aparece_notificacoes(self):
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

    def _test_notificacao_bar_nenhuma_noti(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Você não tem notificações.')

    def _test_notificacao_bar_uma_noti(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        mixer.blend(Notificacao, user=aluno.user, visualizado=False)
        response = c.get(reverse(self.page_name))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Você tem 1 notificação.')

    def _test_notificacao_bar_duas_noti(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        mixer.blend(Notificacao, user=aluno.user, visualizado=False)
        mixer.blend(Notificacao, user=aluno.user, visualizado=False)
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
        self.assertFormError(response, 'form', 'numero', 'Por favor, digite um valor positivo')
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
        self.assertFormError(response, 'form', 'numero', 'Por favor, digite um valor positivo')
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
class TestAddCargo(TestCase):
    def test_permission_anonymous(self):
        c = Client()
        c.logout()
        turma__pk = create_turma().pk
        response = c.get(reverse('escola:add-cargo', args=[turma__pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:add-cargo', args=[turma__pk, ]))

    def test_permission_user_not_admin(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        turma__pk = create_turma().pk
        response = c.get(reverse('escola:add-cargo', args=[turma__pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:add-cargo', args=[turma__pk, ]))

    def test_permission_admin(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        response = c.get(reverse('escola:add-cargo', args=[create_turma().pk, ]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'escola/cargos/formCargos.html')

    def test_blank_values(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        response = c.post(reverse('escola:add-cargo', args=[create_turma().pk, ]), {})
        self.assertFormError(response, 'form', 'nome', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'ocupante', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'cod_especial', 'Este campo é obrigatório.')

    def test_create_invalid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        response = c.post(reverse('escola:add-cargo', args=[create_turma().pk, ]), {'nome': 12, 'ocupante': 2.4,
                                                                                    'cod_especial': 'ola', 'ativo': 2})
        self.assertFormError(response, 'form', 'ocupante',
                             'Faça uma escolha válida. Sua escolha não é uma das disponíveis.')
        self.assertFormError(response, 'form', 'cod_especial',
                             'Faça uma escolha válida. ola não é uma das escolhas disponíveis.')

    def test_create_with_valid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        profe = create_professor()
        turma__pk = create_turma().pk
        response = c.post(reverse('escola:add-cargo', args=[turma__pk, ]),
                          {'nome': 'Regencia', 'ocupante': profe.user.pk.__str__(),
                           'cod_especial': '5', 'ativo': 'True'})
        self.assertRedirects(response, reverse('escola:list-cargos', args=[turma__pk, ]))

        cargo_criado: CargoTurma = CargoTurma.objects.get(nome='Regencia')
        assert cargo_criado.turma is not None
        assert cargo_criado.nome == 'Regencia'
        assert cargo_criado.ativo is True
        assert cargo_criado.cod_especial == 5
        assert cargo_criado.ocupante == profe.user


class TestListCargos(TestCase):
    def test_todas_aparecem(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        turma = create_turma()
        response = c.get(reverse('escola:list-cargos', args=[turma.pk, ]))
        self.assertTemplateUsed(response, 'escola/cargos/listCargos.html')
        self.assertEqual(200, response.status_code)
        assert len(response.context['cargos']) == len(CargoTurma.objects.filter(turma=turma))
        for a in range(len(CargoTurma.objects.filter(turma=turma))):
            assert response.context['cargos'][a] == CargoTurma.objects.filter(turma=turma)[a]


#   TODO: Testa as permisões dos Links
class TestEditCargo(TestCase):
    def test_permission_anonymous(self):
        c = Client()
        c.logout()
        cargo = mixer.blend(CargoTurma)
        response = c.get(reverse('escola:edit-cargo', args=[cargo.pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:edit-cargo', args=[cargo.pk, ]))

    def test_permission_user_not_admin(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        cargo = mixer.blend(CargoTurma)
        response = c.get(reverse('escola:edit-cargo', args=[cargo.pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:edit-cargo', args=[cargo.pk, ]))

    def test_permission_admin(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        cargo = mixer.blend(CargoTurma)
        response = c.get(reverse('escola:edit-cargo', args=[cargo.pk, ]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'escola/cargos/formCargos.html')

    def test_blank_values(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        cargo = mixer.blend(CargoTurma)
        response = c.post(reverse('escola:edit-cargo', args=[cargo.pk, ]), {})
        self.assertFormError(response, 'form', 'nome', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'ocupante', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'cod_especial', 'Este campo é obrigatório.')

    def test_create_invalid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        cargo = mixer.blend(CargoTurma)
        response = c.post(reverse('escola:edit-cargo', args=[cargo.pk, ]), {'nome': 12, 'ocupante': 2.4,
                                                                            'cod_especial': 'ola', 'ativo': 2})
        self.assertFormError(response, 'form', 'ocupante',
                             'Faça uma escolha válida. Sua escolha não é uma das disponíveis.')
        self.assertFormError(response, 'form', 'cod_especial',
                             'Faça uma escolha válida. ola não é uma das escolhas disponíveis.')

    def test_create_with_valid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        profe = create_professor()
        turma = create_turma()
        cargo = mixer.blend(CargoTurma, turma=turma)
        response = c.post(reverse('escola:edit-cargo', args=[cargo.pk, ]),
                          {'nome': 'Regencia', 'ocupante': profe.user.pk.__str__(),
                           'cod_especial': '5', 'ativo': 'True'})
        self.assertRedirects(response, reverse('escola:list-cargos', args=[turma.pk, ]))

        cargo_criado: CargoTurma = CargoTurma.objects.get(nome='Regencia')
        assert cargo_criado.turma is not None
        assert cargo_criado.nome == 'Regencia'
        assert cargo_criado.ativo is True
        assert cargo_criado.cod_especial == 5
        assert cargo_criado.ocupante == profe.user


class TestDeleteCargo(TestCase):
    def test_permission_anonymous(self):
        c = Client()
        c.logout()
        cargo = mixer.blend(CargoTurma)
        response = c.get(reverse('escola:delete-cargo', args=[cargo.pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:delete-cargo', args=[cargo.pk, ]))

    def test_permission_user_not_admin(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        cargo = mixer.blend(CargoTurma)
        response = c.get(reverse('escola:delete-cargo', args=[cargo.pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:delete-cargo', args=[cargo.pk, ]))

    def test_permission_admin(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma = create_turma()
        turma_pk = turma.pk
        cargo = mixer.blend(CargoTurma, turma=turma)
        cargo_pk = cargo.pk
        response = c.get(reverse('escola:delete-cargo', args=[cargo.pk, ]))
        self.assertRedirects(response, reverse('escola:list-cargos', args=[turma_pk, ]))
        self.assertRaises(Exception, lambda: CargoTurma.objects.get(pk=cargo_pk))


class TestAddAluno(TestCase):
    def test_permission_anonymous(self):
        c = Client()
        c.logout()
        turma__pk = create_turma().pk
        response = c.get(reverse('escola:add-aluno', args=[turma__pk, ]), follow=True)
        # self.assertEqual(403, response.status_code)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:add-aluno', args=[turma__pk, ]))

    def test_permission_user_not_admin(self):
        c = Client()
        aluno = create_aluno()
        c.force_login(aluno.user)
        turma__pk = create_turma().pk
        response = c.get(reverse('escola:add-aluno', args=[turma__pk, ]), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('escola:add-aluno', args=[turma__pk, ]))

    def test_permission_admin(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma__pk = create_turma().pk
        response = c.get(reverse('escola:add-aluno', args=[turma__pk, ]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'escola/alunos/formAlunosCreate.html')

    def test_allows_prof_regente(self):
        c = Client()
        prof = create_professor()
        c.force_login(prof.user)
        turma = create_turma()
        cargo = mixer.blend(CargoTurma, turma=turma, ocupante=prof.user, cod_especial=5, ativo=True)
        assign_perm('escola.can_add_aluno', prof.user, turma)  # FIXME ISSO NÃO DEVE ACONTECER AQUI
        turma__pk = turma.pk
        response = c.get(reverse('escola:add-aluno', args=[turma__pk, ]))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'escola/alunos/formAlunosCreate.html')

    def test_blank_values(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma__pk = create_turma().pk
        response = c.post(reverse('escola:add-aluno', args=[turma__pk, ]), {})
        self.assertFormError(response, 'form', 'num_chamada', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'nome', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'turma', 'Este campo é obrigatório.')

    def test_create_invalid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma = create_turma()
        turma__pk = turma.pk
        response = c.post(reverse('escola:add-aluno', args=[turma__pk, ]),
                          {'num_chamada': 'KUHAKU', 'nome': 1341, 'turma': 'PEDRO'})
        self.assertFormError(response, 'form', 'num_chamada', 'Informe um número inteiro.')
        self.assertFormError(response, 'form', 'turma', 'Informe um número inteiro.')
        user = create_aluno().user
        response = c.post(reverse('escola:add-aluno', args=[turma__pk, ]),
                          {'num_chamada': 'KUHAKU', 'nome': 1341, 'username': user.username, 'senha': '1',
                           'turma': 'PEDRO'})
        self.assertFormError(response, 'form', 'num_chamada', 'Informe um número inteiro.')
        self.assertFormError(response, 'form', 'turma', 'Informe um número inteiro.')
        self.assertFormError(response, 'form', 'username', 'Este nome de usuario já existe, use outro.')
        self.assertFormError(response, 'form', 'senha', 'Esta senha é muito curta. Ela precisa conter pelo menos 8 '
                                                        'caracteres.')
        self.assertFormError(response, 'form', 'senha', 'Esta senha é muito comum.')
        self.assertFormError(response, 'form', 'senha', 'Esta senha é inteiramente numérica.')

    def test_create_with_valid(self):
        c = Client()
        admin = create_admin()
        c.force_login(admin)
        turma = create_turma()
        turma__pk = turma.pk
        response = c.post(reverse('escola:add-aluno', args=[turma.pk, ]),
                          {'num_chamada': 12, 'nome': 'Pedro Alvares Cabral', 'turma': turma.numero})
        print(response)
        self.assertEqual(200, response.status_code)

        aluno_criado = Aluno.objects.get(nome='Pedro Alvares Cabral')
        usuario_criado = aluno_criado.user
        assert aluno_criado.nome == 'Pedro Alvares Cabral'
        assert aluno_criado.chamada == 12
        assert usuario_criado == User.objects.get(username=response.context['usuarios'][0][0])
        assert authenticate(username=response.context['usuarios'][0][0],
                            password=response.context['usuarios'][0][1]).pk == usuario_criado.pk
        assert aluno_criado.turma == turma
        assert aluno_criado.user.profile_escola.is_aluno
        assert not aluno_criado.user.profile_escola.is_professor

        response = c.post(reverse('escola:add-aluno', args=[turma.pk, ]),
                          {'num_chamada': 12, 'nome': 'Thomas C Marshall', 'turma': turma.numero,
                           'username': 'thomis6343', 'senha': 'vc3hz0atu'})
        print(response)

        self.assertRedirects(response, reverse('escola:list-alunos', args=[turma__pk, ]))

        aluno_criado = Aluno.objects.get(nome='Thomas C Marshall')
        usuario_criado = aluno_criado.user
        assert aluno_criado.nome == 'Thomas C Marshall'
        assert aluno_criado.chamada == 12
        assert usuario_criado.username == 'thomis6343'
        assert authenticate(username='thomis6343',
                            password='vc3hz0atu').pk == usuario_criado.pk
        assert aluno_criado.turma == turma
        assert aluno_criado.user.profile_escola.is_aluno
        assert not aluno_criado.user.profile_escola.is_professor


class TestListAlunos(_TestView, TestCase):
    page_name = 'escola:list-alunos'

    annonymous = AssertRedirectsLogin()
    loged_not_escola = AssertRedirectsLogin()
    aluno = Assert200AndTemplate('escola/alunos/listAlunosPerTurma.html')
    professor = Assert200AndTemplate('escola/alunos/listAlunosPerTurma.html')

    def set_up(self):
        """ Prepara adicionando a turma aos parametros"""
        super(TestListAlunos, self).set_up()
        self.page_parameters = [create_turma().pk, ]


class TestVerHorario(_TestViewEspecificaParaTurma, TestCase):
    page_name = 'escola:show-horario'
    aluno_turma = Assert200AndTemplate('escola/horario/mostraHorario.html')
    professor = Assert200AndTemplate('escola/horario/mostraHorario.html')
    aluno_e_professor = Assert200AndTemplate('escola/horario/mostraHorario.html')

    def set_up(self):
        """Prepara adicionando a turma aos parametros"""
        super(TestVerHorario, self).set_up()
        self.page_parameters = [self.turma.pk, ]


#   TODO: Testa o aparecimento do horario.

class TestAlterarHorario(_TestFormViewEspecificoTurma, TestCase):
    page_name = 'escola:alterar-horario'
    aluno_turma = Assert200AndTemplate('escola/horario/mostraHorario.html')
    professor = Assert200AndTemplate('escola/horario/mostraHorario.html')
    aluno_e_professor = Assert200AndTemplate('escola/horario/mostraHorario.html')

    def set_up(self):
        """Prepara adicionando a turma aos parametros"""
        super(TestAlterarHorario, self).set_up()
        self.page_parameters = [self.turma.pk, 0, 0]
    # TODO: 04/04/2019 por wwwvi: Adicionar coisas de forms.


#   TODO: Aparecem apenas materias da turma certa;
class TestDeleteAluno(_TestViewEspecificoModel, TestCase):
    obj_class = Aluno
    page_name = 'escola:delete-aluno'
    aluno = AssertRedirects()

    def set_up(self):
        super(TestDeleteAluno, self).set_up()
        self.page_parameters = [self.obj.pk, ]


#   TODO: Testa Permissão
#   TODO: Testa apagar
class TestAddProfessor(_TestView, TestCase):
    page_name = 'escola:add-professor'
    aluno = AssertRedirectsLogin()
    professor = AssertRedirectsLogin()



    def set_up(self):
        super(TestAddProfessor, self).set_up()
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
