import datetime

import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from escola.models import Evento, EventoTurma, ProvaMarcada, ProvaAreaMarcada, ProvaMateriaMarcada

pytestmark = pytest.mark.django_db

# Evento


def test_evento_create(faker):
    initial = Evento.objects.count()
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert initial + 1 == Evento.objects.count()


def test_evento_get_nome(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.get_nome() == nome


def test_evento_get_data(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.get_data() == data


def test_evento_get_descricao(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.get_descricao() == descricao


def test_evento_get_owner(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.get_owner() == owner


def test_evento_somebody_has_permition_to_edit_denies(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    somebody = mixer.blend(User)
    assert a.has_permition_edit(somebody) is False


def test_evento_owner_has_permition_to_edit_accept(faker):
    nome = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome, data, descricao, owner)
    assert a.has_permition_edit(owner) is True

def test_evento_update(faker):
    nome_original = faker.sentence()
    nome_novo = faker.sentence()
    data = faker.date_time()
    descricao = faker.paragraph()
    owner = mixer.blend(User)
    a = Evento.create(nome_original, data, descricao, owner)
    assert not nome_novo == nome_original  # Se isso der problema, rode novamente
    assert a.get_nome() == nome_original
    a.update(nome=nome_novo)
    assert a.get_nome() == nome_novo
