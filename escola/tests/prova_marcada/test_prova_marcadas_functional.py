import logging
import time

import pytest

# Helpers
from django.test import TestCase


def HeaderWrongMsg(expected, recieved):
    """Retorna uma msg para quando o Title no HEAD da pagina estiver erado"""
    return f"O titulo no HEAD da pagina não é '{expected}', e sim '{recieved}'"


def AssertHeader(expected, recieved_browser):
    """Verifica que o Title no Head esta coreto"""
    TestCase().assertIn(expected, recieved_browser.title, HeaderWrongMsg(expected, recieved_browser.title))


def dummy_login(browser, dummy_user, live_server):
    browser.visit(live_server.url)
    # O site o redireciona a pagina de login.
    # Login é o titulo
    AssertHeader('Login', browser)
    # Pedro adiciona sua credenciais e loga no site.
    username_input = browser.find_by_css('#id_username')[0]
    username_input.type(dummy_user['username'])
    senha_input = browser.find_by_css('#id_password')
    senha_input.type(dummy_user['senha'])
    button = browser.find_by_tag('button')
    button.click()
    # Ele é redirecionado a pagina inicial do site,
    # Pedro Verifica que a pagina possui o titulo de 'Pagina Inicial'
    AssertHeader('Página Inicial', browser)

# Testes


@pytest.mark.xfail()
@pytest.mark.selenium_test
@pytest.mark.live_server_no_flush
def test_ver_datas_e_marcar_uma(dummy_professor, live_server, browser):
    # A Joana, uma professora de sua escola, precisa marcar uma prova com sua turma, ela entra na sua plataforma,
    dummy_login(browser, dummy_professor, live_server)
    # ela observa que está na página inicial já que havia logado anteriormente. Ela abre a vê na página inicial uma
    AssertHeader("Página Inicial", browser)
    # lista de turmas do dia num painel com título escrito ’Resumo de Hoje’, com um subpainel ‘Turmas de Hoje’.
    assert browser.is_element_present_by_id('section-resumo-professor')
    browser.find_by_id('section-resumo-professor').is_element_present_by_id('div-turmas-hoje')
    # Ela aperta no primeiro botão ‘Química/203’
    assert browser.find_by_id('section-resumo-professor').find_by_id('div-turmas-hoje').is_text_present('Química/203')
    browser.find_by_id('section-resumo-professor').find_by_id('div-turmas-hoje').click_link_by_text('Química/203')
    # e é levada a uma página onde ela pode ver algumas informações,

    # e em um painel lateral ela vê um botão ‘Escolher data para marcar prova’, ela clica ali e é levada a uma página com título
    # ‘Datas livres da 203’ e embaixo há um calendário, o mês é o mesmo que o atual, datas passadas estão em cinza, já a
    # data atual em azul, as datas que o professor tem aula com a  turma em verde, já outras datas em branco.
    # Se houvesse alguma prova marcada estaria em vermelho. Cada data tem espaço para seus eventos, como provas, e
    # um botão escrito ‘Marcar prova’. Joana clica no botão do dia da próxima aula, e então a página é redirecionada
    # para uma página com título Marcar uma prova’, há alguns campos, o da data e da matéria já estão preenchidos com
    # os valores corretos, ela preenche o resto, como o nome de ‘Prova de Química’, preenche a descrição com ‘Prova
    # simples de Quimica’, e clica no botão ‘Marcar’. Ela é redirecionada a pagina inicial. Patricia abre um segundo
    # browser, e loga no seu usuario, ela está na sua pagina inicial, no final da pagina na lista de provas,
    # ela vê a prova que foi adicionada na lista.
    pass



