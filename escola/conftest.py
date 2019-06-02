#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from mixer.backend.django import mixer

from .models import Turma, MateriaDaTurma, ProvaMateriaMarcada, ProvaAreaMarcada, AreaConhecimento
from .user_utils import create_aluno_user, create_professor_user, create_user

pytestmark = pytest.mark.django_db


@pytest.fixture
def client(request):
    return Client()


@pytest.fixture
def anonymous_client(request, client):
    return client


@pytest.fixture
def turma(request):
    turma = mixer.blend(Turma)
    return turma


@pytest.fixture
def aluno(request, faker, turma) -> User:
    aluno = create_aluno_user(faker.user_name(), faker.password(), turma, faker.name())
    return aluno


@pytest.fixture
def aluno_client(request, client: Client, aluno):
    client.force_login(aluno)
    return client


@pytest.fixture
def tc(request):
    return TestCase()


@pytest.fixture
def professor(request, faker, turma):
    professor_user = create_professor_user(faker.user_name(), faker.password(), faker.name())
    mixer.blend(MateriaDaTurma, area=mixer.blend(AreaConhecimento, turma=turma), turma=turma, professor=professor_user.professor)
    return professor_user


@pytest.fixture
def professor_client(request, professor, client: Client):
    client.force_login(professor)
    return client


@pytest.fixture
def materia(request, turma):
    return mixer.blend(MateriaDaTurma, area=mixer.blend(AreaConhecimento, turma=turma), turma=turma)


@pytest.fixture
def area(request, turma):
    return mixer.blend(AreaConhecimento, turma=turma)


@pytest.fixture
def user(request, faker):
    return create_user(faker.user_name(), faker.password())


@pytest.fixture
def prova_marcada_materia(request, materia, faker, user):
    return ProvaMateriaMarcada.create(materia, faker.sentence(), faker.date_time(), faker.paragraph(), user)


@pytest.fixture
def prova_marcada_area(request, area, faker, user):
    return ProvaAreaMarcada.create(area, faker.sentence(), faker.date_time(), faker.paragraph(), user)
