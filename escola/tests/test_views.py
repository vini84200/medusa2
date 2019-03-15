import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

class TestIndex():
    def test_annonymous(self, cl, rf):
        #TODO Continuar testes;