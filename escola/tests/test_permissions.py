#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 14:26.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

import pytest
from django.test.testcases import TestCase

from helpers.utils import create_aluno, create_turma, create_cargo, cargo_muda_ocupante

pytestmark = pytest.mark.django_db


class TestPermissionToLider(TestCase):
    def test_doesnt_allow_two_lideres(self):
        turma = create_turma()
        lider_inicial = create_aluno(turma)
        cargo = create_cargo(lider_inicial.user, nivel=1, turma=turma)
        assert lider_inicial.user.has_perm('escola.editar_horario', turma)
        assert lider_inicial.user.has_perm('escola.can_add_materia', turma)
        assert lider_inicial.user.has_perm('escola.can_add_tarefa', turma)
        lider_dois = create_aluno(turma)
        cargo_muda_ocupante(lider_dois.user, cargo)
        assert not lider_inicial.user.has_perm('escola.editar_horario', turma)
        assert not lider_inicial.user.has_perm('escola.can_add_materia', turma)
        assert not lider_inicial.user.has_perm('escola.can_add_tarefa', turma)

        assert lider_dois.user.has_perm('escola.editar_horario', turma)
        assert lider_dois.user.has_perm('escola.can_add_materia', turma)
        assert lider_dois.user.has_perm('escola.can_add_tarefa', turma)
