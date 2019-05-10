#  Developed by Vinicius José Fritzen
#  Last Modified 04/05/19 17:45.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

# coding=utf-8
"""Aviso de email feature tests."""
from django.urls import reverse
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers)


@scenario('Frontend/Escola/aviso_email.feature', 'Usuario preenche email')
def test_usuario_preenche_email():
    """Usuario preenche email."""
    pass


@scenario('Frontend/Escola/aviso_email.feature', 'Usuario tem formulario')
def test_usuario_tem_formulario():
    """Usuario tem formulario."""
    pass


@scenario('Frontend/Escola/aviso_email.feature', 'Usuario vê aviso')
def test_usuario_ve_aviso():
    """Usuario vê aviso."""
    pass


@given('a user is logged in')
def a_user_is_logged_in(browser,live_server, dummy_aluno):
    """a user is logged in."""
    browser.visit(live_server.url)
    # browser.add_cookie({'name': 'sessionid', 'value': dummy_aluno['cookie'].value, 'secure': False, 'path': '/'})
    browser.cookies.add({'sessionid': dummy_aluno['cookie'].value})
    browser.reload()

@when(parsers.cfparse('Enters the page \'{page:Page}\'', extra_types=dict(Page=str)))
@given(parsers.cfparse('enters the page \'{page:Page}\'', extra_types=dict(Page=str)))
def enters_the_page(page, browser, live_server):
    """enters the page."""
    browser.visit(live_server.url + reverse(page))


@given('he doesn\'t have a email')
def he_doesnt_have_a_email():
    """he doesn't have a email."""
    raise NotImplementedError


@when('fill the field \'email\' with \'teste@ok.com\'')
def fill_the_field_email_with_testeokcom():
    """fill the field 'email' with 'teste@ok.com'."""
    raise NotImplementedError


@when('he is in the homepage')
def he_is_in_the_homepage():
    """he is in the homepage."""
    raise NotImplementedError


@when('submit the form')
def submit_the_form():
    """submit the form."""
    raise NotImplementedError


@then('a form should load')
def a_form_should_load():
    """a form should load."""
    raise NotImplementedError


@then('a link in the warning, to change his email')
def a_link_in_the_warning_to_change_his_email():
    """a link in the warning, to change his email."""
    raise NotImplementedError


@then('he is redirected to a page with confirmation message')
def he_is_redirected_to_a_page_with_confirmation_message():
    """he is redirected to a page with confirmation message."""
    raise NotImplementedError


@then('he sees a warning about his email')
def he_sees_a_warning_about_his_email():
    """he sees a warning about his email."""
    raise NotImplementedError
