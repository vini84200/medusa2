#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 14:46.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import time

from mixer.backend.django import mixer
from django.contrib.auth.models import User

import pytest

from escola.tests.selenium_test_case import SeleniumTestCase

pytestmark = pytest.mark.django_db


class AddingAlunosTest(SeleniumTestCase):

    def setUp(self):
        """Adiciono Usuario user as configs"""
        super(AddingAlunosTest, self).setUp()
        self.username = 'pedrinho'
        self.senha = '123456'
        self.user = mixer.blend(User, username=self.username, password=self.senha, is_staff=True)

    def test_loggin_in_as_admin_and_ading_a_turma_and_alunos_with_both_populate_alunos_and_simple_add(self):
        # Pedro, admin e aluno no site de sua escola quer adicionar uma nova turma ao site, no inicio do ano letivo,
        # para isso acessa o site da escola.
        self.browser.get(self.live_server_url)
        # O site o redireciona a pagina de login.
        time.sleep(3)
        # Login é o titulo
        self.assertIn('Login', self.browser.title, f'O titulo da pagina não é Login, é {self.browser.title}')
        # Pedro adiciona sua credenciais e loga no site.
        username_input = self.browser.find_css('#id_username')
        username_input.send_keys(self.username)
        senha_input = self.browser.find_css('#id_password')
        senha_input.send_keys(self.senha)
        button = self.browser.find_element_by_tag_name('button')
        button.click()
        # Ele é redirecionado a pagina inicial do site,
        time.sleep(3)
        # Pedro Verifica que a pagina possui o titulo de 'Pagina Inicial'
        self.assertIn('Página Inicial', self.browser.title, f'O titulo da pagina não é "Página Inicial", é "{self.browser.title}" ')
        self.fail("Terminar os testes")
        # La pedro clica no item que o leva a listagem de turmas
        # Ele chega lá, e vê que há um titulo 'Lista de Turmas'.
        # Ele tambem vê um botão, adicionar turma.
        # Quando clica no botão, ele é redirecionado a uma pagina com um formulario para adcionar sua propria turma,
        # ele preeche com turma: '302', um terceiro ano de sua escola, e ano '2019', ano letivo que estava começando.
        # Ele aperta enter e é redirecionado a lista de turmas, onde Pedro pode ver que sua turma está na lista,
        # isso alegra Pedro. :D
        # Pedro clica na lista de alunos da turma recem criada. Está um vazio enorme, e Pedro está determinado a muda-lo
        # Pedro clica no link de adicionar aluno, e preenche com o nome de 'Silas S Abdi', anota o n da chamada como 14.
        # Pedro preciona enter e seus olhos brilham quando vê, lá está, na lista que estava vazia, há um nome.
        # O nome que ele adicionara. Pedro precisa adicionar mais nomes, mas ele sabe que adicionar um por vez não
        # sera uma opção, então ele volta a lista de turmas,
        # e lá ele clica no botão Popular Turmas,
        # Quando a pagina carega, ele sorri, ali esta tudo o que ele precisa, uma lista de campos para ele adicionar
        # alunos, ele comeca a adicionar varios:
        # 2 | Eligia A Borkowska | 302
        # 3 | Kelsie E Aitken    | 302
        # 4 | Amanda M Nilsson   | 302
        # E então pedrinho clica em enviar,
        # a pagina recarega, e ele é redirecionado a pagina com a lista de turmas, ele rapidamente clica no botão com a
        # lista de alunos da 302, e ele está satisfeito, há 4 alunos na lista, todos os nomes que ele havia adicionado.
        # Pedro sai de sua conta.
