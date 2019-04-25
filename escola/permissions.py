#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 18:06.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
from rolepermissions.checkers import has_role, has_permission
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
    """Verifica se pode adicionar aluno na turma"""
    if user.is_superuser:
        return True

    if user == turma.regente:
        return True

    if has_permission(user, 'add_aluno_g'):
        return True

    return False


@register_object_checker()
def edit_horario(role, user, turma):
    """Verifica se pode mudar o horario da turma"""
    if user.is_superuser:
        return True

    if has_permission(user, 'edit_horario_g'):
        return True

    if user == turma.regente or user == turma.lider or user == turma.vicelider:
        return True

    return False
