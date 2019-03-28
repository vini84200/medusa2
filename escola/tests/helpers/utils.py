import pytest
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from mixer.backend.django import mixer

from escola.models import Turma, Profile, Aluno, Professor, MateriaDaTurma, CargoTurma, Horario
from escola.utils import dar_permissao_user

pytestmark = pytest.mark.django_db


def create_admin():
    user = mixer.blend(User, is_superuser=True)
    return user


def create_aluno(turma=None, user=None):
    if not turma:
        turma = mixer.blend(Turma)
    if user is None:
        user = mixer.blend(User)
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


def create_cargo(user, nivel=None, turma=None):
    if turma is None:
        turma = create_turma()
        a = create_aluno(turma=turma,user=user)

    if nivel is None:
        nivel = 5
    cargo = mixer.blend(CargoTurma, turma=turma, ocupante=user, cod_especial=nivel,
                                          ativo=True)
    dar_permissao_user(user, cargo)
    return cargo


def cargo_muda_ocupante(user, cargo):
    dar_permissao_user(user, cargo)
    return cargo