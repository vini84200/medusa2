from django.http import HttpResponseRedirect
from django.test.client import Client
import pytest
from mixer.backend.django import mixer
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestIndex:
    def test_annonymous(self, client: Client, rf):
        response = client.get(reverse('escola:index'), follow=False)
        assert response.status_code == 302, 'Caso um usario não logue deve ser redirecionado'
        assert reverse('login') in response.url
