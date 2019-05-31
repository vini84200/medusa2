#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.test.client import Client
from .user_utils import create_aluno_user
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from .models import Turma
import pytest


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
