#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 23:05.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import time

import pytest
from django.test import TestCase
from selenium import webdriver

from escola.tests.selenium_test_case import CustomWebDriver


@pytest.mark.xfail
@pytest.mark.live_server_no_flush
def test_loggin_in_as_admin_and_ading_a_turma_and_alunos_with_both_populate_alunos_and_simple_add(live_server, browser
                                                                                                  , pedrinho):
    """

    :param live_server:
    :param webdriver.Firefox browser:
    :param pedrinho:
    :return:
    """
    tc = TestCase()
    # Pedro, admin e aluno no site de sua escola quer adicionar uma nova turma ao site, no inicio do ano letivo,
    # para isso acessa o site da escola.
    browser.get(live_server.url)
    # O site o redireciona a pagina de login.
    time.sleep(3)
    # Login é o titulo
    AssertHeader('Login', browser)
    # Pedro adiciona sua credenciais e loga no site.
    username_input = browser.find_css('#id_username')
    username_input.send_keys(pedrinho[1])
    senha_input = browser.find_css('#id_password')
    senha_input.send_keys(pedrinho[2])
    button = browser.find_element_by_tag_name('button')
    button.click()
    # Ele é redirecionado a pagina inicial do site,
    time.sleep(3)
    # Pedro Verifica que a pagina possui o titulo de 'Pagina Inicial'
    AssertHeader('Página Inicial', browser)
    # La pedro clica no dropdonw, e então no item que o leva a listagem de turmas
    dropdown = browser.find_element_by_link_text('Escola')
    dropdown.click()
    list_turmas = browser.find_element_by_link_text('Lista de turmas')
    list_turmas.click()
    # Ele chega lá, e vê que há um titulo 'Lista de Turmas'.
    AssertHeader('Lista de Turmas', browser)
    h1 = browser.find_element_by_tag_name('h1')
    tc.assertIn('Lista de Turmas', h1.text, f"Lista de turmas não é o titulo no h1 da pagina, e sim '{h1.text}'")
    # pytest.fail("TERMINAR")

    # Ele tambem vê um botão, 'Adicionar turma'.
    adcionar_turma_btn = browser.find_element_by_link_text('Adicionar Turma')
    adcionar_turma_btn.click()

    # Quando clica no botão, ele é redirecionado a uma pagina com um formulario para adcionar sua propria turma,
    # a pagina possui titulo: 'Adicionar uma turma'
    AssertHeader('Adicionar uma turma', browser)
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


def HeaderWrongMsg(expected, recieved):
    """Retorna uma msg para quando o Title no HEAD da pagina estiver erado"""
    return f"O titulo no HEAD da pagina não é '{expected}', e sim '{recieved}'"


def AssertHeader(expected, recieved_browser: webdriver.Firefox):
    """Verifica que o Title no Head esta coreto"""
    TestCase().assertIn(expected, recieved_browser.title, HeaderWrongMsg(expected, recieved_browser.title))
