#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 17:02.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
from rolepermissions.checkers import has_role
from rolepermissions.permissions import register_object_checker

from escola.models import MateriaDaTurma
from escola.roles import Professor


@register_object_checker()
def create_tarefa(role, user, materia: MateriaDaTurma):
    """
    Verifica se o usuario tem permissão para criar uma tarefa para essa materia
    :return: Bool se tem perm
    """
    if user.is_superuser:
        return True

    if role == Professor:
        return True

    if has_role(user, 'admin') and materia.turma == user.Aluno.turma and materia.turma.lider == user:
        return True

    return False


@register_object_checker()
def add_aluno(role, user, turma):
    if user.is_superuser:
        return True

    if user == turma.regente:
        return True

    if has_role(user, 'admin'):
        return True

    return False