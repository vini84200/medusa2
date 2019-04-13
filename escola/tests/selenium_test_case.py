#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 16:04.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import pytest
from decouple import config
from django.contrib.auth.models import User
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait


# @pytest.mark.selenium
class SeleniumTestCase(LiveServerTestCase):
    """
    A base test case for Selenium, providing hepler methods for generating
    clients and logging in profiles.
    """

    def setUp(self):
        options = Options()
        if config('MOZ_HEADLESS', 0) == 1:
            options.add_argument('-headless')

        self.browser = CustomWebDriver(firefox_options=options)

    def tearDown(self):
        self.browser.quit()


class CustomWebDriver(webdriver.Firefox):
    """Our own WebDriver with some helpers added"""

    def find_css(self, css_selector):
        """Shortcut to find elements by CSS. Returns either a list or singleton"""
        elems = self.find_elements_by_css_selector(css_selector)
        found = len(elems)
        if found == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

    def wait_for_css(self, css_selector, timeout=7):
        """ Shortcut for WebDriverWait"""
        return WebDriverWait(self, timeout).until(lambda driver : driver.find_css(css_selector))