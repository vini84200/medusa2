#  Developed by Vinicius José Fritzen
#  Last Modified 28/04/19 16:28.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging
from pathlib import Path

import pytest
from decouple import config
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client
from mixer.backend.django import mixer
from rolepermissions.roles import assign_role
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from escola import user_utils
from escola.models import Turma
from escola.tests.selenium_test_case import CustomWebDriver

logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def browser(request):
    """Provide a selenium webdriver instance."""
    # SetUp
    options = Options()
    if config('MOZ_HEADLESS', 0) == 1:
        options.add_argument('-headless')

    browser_: CustomWebDriver = CustomWebDriver(options=options)
    failed_before = request.session.testsfailed
    logger.info(f"Yielding browser, failed before: {failed_before}")
    yield browser_
    logger.info(f"Retornou o browser, failed: {request.session.testsfailed}")
    if request.session.testsfailed != failed_before:
        test_name = request.node.name
        take_screenshot(browser_, test_name)
    # TearDown
    browser_.quit()


def take_screenshot(browser: webdriver.firefox, test_name: str):
    screenshots_dir = Path("Logs/Screenshots/funcional_tests")
    screenshot_file_path = screenshots_dir / (test_name.replace('/', '_').replace('.py', '') + ".png")
    print("Path to screnshot: '{}'".format(screenshot_file_path))
    l = browser.save_screenshot(
        screenshot_file_path.absolute().resolve().__str__()
    )
    if not l:
        logger.warning("Couldn't take screnshot for some reason.")
    else:
        logger.info("Screnshot taken! Path: '{}'".format(screenshot_file_path))

username = 'pedrinho'
senha = '123456'


@pytest.fixture()
def pedrinho(db):
    """Add a test user to the database."""
    user_ = mixer.blend(User,
        name='Pedrinho',
        username=username,
        password=make_password(senha),
        is_staff = True,
        )
    assign_role(user_, 'admin')
    return user_, username, senha


@pytest.fixture()
def authenticated_pedrinho_browser(browser, client, live_server, pedrinho):
    """Return a browser instance with logged-in user session."""
    client.login(username=username, password=senha)
    cookie = client.cookies['sessionid']

    browser.get(live_server.url)
    browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    browser.refresh()

    return browser

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


@pytest.fixture()
def dummy_professor():
    username = 'teixeira'
    senha = '12345678'
    nome = 'Teixeira das Laranjeiras'
    a = user_utils.create_professor_user(username, senha, nome)
    c = Client()
    c.login(username=username, password=senha)
    cookie = c.cookies['sessionid']
    return {
        'user': a,
        'username': username,
        'senha': senha,
        'nome': nome,
        'cookie': cookie,
        'professor': a.professor,
    }
