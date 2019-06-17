import pytest
from mixer.backend.django import mixer

from escola.models import Turma

pytestmark = pytest.mark.django_db

def test_get_or_create_horario():
    turma:Turma = mixer.blend(Turma)
    a = turma.get_or_create_horario()
    b = turma.get_or_create_horario()
    assert a==b