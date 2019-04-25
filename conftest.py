#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 14:26.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import pytest
from decouple import config
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from rolepermissions.roles import assign_role
from selenium.webdriver.firefox.options import Options

from escola.tests.selenium_test_case import CustomWebDriver


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
    client.login(email=TESTEMAIL, password=TESTPASSWORD)
    cookie = client.cookies['sessionid']

    browser.get(live_server.url)
    browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    browser.refresh()

    return browser