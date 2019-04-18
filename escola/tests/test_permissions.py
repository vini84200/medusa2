#  Developed by Vinicius José Fritzen
#  Last Modified 17/04/19 16:42.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import pytest
from django.test.testcases import TestCase
from guardian.shortcuts import get_perms_for_model

from escola.conftest import *

# pytestmark = pytest.mark.django_db

# TODO: 17/04/2019 por wwwvi: Resolver falhas
@pytest.mark.xfail(reason="Desconhecido,"
                          " django.contrib.auth.models.Permission.DoesNotExist: Permission matching query does not exist.")
def test_doesnt_allow_two_lideres():
    aluno, turma = create_aluno_e_turma()
    lider_inicial = aluno
    print(turma)
    print(Turma.objects.all())
    print(aluno)
    print(get_perms_for_model(turma))
    print(get_perms_for_model(Turma))
    print(aluno.get_all_permissions(turma))
    cargo = create_cargo(lider_inicial, nivel=1, turma=turma)
    assert lider_inicial.has_perm('escola.mudar_horario', turma)
    assert lider_inicial.has_perm('escola.can_add_materia', turma)
    assert lider_inicial.has_perm('escola.can_add_tarefa', turma)
    lider_dois = create_aluno(turma=turma)
    cargo_muda_ocupante(lider_dois, cargo)
    assert not lider_inicial.has_perm('escola.mudar_horario', turma)
    assert not lider_inicial.has_perm('escola.can_add_materia', turma)
    assert not lider_inicial.has_perm('escola.can_add_tarefa', turma)

    assert lider_dois.has_perm('escola.mudar_horario', turma)
    assert lider_dois.has_perm('escola.can_add_materia', turma)
    assert lider_dois.has_perm('escola.can_add_tarefa', turma)
