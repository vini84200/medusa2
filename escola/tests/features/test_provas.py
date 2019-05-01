# coding=utf-8
"""Provas feature tests."""

#  Developed by Vinicius José Fritzen
#  Last Modified 01/05/19 09:23.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
from mixer.backend.django import mixer
from pytest_bdd import (
    given,
    scenario,
    then,
)

from escola.models import MateriaDaTurma
from escola.tests.selenium_test_case import CustomWebDriver


@scenario('Frontend/Escola/provas.feature', 'Aluno wants to see his Provas')
def test_aluno_wantspytestbdd_generate_to_see_his_provas():
    """Aluno wants to see his Provas."""


@scenario('Frontend/Escola/provas.feature', 'When Professor wants to create a Prova show Form')
def test_professor_wants_to_create_a_prova():
    """Professor wants to create a Prova."""


@given('a Aluno is logged in')
def aluno_logged(browser, dummy_aluno, live_server):
    """Aluno is logged in."""
    browser.get(live_server.url)
    browser.add_cookie({'name': 'sessionid', 'value': dummy_aluno['cookie'].value, 'secure': False, 'path': '/'})
    browser.refresh()


@given('Professor created a Prova')
def a_professor_created_a_prova():
    """a Professor created a Prova."""
    # mixer.blend(Prova, )
    raise NotImplementedError


@given('a Professor is logged in')
def professor_logged(browser, live_server, dummy_professor):
    """a Professor is logged in."""
    browser.get(live_server.url)
    browser.add_cookie({'name': 'sessionid', 'value': dummy_professor['cookie'].value, 'secure': False, 'path': '/'})
    browser.refresh()
    return dummy_professor


@given('he clicks on the materia of the list')
def he_clicks_on_the_materia_of_the_list(browser: CustomWebDriver):
    """he clicks on the materia of the list."""
    browser.find_element_by_class_name("materia-item").find_elements_by_class_name("materia-name").click()


@given('he clicks the Area do Professor dropdown')
def he_clicks_the_area_do_professor_dropdown(browser):
    """he clicks the Area do Professor dropdown."""
    browser.find_element_by_link_text("Area do Professor").click()


@given('he clicks the link \'Adicionar Prova\'')
def he_clicks_the_link_adicionar_prova(browser):
    """he clicks the link 'Adicionar Prova'."""
    browser.find_element_by_link_text("Adicionar Prova").click()


@given('he has a Materia for him')
def he_has_a_materia_for_him(professor_logged):
    """he has a Materia for him."""
    mixer.blend(MateriaDaTurma, professor=professor_logged['professor'])


@given('he is in the homepage')
def he_is_in_the_homepage(browser, live_server):
    """he is in the homepage."""
    browser.get(live_server.url)


@given('then clicks in the Minhas Materias option in the dropdown')
def then_clicks_in_the_minhas_materias_option_in_the_dropdown(browser):
    """then clicks in the Minhas Materias option in the dropdown."""
    browser.find_element_by_link_text("Minhas Materias").click()


@then('the Aluno should see the Prova in the list')
def the_aluno_should_see_the_prova_in_the_list():
    """the Aluno should see the Prova in the list."""
    raise NotImplementedError


@then('the form of Adicionar Prova shows')
def the_form_of_adicionar_prova_shows():
    """the form of Adicionar Prova shows."""
    raise NotImplementedError

