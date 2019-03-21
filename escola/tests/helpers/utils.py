import pytest
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from mixer.backend.django import mixer

from escola.models import Turma, Profile, Aluno, Professor, Horario, MateriaDaTurma


pytestmark = pytest.mark.django_db

def create_admin():
    user = mixer.blend(User, is_superuser=True)
    return user


def create_aluno(turma=None):
    if not turma:
        turma = mixer.blend(Turma)
    user = mixer.blend(User, turma=turma)
    profile = mixer.blend(Profile, user=user, is_aluno=True, is_professor=False)
    aluno = mixer.blend(Aluno, user=user)
    return aluno


def create_professor():
    user = mixer.blend(User)
    profile = mixer.blend(Profile, user=user, is_aluno=False, is_professor=True)
    professor = mixer.blend(Professor, user=user)
    return professor


def create_turma():
    turma = mixer.blend(Turma, ano=datetime.today().year)
    horario = mixer.blend(Horario, turma=turma)
    aluno = create_aluno(turma=turma)
    prof = create_professor()
    materia = mixer.blend(MateriaDaTurma, professor=prof, turma=turma)
    return turma