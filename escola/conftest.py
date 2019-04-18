#  Developed by Vinicius José Fritzen
#  Last Modified 17/04/19 16:48.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import pytest
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from faker import Faker
from faker.providers import internet, misc
from mixer.backend.django import mixer

from escola import user_utils
from escola.models import Turma, Horario, Aluno, CargoTurma
from escola.utils import dar_permissao_user

fake = Faker('pt_BR')
fake.add_provider(internet)
fake.add_provider(misc)


# Cria coisas


def create_turma():
    turma: Turma = Turma()
    turma.numero = fake.number()
    turma.ano = datetime.today().year
    turma.save()
    horario = mixer.blend(Horario, turma=turma)
    return turma


@pytest.fixture(scope='module')
def create_admin():
    turma = create_turma()
    user = user_utils.create_admin_user(fake.user_name(), fake.password())
    return user


@pytest.fixture(scope='module')
def aluno(*args, **kwargs):
    """

    :keyword turma: Turma do usuario
    :return:
    """
    if kwargs.get('turma'):
        turma = kwargs.get('turma')
    else:
        turma = create_turma()
    aluno = user_utils.create_aluno_user(fake.user_name(), fake.password(), turma, fake.name())
    return aluno


def create_aluno(*args, **kwargs):
    """

    :keyword turma: Turma do usuario
    :return:
    """
    if kwargs.get('turma'):
        turma = kwargs.get('turma')
    else:
        turma = create_turma()
    aluno = user_utils.create_aluno_user(fake.user_name(), fake.password(), turma, fake.name())
    return aluno


def create_aluno_e_turma() -> (User, Turma):
    turma = create_turma()
    aluno = user_utils.create_aluno_user(fake.user_name(), fake.password(), turma, fake.name())
    return aluno, turma


@pytest.fixture(scope='module')
def create_professor():
    professor = user_utils.create_professor_user(fake.user_name(), fake.password(), fake.name())
    return professor


def create_cargo(user: User, nivel: int=None, turma: Turma=None):
    if turma is None:
        turma = create_turma()
        a = create_aluno(turma=turma, user=user)

    if nivel is None:
        nivel = 5
    cargo = mixer.blend(CargoTurma, turma=turma, ocupante=user, cod_especial=nivel,
                                          ativo=True)
    dar_permissao_user(user, cargo)
    return cargo


def cargo_muda_ocupante(user, cargo):
    dar_permissao_user(user, cargo)
    return cargo