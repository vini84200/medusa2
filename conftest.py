#  Developed by Vinicius José Fritzen
#  Last Modified 17/04/19 14:28.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import pytest
from decouple import config
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from faker import Faker
from faker.providers import internet, misc
from mixer.backend.django import mixer
from selenium.webdriver.firefox.options import Options

from escola import user_utils
from escola.models import Turma, Horario, MateriaDaTurma, Aluno, CargoTurma
from escola.tests.selenium_test_case import CustomWebDriver
from escola.utils import dar_permissao_user

fake = Faker('pt_BR')
fake.add_provider(internet)
fake.add_provider(misc)

@pytest.fixture(scope='module')
def browser(request):
    """Provide a selenium webdriver instance."""
    # SetUp
    options = Options()
    if config('MOZ_HEADLESS', 0) == 1:
        options.add_argument('-headless')

    browser_: CustomWebDriver = CustomWebDriver(firefox_options=options)

    yield browser_

    # TearDown
    browser_.quit()


username = 'pedrinho'
senha = '123456'


@pytest.fixture()
def pedrinho(db):
    """Add a test user to the database."""
    user_ = user_utils.create_admin_user(username, senha)
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

