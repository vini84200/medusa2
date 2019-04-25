#  Developed by Vinicius José Fritzen
#  Last Modified 22/04/19 19:27.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import time

import pytest
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from escola.tests.selenium_test_case import CustomWebDriver

TIME_LOAD = 2


@pytest.mark.xfail(reason="Not finished")
@pytest.mark.live_server_no_flush
def test_loggin_in_as_admin_and_ading_a_turma_and_alunos_with_both_populate_alunos_and_simple_add(live_server, browser,
                                                                                                   pedrinho):
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
    # ele preeche com turma: '302', um terceiro ano de sua escola, e o ano, '2019', já estava preenchido. ano letivo que estava começando.
    browser.find_css('#id_numero').send_keys('302')
    assert browser.find_css('#id_ano').get_property('value') == '2019'
    # Ele aperta enter e é redirecionado a lista de turmas,
    browser.find_css('#id_ano').send_keys(Keys.ENTER)
    # onde Pedro pode ver que sua turma está na lista, isso alegra Pedro. :D
    time.sleep(TIME_LOAD)
    turma_row = browser.find_element_by_class_name('turma_302')
    n_turma = turma_row.find_element_by_class_name('turma_n')
    tc.assertEqual('302', n_turma.text)
    # Pedro clica na lista de alunos da turma recem criada.
    turma_row.find_element_by_link_text('Alunos').click()
    # Está um vazio enorme, e Pedro está determinado a muda-lo
    rows = browser.find_elements_by_tag_name('tr')
    ## Um para o header da tebela
    assert len(rows) == 1
    # Pedro clica no link de adicionar aluno,
    browser.find_element_by_link_text('Adicionar Aluno').click()
    # e preenche com o nome de 'Silas S Abdi', anota o n da chamada como 14.
    browser.find_css('#id_num_chamada').send_keys('14')
    browser.find_css('#id_nome').send_keys('Silas S Abdi')
    browser.find_css('#id_nome').send_keys(Keys.ENTER)
    # Pedro preciona enter e redirecionado para uma pagina que mostra que seu novo usuario possui uma senha
    # e nome de usuario, pedro os imprime e volta para pagina inicial
    browser.get(live_server.url)
    #Ele está de volta a pagina inicial, de lá ele rapidamente verifica a lista de alunos da turma que ele criou
    dropdown = browser.find_element_by_link_text('Escola')
    dropdown.click()
    list_turmas = browser.find_element_by_link_text('Lista de turmas')
    list_turmas.click()
    time.sleep(TIME_LOAD)
    turma_row = browser.find_element_by_class_name('turma_302')
    turma_row.find_element_by_link_text('Alunos').click()
    time.sleep(TIME_LOAD)
    # e seus olhos brilham quando vê, lá está, na lista que estava vazia, há um nome.
    rows = browser.find_elements_by_tag_name('tr')
    ## Um para o header da tebela
    assert len(rows) == 2
    alunos_n = browser.find_elements_by_class_name('aluno_n')
    tc.assertIn('14', [n.text for n in alunos_n])
    alunos_nome = browser.find_elements_by_class_name('aluno_nome')
    tc.assertIn('Silas S Abdi', [row.text for row in alunos_nome])
    # O nome que ele adicionara. Pedro precisa adicionar mais nomes, mas ele sabe que adicionar um por vez não
    # sera uma opção, então ele volta a lista de turmas,
    dropdown = browser.find_element_by_link_text('Escola')
    dropdown.click()
    list_turmas = browser.find_element_by_link_text('Lista de turmas')
    list_turmas.click()
    time.sleep(TIME_LOAD)
    # e lá ele clica no botão Popular Turmas,
    browser.find_element_by_link_text('Adicionar Lista de Alunos').click()
    time.sleep(TIME_LOAD)
    # Quando a pagina carega, ele sorri, ali esta tudo o que ele precisa, uma lista de campos para ele adicionar
    # alunos, ele comeca a adicionar varios:
    # 2 | Eligia A Borkowska | 302
    ## time.sleep(30)
    browser.find_element_by_name('form-0-num_chamada').send_keys('2')
    browser.find_element_by_name('form-0-nome').send_keys('Eligia A Borkowska')
    browser.find_element_by_name('form-0-turma').send_keys('302')
    # 3 | Kelsie E Aitken    | 302
    browser.find_element_by_name('form-1-num_chamada').send_keys('3')
    browser.find_element_by_name('form-1-nome').send_keys('Kelsie E Aitken')
    browser.find_element_by_name('form-1-turma').send_keys('302')
    # 4 | Amanda M Nilsson   | 302
    browser.find_element_by_name('form-2-num_chamada').send_keys('4')
    browser.find_element_by_name('form-2-nome').send_keys('Amanda M Nilsson')
    browser.find_element_by_name('form-2-turma').send_keys('302')
    # E então pedrinho clica em enviar,
    browser.find_css('#submit-id-submit').click()
    # ele vê então uma pagina com senhas e cartões para serem distribuidos, ele esta feliz,
    # ele mais uma vez volta a pagina inicial
    time.sleep(TIME_LOAD)
    browser.get(live_server.url)
    # e então volta a lista de alunos
    dropdown = browser.find_element_by_link_text('Escola')
    dropdown.click()
    list_turmas = browser.find_element_by_link_text('Lista de turmas')
    list_turmas.click()
    turma_row = browser.find_element_by_class_name('turma_302')
    turma_row.find_element_by_link_text('Alunos').click()
    time.sleep(TIME_LOAD)
    #  e ele está satisfeito, há 4 alunos na lista, todos os nomes que ele havia adicionado.
    ## Um para o header da tebela
    rows = browser.find_elements_by_tag_name('tr')
    assert len(rows) == 5
    AssertAlunoInTheList('Silas S Abdi', '14', browser)
    AssertAlunoInTheList('Eligia A Borkowska', '2', browser)
    AssertAlunoInTheList('Kelsie E Aitken', '3', browser)
    AssertAlunoInTheList('Amanda M Nilsson', '4', browser)
    # Pedro sai de sua conta.
    browser.find_element_by_link_text('Sair').click()


def HeaderWrongMsg(expected, recieved):
    """Retorna uma msg para quando o Title no HEAD da pagina estiver erado"""
    return f"O titulo no HEAD da pagina não é '{expected}', e sim '{recieved}'"


def AssertHeader(expected, recieved_browser: webdriver.Firefox):
    """Verifica que o Title no Head esta coreto"""
    TestCase().assertIn(expected, recieved_browser.title, HeaderWrongMsg(expected, recieved_browser.title))


def AssertAlunoInTheList(nome, num, browser):
    tc = TestCase()
    alunos_n = browser.find_elements_by_class_name('aluno_n')
    tc.assertIn(num, [n.text for n in alunos_n])
    alunos_nome = browser.find_elements_by_class_name('aluno_nome')
    tc.assertIn(nome, [row.text for row in alunos_nome])
 