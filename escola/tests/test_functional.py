#  Developed by Vinicius José Fritzen
#  Last Modified 28/04/19 08:32.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import time

import pytest
from django.test import TestCase, Client
from mixer.backend.django import mixer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from escola import user_utils
from escola.models import Turma

TIME_LOAD = 2

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


def navigate_navbar(browser, points):
    """Navega no site pela NavBar, envie quais pontos da navbar devem ser selecionados"""
    for p in points:
        browser.find_element_by_link_text(p).click()


def click_button(browser, btn_text):
    """Clica no botão com esse texto"""
    browser.find_element_by_link_text(btn_text).click()


def fill_form_id(browser, fields: dict):
    """Prenche um form usando os valores passados como key como id e value como o que escrever"""
    for field_id, data in fields.items():
        browser.find_css(f'#{field_id}').send_keys(data)

def submit_form(browser):
    """Envia o form da pagina"""
    browser.find_element_by_tag_name('form').find_element_by_name('submit').click()


@pytest.mark.selenium_test
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
    navigate_navbar(browser, ['Escola', 'Lista de Turmas'])
    # Ele chega lá, e vê que há um titulo 'Lista de Turmas'.
    AssertHeader('Lista de Turmas', browser)
    h1 = browser.find_element_by_tag_name('h1')
    tc.assertIn('Lista de Turmas', h1.text, f"Lista de turmas não é o titulo no h1 da pagina, e sim '{h1.text}'")

    # Ele tambem vê um botão, 'Adicionar Turma'.
    click_button(browser, 'Adicionar Turma')

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
    time.sleep(TIME_LOAD)
    # Pedro preciona enter e redirecionado para uma pagina que mostra que seu novo usuario possui uma senha
    # e nome de usuario, pedro os imprime e volta para pagina inicial
    browser.get(live_server.url)
    #Ele está de volta a pagina inicial, de lá ele rapidamente verifica a lista de alunos da turma que ele criou
    navigate_navbar(browser, ['Escola', 'Lista de Turmas'])
    turma_row = browser.find_element_by_class_name('turma_302')
    turma_row.find_element_by_link_text('Alunos').click()

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
    navigate_navbar(browser, ['Escola', 'Lista de Turmas'])

    # e lá ele clica no botão Popular Turmas,
    browser.find_element_by_link_text('Adicionar Lista de Alunos').click()

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

    browser.get(live_server.url)
    # e então volta a lista de alunos
    navigate_navbar(browser, ['Escola', 'Lista de Turmas'])
    turma_row = browser.find_element_by_class_name('turma_302')
    turma_row.find_element_by_link_text('Alunos').click()

    #  e ele está satisfeito, há 4 alunos na lista, todos os nomes que ele havia adicionado.
    ## Um para o header da tebela
    rows = browser.find_elements_by_tag_name('tr')
    assert len(rows) == 5
    AssertAlunoInTheList('Silas S Abdi', '14', browser)
    AssertAlunoInTheList('Eligia A Borkowska', '2', browser)
    AssertAlunoInTheList('Kelsie E Aitken', '3', browser)
    AssertAlunoInTheList('Amanda M Nilsson', '4', browser)
    # Pedro vai adicionar os professores de sua escola
    navigate_navbar(browser, ['Escola', 'Lista de Professores'])
    click_button(browser, 'Adicionar Professor')
    # Ele adiciona 'Maria das Dores' professora de Matematica
    fill_form_id(browser, {
        'id_nome': 'Maria das Dores'
    })
    submit_form(browser)
    # Agora ele vai verificar que sua professora foi adicionada
    browser.get(live_server.url)
    navigate_navbar(browser, ['Escola', 'Lista de Professores'])

    tc.assertIn('Maria das Dores', [row.text for row in browser.find_elements_by_class_name('professor_nome')])
    assert 'Lista de Professores' in browser.title
    # Agora ele adiciona um novo professor
    click_button(browser, 'Adicionar Professor')
    # Ele adiciona 'Patricia Klainir' professora de Geografia
    assert 'Adicionar Professor' in browser.title
    fill_form_id(browser, {
        'id_nome': 'Patricia Klainir'
    })
    submit_form(browser)
    # Agora ele vai verificar que sua professora foi adicionada
    browser.get(live_server.url)
    navigate_navbar(browser, ['Escola', 'Lista de Professores'])
    # Ele verifica que seus dois professores foram adicionados
    tc.assertIn('Maria das Dores', [row.text for row in browser.find_elements_by_class_name('professor_nome')])
    tc.assertIn('Patricia Klainir', [row.text for row in browser.find_elements_by_class_name('professor_nome')])
    # Agora Pedro volta a lista de turmas, e abre a lista de materias
    navigate_navbar(browser, ['Escola', 'Lista de Turmas'])
    turma_row = browser.find_element_by_class_name('turma_302')
    click_button(turma_row, "Materias")
    assert 'Materias da 302' in browser.title
    # Lá ele clica para adicionar uma nova materia 'Matematica' com a professora 'Maria das Dores'
    click_button(browser, 'Adicionar Materia')
    assert 'Adicionar Materia' in browser.title
    fill_form_id(browser, {
        'id_nome': 'Matematica',
        'id_abreviacao': 'MAT'
    })
    s = Select(browser.find_element_by_id('id_professor'))
    s.select_by_visible_text('Maria das Dores')
    submit_form(browser)
    # Tambem adiciona a materia 'Geografia' com a professora 'Patricia Klainir'
    click_button(browser, 'Adicionar Materia')
    fill_form_id(browser, {
        'id_nome': 'Geografia',
        'id_abreviacao': 'GEO'
    })
    s = Select(browser.find_element_by_id('id_professor'))
    s.select_by_visible_text('Patricia Klainir')
    submit_form(browser)

    # Agora Pedro transformara Patricia na Regente da Turma
    navigate_navbar(browser, ['Escola', 'Lista de Turmas'])
    turma_row = browser.find_element_by_class_name('turma_302')
    click_button(turma_row, "Cargos")
    assert 'Cargos da 302' in browser.title
    # Pedro clica em criar cargo
    click_button(browser, 'Adicionar Cargo')
    assert 'Adicionar Cargo' in browser.title
    # Pedro preenche como Regente e adiciona sua professora
    fill_form_id(browser, {
        'id_nome': 'Regente'
    })
    Select(browser.find_element_by_id('id_ocupante')).select_by_visible_text('patricia.pk')
    Select(browser.find_element_by_id('id_cod_especial')).select_by_value('5')
    submit_form(browser)
    navigate_navbar(browser, ['Escola','Lista de Turmas'])
    turma_row = browser.find_element_by_class_name('turma_302')
    click_button(turma_row, "Cargos")
    assert 'patricia.pk' in [r.text for r in browser.find_elements_by_class_name('cargo_ocupante')]
    # Pedro sai de sua conta.
    browser.find_element_by_link_text('Sair').click()


@pytest.fixture()
def dummy_aluno():
    t = mixer.blend(Turma)
    username = 'marcos'
    senha = '12345678'
    nome = 'Marcos das Laranjeiras'
    a = user_utils.create_aluno_user(username, senha, t, nome, 0)
    c = Client()
    c.login(username=username, password=senha)
    cookie = c.cookies['sessionid']
    return {
        'user': a,
        'username': username,
        'senha': senha,
        'nome': nome,
        'turma': t,
        'cookie': cookie,
    }

@pytest.fixture()
def dummy_aluno_lider(dummy_aluno):
    dummy_aluno['turma'].lider = dummy_aluno['user']
    dummy_aluno['turma'].save()
    return dummy_aluno


@pytest.mark.selenium_test
@pytest.mark.live_server_no_flush
def test_novo_aluno_pode_logar(live_server, browser, dummy_aluno):
    """Aluno novo loga no site"""
    tc = TestCase()
    # Marcos ouviu falar do novo site de escola, ele esta curioso sobre esse site e suas funcionalidades
    # Então Marcos acessa o link do site
    browser.get(live_server.url)
    # A primeira coisa que Marcos vê é uma tela de Login muito bonita
    AssertHeader("Login", browser)
    # Marcos preenche as credencias que recebeu
    fill_form_id(browser, {
        'id_username':dummy_aluno['username'],
        'id_password': dummy_aluno['senha']
    })
    submit_form(browser)
    # Ele é redirecionado a pagina inicial,
    AssertHeader("Página Inicial", browser)
    # Na pagina inicial ele vê uma tabela de horarios vazia
    assert "Horario" in [a.text for a in browser.find_elements_by_tag_name('h2')]
    # Tambem ele vê uma tabela de Tarefas
    assert "Tarefas" in [a.text for a in browser.find_elements_by_tag_name('h2')]
    # Ele resolve sair, sua curiosidade foi saciada


@pytest.mark.selenium_test
@pytest.mark.live_server_no_flush
def test_lider_pode_alterar_horario(live_server, browser, dummy_aluno_lider):
    # Jorge é o lider de sua turma, ele acessa o site para definir o horario de sua turma
    ## Defininindo Jorge como logado
    dummy_login(browser, dummy_aluno_lider, live_server)
    # Ele acessa a pagina inicial
    browser.get(live_server.url)
    ht = browser.find_element_by_class_name("horario_table")
    dia = ht.find_element_by_id("turno_1").find_element_by_id('dia_2')
    dia.find_element_by_link_text("Alterar").click()


def dummy_login(browser, dummy_user, live_server):
    browser.get(live_server.url)
    browser.add_cookie({'name': 'sessionid', 'value': dummy_user['cookie'].value, 'secure': False, 'path': '/'})
    browser.refresh()